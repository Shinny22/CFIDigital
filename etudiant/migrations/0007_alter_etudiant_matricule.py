# Generated by Django 5.1.5 on 2025-01-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etudiant', '0006_alter_etudiant_matricule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
