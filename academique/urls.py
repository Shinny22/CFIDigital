from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MentionViewSet, ParcoursViewSet, CycleViewSet, NiveauViewSet, ClasseViewSet,
    
)

router = DefaultRouter()
router.register('mentions', MentionViewSet)
router.register('parcours', ParcoursViewSet)
router.register('cycles', CycleViewSet)
router.register('niveaux', NiveauViewSet)
router.register('classes', ClasseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
