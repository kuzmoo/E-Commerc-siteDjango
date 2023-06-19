from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Kategorija(models.Model):
    ime = models.CharField(max_length=150, unique=True)
    identifikator = models.SlugField(max_length=100, unique=True)
    opis = models.TextField(max_length=500, unique=True)
    slika = models.ImageField(upload_to='kategorija', blank=True)

    class Meta:
        ordering = ('ime',)
        verbose_name = 'kategorija'
        verbose_name_plural = 'kategorije'

    def get_url(self):
        return reverse('proizvod_sa_kategorijom', args=[self.identifikator])

    def __str__(self):
        return self.ime
    
class Proizvod(models.Model):
    imeproizvoda = models.CharField(max_length=150, unique=True)
    identifikator = models.SlugField(max_length=100, unique=True)
    opis = models.TextField(max_length=500, unique=True)
    kategorija = models.ForeignKey(Kategorija, on_delete=models.CASCADE)
    cijena = models.DecimalField(max_digits=10, decimal_places=2)
    slika = models.ImageField(upload_to='proizvod', null=True, blank=True, default="greska/error.jpg")
    akcija = models.IntegerField()
    dostupno = models.BooleanField(default=True)
    kreirano = models.DateTimeField(auto_now_add=True)
    azurirano = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('imeproizvoda',)
        verbose_name = 'proizvod'
        verbose_name_plural = 'proizvodi'

    def get_url(self):
        return reverse('proizvod_detalji', args=[self.kategorija.identifikator, self.identifikator])

    def __str__(self):
        return self.imeproizvoda
    

class Korpa(models.Model):
    korpa_id = models.CharField(max_length=150, blank=True)
    datum_dodavanja = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Korpa'
        ordering = ['datum_dodavanja']

    def __str__(self):
        return self.korpa_id
    
class KorpaProizvodi(models.Model):
    proizvod = models.ForeignKey(Proizvod, on_delete=models.CASCADE)
    korpa = models.ForeignKey(Korpa, on_delete=models.CASCADE)
    kolicina = models.IntegerField()
    aktivno = models.BooleanField(default=True)

    class Meta:
        db_table = 'KorpaProizvodi'

    def sub_total(self):
        return self.proizvod.cijena * self.kolicina
    
    def __str__(self):
        return self.proizvod
    
class Narudzba(models.Model):
    token = models.CharField(max_length=200, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='KM ukupno')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    kreirano = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'Narudzba'
        ordering = ['-kreirano']

    def __str__(self):
        return str(self.id)
    
class NarudzbaProizvodi(models.Model):
    proizvod = models.CharField(max_length=250)
    kolicina = models.IntegerField()
    cijena = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=' KM ')
    narudzba = models.ForeignKey(Narudzba, on_delete=models.CASCADE)

    class Meta:
        db_table = 'NarudzbaProizvodi'

    def sub_total(self):
        return self.kolicina * self.cijena

    def __str__(self):
        return self.proizvod
    
class pregled(models.Model):
    proizvod = models.ForeignKey(Proizvod, on_delete=models.CASCADE)
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    kontekst = models.CharField(max_length=550)

    def __str__(self):
        return self.proizvod.imeproizvoda
    
class KontaktPoruka(models.Model):
    ime = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    poruka = models.TextField()

    def __str__(self):
        return self.subject