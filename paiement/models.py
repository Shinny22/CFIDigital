from django.db import models

# Create your models here.
from django.db import models
from inscription.models import Enregistrement

class FraisPaiement(models.Model):
    id_frais_paiement = models.AutoField(primary_key=True)
    libelle_frais_paiement = models.CharField(max_length=100)
    montant_frais_paiement = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.libelle_frais_paiement


class Facture(models.Model):
    id_facture = models.AutoField(primary_key=True)
    numero_facture = models.CharField(max_length=30)
    date_facture = models.DateField()
    montant_facture = models.DecimalField(max_digits=10, decimal_places=2)
    frais_paiement = models.ForeignKey(FraisPaiement, on_delete=models.CASCADE, related_name="factures")

    def __str__(self):
        return self.numero_facture


class Paiement(models.Model):
    id_paiement = models.AutoField(primary_key=True)
    numero_paiement = models.CharField(max_length=20)
    date_paiement = models.DateField()
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="paiements")

    def __str__(self):
        return self.numero_paiement
