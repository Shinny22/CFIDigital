# Generated by Django 5.1.5 on 2025-02-14 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etudiant', '0009_remove_etudiant_mot_de_passe_etudiant_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='email',
        ),
    ]
