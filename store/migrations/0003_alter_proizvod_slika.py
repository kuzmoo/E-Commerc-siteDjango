# Generated by Django 4.1.5 on 2023-05-19 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_kategorija_options_alter_proizvod_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proizvod',
            name='slika',
            field=models.ImageField(blank=True, default='profiles/error.jpg', null=True, upload_to='proizvod'),
        ),
    ]