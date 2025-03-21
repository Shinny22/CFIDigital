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


from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    senderOperator = serializers.CharField(max_length=20)
    senderIndicatif = serializers.CharField(max_length=5)
    senderPhone = serializers.CharField(max_length=20)
    receiverPhone = serializers.CharField(max_length=20)
    user = serializers.CharField(max_length=100)

class CheckPaymentSerializer(serializers.Serializer):
    paymentId = serializers.CharField(max_length=100)

class WithdrawalSerializer(serializers.Serializer):
    receiverOperator = serializers.CharField(max_length=20)
    receiverIndicatif = serializers.CharField(max_length=5)
    receiverPhone = serializers.CharField(max_length=20)
    amount = serializers.FloatField()
    senderIndicatif = serializers.CharField(max_length=5)
    senderOperator = serializers.CharField(max_length=20)
    senderPhone = serializers.CharField(max_length=20)
    paymentId = serializers.CharField(max_length=100)