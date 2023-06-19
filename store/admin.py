from django.contrib import admin
from .models import Kategorija, Proizvod, Narudzba, NarudzbaProizvodi, pregled, KontaktPoruka

class KategorijaAdmin(admin.ModelAdmin):
    list_display = ['ime', 'identifikator']
    prepopulated_fields = {'identifikator': ('ime',)}

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

admin.site.register(Kategorija, KategorijaAdmin)

class ProizvodAdmin(admin.ModelAdmin):
    list_display = ['imeproizvoda', 'cijena', 'akcija', 'dostupno', 'kreirano', 'azurirano']
    list_editable = ['cijena', 'akcija', 'dostupno']
    prepopulated_fields = {'identifikator': ('imeproizvoda',)}
    list_per_page = 5
    
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

admin.site.register(Proizvod, ProizvodAdmin)

class NarudzbaProizvodAdmin(admin.TabularInline):
    model = NarudzbaProizvodi
    fieldsets = [
    ('Proizvod', {'fields': ['proizvod'],}),
    ('Kolicina', {'fields': ['kolicina'],}),
    ('Cijena', {'fields': ['cijena'],}),
    ]
    readonly_fields = ['proizvod', 'kolicina', 'cijena']
    can_delete = False
    max_num = 0

@admin.register(Narudzba)
class NarudzbaAdmin(admin.ModelAdmin):

    list_display = ['id', 'billingName', 'emailAddress', 'kreirano']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'emailAddress']
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'kreirano', 'billingName', 'billingAddress1',
                       'billingCity', 'billingPostcode', 'billingCountry', 'shippingName', 'shippingAddress1',
                       'shippingCity', 'shippingPostcode', 'shippingCountry']
    
    fieldsets = [
        ('INFORMACIJE O NARUDZBI', {'fields': ['id', 'token', 'total', 'kreirano', ]}),
        ('INFORMACIJE O NAPLATI', {'fields': ['billingName', 'billingAddress1',
                       'billingCity', 'billingPostcode', 'billingCountry', 'emailAddress']}),
        ('INFORMACIJE O DOSTAVI', {'fields': ['shippingName', 'shippingAddress1',
                       'shippingCity', 'shippingPostcode', 'shippingCountry']})
    ]

    inlines = [
        NarudzbaProizvodAdmin,
    ]

    def has_delete_permission(self, request, obj = None):
        return False

    def has_add_permission(self, request):
        return False
    
    
admin.site.register(pregled)


class PorukaAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email']

admin.site.register(KontaktPoruka, PorukaAdmin)