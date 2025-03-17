from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Compte
from .serializers import InscriptionSerializer
from rest_framework.response import Response


class InscriptionView(generics.CreateAPIView):
    queryset = Compte.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "Utilisateur créé avec succès"}, status=201)

class ConnexionView(TokenObtainPairView):
    permission_classes = [AllowAny]
