# Generated by Django 5.1.5 on 2025-02-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etudiant', '0008_alter_etudiant_email_alter_tuteur_email_tuteur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='mot_de_passe',
        ),
        migrations.AddField(
            model_name='etudiant',
            name='status',
            field=models.CharField(choices=[('Nouveau', 'nouveau'), ('Ancien', 'ancien'), ('Redoublant', 'redoublant'), ('Travailleur', 'travailleur')], default='nouveau', max_length=20, null=True),
        ),
    ]
