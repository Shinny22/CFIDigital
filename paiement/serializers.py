from rest_framework import serializers
from .models import FraisPaiement, Facture, Paiement

class FraisPaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraisPaiement
        fields = ['id_frais_paiement', 'libelle_frais_paiement', 'montant_frais_paiement']

class FactureSerializer(serializers.ModelSerializer):
    frais_paiement = FraisPaiementSerializer(read_only=True)  # Inclure les informations du frais de paiement

    class Meta:
        model = Facture
        fields = ['id_facture', 'numero_facture', 'date_facture', 'montant_facture', 'frais_paiement']

class PaiementSerializer(serializers.ModelSerializer):
    facture = FactureSerializer(read_only=True)  # Inclure les informations de la facture associée

    class Meta:
        model = Paiement
        fields = ['id_paiement', 'numero_paiement', 'date_paiement', 'facture']
