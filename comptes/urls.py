from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import InscriptionView, ConnexionView

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
