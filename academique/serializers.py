from rest_framework import serializers
from .models import Mention, Parcours, Cycle, Niveau, Classe

class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention
        fields = ['id_filiere', 'nom_filiere', 'libelle_filiere']
        # Le serializer expose les champs de la table Mention pour l'API

class ParcoursSerializer(serializers.ModelSerializer):
    mention = MentionSerializer(read_only=True)  # Inclure les informations de la Mention associée

    class Meta:
        model = Parcours
        fields = ['id_option', 'nom_option', 'libelle_option', 'mention']

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ['id_cycle', 'nom_cycle', 'libelle_cycle']

class NiveauSerializer(serializers.ModelSerializer):
    cycle = CycleSerializer(read_only=True)  # Inclure les informations du Cycle associé

    class Meta:
        model = Niveau
        fields = ['id_niveau', 'nom_niveau', 'libelle_niveau', 'cycle']

class ClasseSerializer(serializers.ModelSerializer):
    niveau = NiveauSerializer(read_only=True)  # Inclure les informations du Niveau associé
    parcours = ParcoursSerializer(read_only=True)  # Inclure les informations du Parcours associé

    class Meta:
        model = Classe
        fields = ['id_classe', 'nom_classe', 'libelle_classe', 'niveau', 'parcours']
