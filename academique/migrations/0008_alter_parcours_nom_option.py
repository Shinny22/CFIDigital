# Generated by Django 5.1.5 on 2025-02-01 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academique', '0007_classe_capacité'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcours',
            name='nom_option',
            field=models.CharField(choices=[('genie_logiciel', 'Génie logiciel'), ('reseaux_telecommunication', 'Réseaux et télécommunication'), ('systemes_reseaux', 'Systèmes et réseaux'), ('administration_publique', 'Administration publique'), ('informatique de gestion', 'informatique de gestion')], max_length=100, unique=True),
        ),
    ]
