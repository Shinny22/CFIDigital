from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import (
   Etudiant, Photo, Tuteur
)
from .serializers import (
    EtudiantSerializer, PhotoSerializer,
    TuteurSerializer, 
    
)



class EtudiantViewSet(ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer

      # Mise à jour complète (PUT)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Mise à jour partielle (PATCH)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Suppression (DELETE)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Étudiant supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)

class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class TuteurViewSet(ModelViewSet):
    queryset = Tuteur.objects.all()
    serializer_class = TuteurSerializer


