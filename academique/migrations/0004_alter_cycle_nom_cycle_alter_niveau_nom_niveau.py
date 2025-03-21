# Generated by Django 5.1.5 on 2025-01-24 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academique', '0003_alter_cycle_nom_cycle_alter_mention_nom_filiere_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='nom_cycle',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='niveau',
            name='nom_niveau',
            field=models.CharField(choices=[('l1', 'L2'), ('l2', 'L2'), ('l3', 'L3'), ('dut1', 'DUT1'), ('dut2', 'DUT2'), ('master1', 'Master1'), ('master2', 'Master2')], max_length=100, unique=True),
        ),
    ]
