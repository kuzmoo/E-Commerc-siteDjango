from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .models import Kategorija, Proizvod, KorpaProizvodi, Korpa, Narudzba, NarudzbaProizvodi, pregled
import stripe
from django.conf import settings
from django.contrib.auth.models import Group, User
from .forms import FormaZaPrijavu, KontaktForma
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def home(request, kategorija_identifikator=None):
    proizvodi = None
    if kategorija_identifikator is not None:
        kategorija = get_object_or_404(Kategorija, identifikator=kategorija_identifikator)
        proizvodi = Proizvod.objects.filter(kategorija=kategorija, dostupno=True)
    else:
        proizvodi = Proizvod.objects.filter(dostupno=True)
    return render(request, 'home.html', {'kategorija_identifikator': kategorija_identifikator, 'proizvodi': proizvodi})


def proizvodPage(request, kategorija_identifikator, proizvod_identifikator):
    try:
        proizvod = Proizvod.objects.get(kategorija__identifikator = kategorija_identifikator, identifikator = proizvod_identifikator)
    except Exception as e:
        raise e
    
    if request.method == 'POST' and request.user.is_authenticated and request.POST['kontekst'].strip() != '':
        pregled.objects.create(proizvod=proizvod, 
                               korisnik = request.user, 
                               kontekst = request.POST['kontekst'])

    pregledi = pregled.objects.filter(proizvod=proizvod)
    
    return render(request, 'proizvod.html', {'proizvod':proizvod, 'pregledi': pregledi})


def _korpa_id(request):
    korpa = request.session.session_key
    if not korpa:
        korpa = request.session.create()
    return korpa


def dodaj_korpa(request, proizvod_id):
    proizvod = Proizvod.objects.get(id=proizvod_id)
    try:
        korpa = Korpa.objects.get(korpa_id=_korpa_id(request))
    except Korpa.DoesNotExist:
        korpa = Korpa.objects.create(korpa_id=_korpa_id(request))
        korpa.save()

    try:
        korpa_proizvod = KorpaProizvodi.objects.get(proizvod=proizvod, korpa=korpa)
        if korpa_proizvod.kolicina < korpa_proizvod.proizvod.akcija:
            korpa_proizvod.kolicina += 1
        korpa_proizvod.save()
    except KorpaProizvodi.DoesNotExist:
        korpa_proizvod = KorpaProizvodi.objects.create(
            proizvod=proizvod,
            kolicina=1,
            korpa=korpa
        )
        korpa_proizvod.save()

    return redirect('korpa_detalji')




def korpa_detalji(request, total=0, brojac=0, korpa_proizvodi=None):
    try:
        korpa = Korpa.objects.get(korpa_id=_korpa_id(request))
        korpa_proizvodi = KorpaProizvodi.objects.filter(korpa=korpa, aktivno=True)
        for korpa_proizvod in korpa_proizvodi:
            total += (korpa_proizvod.proizvod.cijena * korpa_proizvod.kolicina)
            brojac += korpa_proizvod.kolicina
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_ukupno = int(total * 100)
    opis = 'Z-STORE - Nova Prodavnica'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(email=email, source=token)
            cijena = stripe.Charge.create(
                amount=stripe_ukupno,
                currency='usd',
                description=opis,
                customer=customer.id
            )

            try:
                narudzba_detalji = Narudzba.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                narudzba_detalji.save()
                for korpa_proizvod in korpa_proizvodi:
                    svi_proizvodi = NarudzbaProizvodi.objects.create(
                        proizvod=korpa_proizvod.proizvod.imeproizvoda,
                        kolicina=korpa_proizvod.kolicina,
                        cijena=korpa_proizvod.proizvod.cijena,
                        narudzba=narudzba_detalji
                    )
                    svi_proizvodi.save()

                    # Smanjivanje kolicine zaliha
                    proizvodi = Proizvod.objects.get(id=korpa_proizvod.proizvod.id)
                    proizvodi.akcija = int(korpa_proizvod.proizvod.akcija - korpa_proizvod.kolicina)
                    proizvodi.save()
                    korpa_proizvod.delete()
                    
                    print('Narudzba je kreirana')
                return redirect('zahvalnastranica', narudzba_detalji.id)
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e

    return render(request, "korpa.html", dict(korpa_proizvodi = korpa_proizvodi, total = total, brojac = brojac, data_key = data_key, stripe_ukupno = stripe_ukupno, opis = opis ))

def korpa_brisanje(request, proizvod_id):
    korpa = Korpa.objects.get(korpa_id = _korpa_id(request))
    proizvod = get_object_or_404(Proizvod, id = proizvod_id)
    korpa_proizvod = KorpaProizvodi.objects.get(proizvod=proizvod, korpa=korpa)
    if korpa_proizvod.kolicina > 1:
        korpa_proizvod.kolicina -= 1
        korpa_proizvod.save()
    else:
        korpa_proizvod.delete()
    return redirect ('korpa_detalji')

def korpa_brisanje_proizvod(request, proizvod_id):
    korpa = Korpa.objects.get(korpa_id = _korpa_id(request))
    proizvod = get_object_or_404(Proizvod, id = proizvod_id)
    korpa_proizvod = KorpaProizvodi.objects.get(proizvod=proizvod, korpa=korpa)
    korpa_proizvod.delete()
    return redirect ('korpa_detalji')


def zahvalna_stranica(request, narudzba_id):
    if narudzba_id:
        kupac_narudzba = get_object_or_404(Narudzba, id = narudzba_id)
        return render(request, 'zahvalnastranica.html', {'kupac_narudzba': kupac_narudzba})
    
def prijavaPregled(request):
    if request.method == 'POST':
        form = FormaZaPrijavu(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            prijava_korisnika = User.objects.get(username=username)
            kupac_group = Group.objects.get(name='Kupci')
            kupac_group.user_set.add(prijava_korisnika)
    else:
        form = FormaZaPrijavu()
    return render(request, 'prijava.html', {'form' : form})

def prijavaNaloga(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('prijava')
    else:
        form = AuthenticationForm()
    return render(request, 'prijavanaloga.html', {'form': form})

def odjava(request):
    logout(request)
    return redirect('prijavanaloga')

@login_required(redirect_field_name='nex', login_url='prijavanaloga')
def istorijaNarudzbi(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        detalji_narudzbe = Narudzba.objects.filter(emailAddress=email)
    return render(request, 'lista_proizvoda.html', {'detalji_narudzbe': detalji_narudzbe})

@login_required(redirect_field_name='nex', login_url='prijavanaloga')
def pogledajNarudzbu(request, narudzba_id):
    if request.user.is_authenticated:
        email = str(request.user.email)
        narudzba = Narudzba.objects.get(id=narudzba_id, emailAddress=email)
        narudzba_proizvodi = NarudzbaProizvodi.objects.filter(narudzba=narudzba)
    return render(request, 'narudzba_detalji.html', {'narudzba': narudzba, 'narudzba_proizvodi': narudzba_proizvodi})


def pretrazivanje(request):
    ime_proizvoda = request.GET.get('imeproizvoda')
    proizvodi = Proizvod.objects.filter(imeproizvoda__contains=ime_proizvoda)
    return render(request, 'home.html', {'proizvodi': proizvodi})


@login_required(redirect_field_name='nex', login_url='prijavanaloga') 
def kontakt(request):
    if request.method == 'POST':
        form = KontaktForma(request.POST)
        if form.is_valid():
            form.save()
            ime = form.cleaned_data['ime']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            poruka = form.cleaned_data['poruka']

            message = f"Ime: {ime}\nEmail: {email}\nSubject: {subject}\nPoruka: {poruka}"
            send_mail(
                subject='Novi kontakt',
                message=message,
                from_email=email,
                recipient_list=['nikola.kuz99@gmail.com'], 
                fail_silently=False
            )

            return render(request, 'kontakt_uspjesno.html')
    else:
        form = KontaktForma()

    return render(request, 'kontakt.html', {'form': form})


def onama(request):
    return render(request, 'onama.html')