from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
   FraisPaiementViewSet, FactureViewSet, PaiementViewSet
)

router = DefaultRouter()
router.register('frais-paiements', FraisPaiementViewSet)
router.register('factures', FactureViewSet)
router.register('paiements', PaiementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
