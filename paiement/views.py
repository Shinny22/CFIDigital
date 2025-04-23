from rest_framework.viewsets import ModelViewSet
from .models import (
 Enregistrement, FraisPaiement, Facture, Paiement
)
from .serializers import ( FraisPaiementSerializer,
    FactureSerializer, PaiementSerializer
)


class FraisPaiementViewSet(ModelViewSet):
    queryset = FraisPaiement.objects.all()
    serializer_class = FraisPaiementSerializer

class FactureViewSet(ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer

class PaiementViewSet(ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer


##Essai 3


import os
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urlencode
from .models import Transaction
from .serializers import PaymentSerializer, CheckPaymentSerializer, WithdrawalSerializer
from dotenv import load_dotenv

load_dotenv()

# Fonction pour normaliser ou déduire l'opérateur
OPERATOR_PREFIXES = {
    'CG_MTNMOBILEMONEY': ['060', '061', '062', '063', '064', '065', '066', '067', '068', '069'],
    'CG_AIRTELMONEY': [
        '050', '051', '052', '053', '055', '057', '059', '054', '056', '058',
        '040', '041', '042', '043', '044', '045', '046', '047', '048', '049'
    ],
}

def get_operator(phone: str):
    prefix = phone[:3]
    for operator, prefixes in OPERATOR_PREFIXES.items():
        if prefix in prefixes:
            return operator
    return None

class PlacePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        monetbil_key = os.getenv("MONETBIL_KEY")
        if not monetbil_key:
            return Response({"error": "Les clés Monetbil ne sont pas configurées."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        phone = serializer.validated_data['senderPhone']
        operator = get_operator(phone)
        if not operator:
            return Response({"status": "OPERATOR_NOT_FOUND", "message": "operator not found"}, status=status.HTTP_403_FORBIDDEN)

        url = "https://api.monetbil.com/payment/v1/placePayment"
        data = {
            "phonenumber": f"{serializer.validated_data['senderIndicatif']}{phone}",
            "service": monetbil_key,
            "country": "CG",
            "currency": "XAF",
            "operator": operator,
            "amount": serializer.validated_data['amount'],
            "user": serializer.validated_data['user']
        }

        try:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"error": "Une erreur est survenue", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPaymentView(APIView):
    def post(self, request):
        serializer = CheckPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.monetbil.com/payment/v1/checkPayment"
        data = urlencode({"paymentId": serializer.validated_data['paymentId']})

        try:
            response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            result_data = response.json()

            if "transaction" in result_data and "status" in result_data["transaction"]:
                status_code = result_data["transaction"]["status"]

                if status_code == "1":
                    return Response({"message": "Paiement réussi"}, status=status.HTTP_200_OK)
                elif status_code == "-1":
                    return Response({"message": "Paiement annulé"}, status=status.HTTP_400_BAD_REQUEST)
                elif status_code == "0":
                    return Response({"message": "Paiement échoué"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "Statut inconnu ou en attente"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": "Transaction non valide"}, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({"error": "Une erreur est survenue", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawalView(APIView):
    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        monetbil_key = os.getenv("MONETBIL_KEY")
        monetbil_secret = os.getenv("MONETBIL_SECRET")
        if not monetbil_key or not monetbil_secret:
            return Response({"error": "Les clés Monetbil ne sont pas configurées."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        receiver_phone = serializer.validated_data['receiverPhone']
        receiver_operator = get_operator(receiver_phone)
        if not receiver_operator:
            return Response({"status": "OPERATOR_NOT_FOUND", "message": "operator not found"}, status=status.HTTP_403_FORBIDDEN)

        url = "https://api.monetbil.com/v1/payouts/withdrawal"
        data = {
            "service_key": monetbil_key,
            "service_secret": monetbil_secret,
            "phonenumber": f"{serializer.validated_data['receiverIndicatif']}{receiver_phone}",
            "amount": str(serializer.validated_data['amount']),
            "operator": receiver_operator,
        }

        try:
            response = requests.post(url, data=urlencode(data), headers={"Content-Type": "application/x-www-form-urlencoded"})
            response_data = response.json()

            Transaction.objects.create(                                              
                paymentId=serializer.validated_data['paymentId'],
                receiverPhone=receiver_phone,
                senderOperator=serializer.validated_data['senderOperator'],
                receiverOperator=receiver_operator,
                senderIndicatif=serializer.validated_data['senderIndicatif'],
                receiverIndicatif=serializer.validated_data['receiverIndicatif'],
                senderPhone=serializer.validated_data['senderPhone'],
                amount=response_data.get("amount"),
                transactionStatus=response_data.get("success"),
            )

            return Response({"message": "Retrait effectué avec succès", "data": response_data}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Erreur lors du retrait", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
