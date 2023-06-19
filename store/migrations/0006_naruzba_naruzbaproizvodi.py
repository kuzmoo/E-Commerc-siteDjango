# Generated by Django 4.1.5 on 2023-05-21 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_korpa_korpaproizvodi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Naruzba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=200)),
                ('ukupno', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='EURA ukupno')),
                ('emailAddress', models.EmailField(blank=True, max_length=250, verbose_name='Email Adresa')),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('imenaplate', models.CharField(blank=True, max_length=250)),
                ('adresazanaplatu1', models.CharField(blank=True, max_length=250)),
                ('gradzanaplatu', models.CharField(blank=True, max_length=250)),
                ('postanskikod', models.CharField(blank=True, max_length=250)),
                ('zemljanaplate', models.CharField(blank=True, max_length=250)),
                ('imezaslanje', models.CharField(blank=True, max_length=250)),
                ('adresazaslanje1', models.CharField(blank=True, max_length=250)),
                ('gradzaslanje', models.CharField(blank=True, max_length=250)),
                ('postanskikodzaslanje', models.CharField(blank=True, max_length=250)),
                ('drzavazaslanje', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'db_table': 'Naruzba',
                'ordering': ['-kreirano'],
            },
        ),
        migrations.CreateModel(
            name='NaruzbaProizvodi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proizvod', models.CharField(max_length=250)),
                ('kolicina', models.IntegerField()),
                ('cijena', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Price')),
                ('naruzba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.naruzba')),
            ],
            options={
                'db_table': 'NaruzbaProizvodi',
            },
        ),
    ]