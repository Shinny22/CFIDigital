# Generated by Django 5.1.5 on 2025-02-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='numero_facture',
            field=models.CharField(max_length=30),
        ),
    ]
