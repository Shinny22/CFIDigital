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
