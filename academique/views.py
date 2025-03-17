from rest_framework.viewsets import ModelViewSet
from .models import (
    Mention, Parcours, Cycle, Niveau, Classe
)
from .serializers import (
    MentionSerializer, ParcoursSerializer, CycleSerializer, NiveauSerializer,
    ClasseSerializer
)

class MentionViewSet(ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer

class ParcoursViewSet(ModelViewSet):
    queryset = Parcours.objects.all()
    serializer_class = ParcoursSerializer

class CycleViewSet(ModelViewSet):
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer

class NiveauViewSet(ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer

class ClasseViewSet(ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer




