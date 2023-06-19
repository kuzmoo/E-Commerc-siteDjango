from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import KontaktPoruka

class FormaZaPrijavu(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=70, required=True)
    email = forms.EmailField(max_length=120, help_text='eg. tvojemail@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        labels = {
        'first_name': 'Ime:',
        'last_name': 'Prezime:',
        'username': 'Korisničko ime',
        'password1': 'Sifra',
        'password2': 'Potvrdi sifru',
        'email': 'Email adresa'
    }
        
class KontaktForma(forms.ModelForm):
    class Meta:
        model = KontaktPoruka
        fields = ['ime', 'email', 'subject', 'poruka']