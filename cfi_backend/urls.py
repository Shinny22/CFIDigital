"""
URL configuration for cfi_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Obtenir un access + refresh token
    TokenRefreshView,  # Rafraîchir un access token
    TokenVerifyView  # Vérifier si un token est valide
)
from grappelli.urls import urlpatterns as grappelli_urlpatterns

# from inscription.views import ValiderInscriptionView
from inscription.views import valider_inscription
from inscription.views import place_payment
from inscription.views import check_payment

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
    path('admin/', include(grappelli_urlpatterns)),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/comptes/', include('comptes.urls')),
    path('admin/', admin.site.urls),
    path('academique/', include('academique.urls')),
    path('etudiant/', include('etudiant.urls')),
    path('inscription/', include('inscription.urls')),
    # path('valider-inscription/', ValiderInscriptionView.as_view(), name='valider-inscription'),
    # path('valider-inscription/', valider_inscription, name='valider-inscription'),
    path('valider-inscription/', include('inscription.urls'),name='valider-inscription'),
    path('', include('inscription.urls'), name='place_payment'),
    path('', include('inscription.urls'), name='check_payment'),
    path('paiement/', include('paiement.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
