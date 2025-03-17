from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Compte

class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Compte
        fields = ['email', 'nom', 'prenom', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
