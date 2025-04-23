from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     EtudiantViewSet, PhotoViewSet, TuteurViewSet
    
)

router = DefaultRouter()
router.register('etudiants', EtudiantViewSet)
router.register('photos', PhotoViewSet)
router.register('tuteurs', TuteurViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
]
