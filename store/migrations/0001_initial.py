# Generated by Django 4.1.5 on 2023-05-18 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategorija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=150, unique=True)),
                ('identifikator', models.SlugField(max_length=100, unique=True)),
                ('opis', models.TextField(max_length=500, unique=True)),
                ('slika', models.ImageField(blank=True, upload_to='kategorija')),
            ],
        ),
        migrations.CreateModel(
            name='Proizvod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imeproizvoda', models.CharField(max_length=150, unique=True)),
                ('identifikator', models.SlugField(max_length=100, unique=True)),
                ('opis', models.TextField(max_length=500, unique=True)),
                ('cijena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slika', models.ImageField(blank=True, upload_to='proizvod')),
                ('akcija', models.IntegerField()),
                ('dostupno', models.BooleanField(default=True)),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('azurirano', models.DateTimeField(auto_now=True)),
                ('kategorija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.kategorija')),
            ],
        ),
    ]
