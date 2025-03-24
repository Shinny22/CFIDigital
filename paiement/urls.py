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


# from django.urls import path
# from .views import PlacePaymentView, CheckPaymentView, WithdrawalView

# urlpatterns = [
#     path('place-payment/', PlacePaymentView.as_view(), name='place-payment'),
#     path('check-payment/', CheckPaymentView.as_view(), name='check-payment'),
#     path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
# ]