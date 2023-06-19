from .models import Kategorija,KorpaProizvodi, Korpa
from .views import _korpa_id

def brojac(request):
    proizvod_brojac = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            korpa = Korpa.objects.filter(korpa_id = _korpa_id(request))
            korpa_proizvodi = KorpaProizvodi.objects.all().filter(korpa = korpa[:1])
            for korpa_proizvod in korpa_proizvodi:
                proizvod_brojac += korpa_proizvod.kolicina
        except Korpa.DoesNotExist:
            proizvod_brojac = 0
    return dict(proizvod_brojac = proizvod_brojac)

def menu_link(request):
    links = Kategorija.objects.all()
    return {'links': links}
