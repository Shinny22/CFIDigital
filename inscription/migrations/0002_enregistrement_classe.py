# Generated by Django 5.1.5 on 2025-01-22 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academique', '0001_initial'),
        ('inscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enregistrement',
            name='classe',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enregistrements', to='academique.classe'),
        ),
    ]
