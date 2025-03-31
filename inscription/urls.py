from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.routers import DefaultRouter
from .views import (
   AnneeAcademiqueViewSet, EtudiantViewSet, 
    EnregistrementViewSet, UniversiteValidationViewSet, UniversiteViewSet, check_payment, monetbil_notification, place_payment,valider_inscription)

router = DefaultRouter()

router.register('annees-academiques', AnneeAcademiqueViewSet)
router.register('etudiants', EtudiantViewSet)
router.register('enregistrements', EnregistrementViewSet)
router.register('universites', UniversiteViewSet)
router.register(r'universite-validation', UniversiteValidationViewSet, basename='universite-validation')



urlpatterns = [
    path('api/', include(router.urls)),
    path('', valider_inscription, name='valider_inscription'),
    path('inscrire-etudiant/', UniversiteViewSet.as_view({'post': 'inscrire_etudiant'}), name='inscrire-etudiant'),
    path('place_payment/', place_payment, name="place_payment"),
    path('check_payment', check_payment, name="check_payment"),
    path('notifications/', monetbil_notification, name="monetbil_notification"),
]


