from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
   CheckPaymentView, FraisPaiementViewSet, FactureViewSet, PaiementViewSet, PlacePaymentView, WithdrawalView
)

router = DefaultRouter()
router.register('frais-paiements', FraisPaiementViewSet)
router.register('factures', FactureViewSet)
router.register('paiements', PaiementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('place-payment/', PlacePaymentView.as_view(), name='place-payment'),
    path('check-payment/', CheckPaymentView.as_view(), name='check-payment'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
]