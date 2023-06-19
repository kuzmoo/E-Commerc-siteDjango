from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategorija/<slug:kategorija_identifikator>', views.home, name='proizvod_sa_kategorijom'),
    path('kategorija/<slug:kategorija_identifikator>/<slug:proizvod_identifikator>', views.proizvodPage, name='proizvod_detalji'),
    path('korpa/add/<int:proizvod_id>', views.dodaj_korpa, name='dodaj_korpa'),
    path('korpa', views.korpa_detalji, name="korpa_detalji"),
    path('korpa/remove/<int:proizvod_id>', views.korpa_brisanje, name='korpa_brisanje'),
    path('korpa/remove_proizvod/<int:proizvod_id>', views.korpa_brisanje_proizvod, name='korpa_brisanje_proizvod'),
    path('zahvalnastranica/<int:narudzba_id>', views.zahvalna_stranica, name='zahvalnastranica'),
    path('nalog/kreiraj/', views.prijavaPregled, name='prijava'),
    path('nalog/prijava/', views.prijavaNaloga, name='prijavanaloga'),
    path('nalog/odjava/', views.odjava, name='odjava'),
    path('istorija_narudzbi/', views.istorijaNarudzbi, name='istorija'),
    path('istorija/<int:narudzba_id>/', views.pogledajNarudzbu, name='detalji_narudzbe'),
    path('pretrazivanje/', views.pretrazivanje, name='pretrazivanje'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('onama/', views.onama, name='onama'),  
]
