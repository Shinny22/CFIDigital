from rest_framework import serializers
from .models import Etudiant,Photo,Tuteur

class TuteurSerializer(serializers.ModelSerializer):
 # Inclure les informations de l'étudiant

    class Meta:
        model = Tuteur
        fields = [
           'id_tuteur', 'nom', 'prenom', 'tel'
          
             ]

class EtudiantSerializer(serializers.ModelSerializer):
    tuteur = TuteurSerializer()
    class Meta:
        model = Etudiant
        fields = [
            'id_etudiant', 'nom', 'prenom','date_naissance', 'lieu_naissance', 
            'pays_naissance', 'nationalite', 'status','sexe', 'telephone','matricule','tuteur'
        ]
        # extra_kwargs = {
        #     'mot_de_passe': {'write_only': True}  # Masquer le mot de passe dans les réponses de l'API
        # }
        read_only_fields = ('matricule',)

        def validate_email(self, value):
            if Etudiant.objects.filter(email=value).exists():
                raise serializers.ValidationError("Un étudiant avec cet email existe déjà.")
            return value

class PhotoSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)  # Inclure les informations de l'étudiant

    class Meta:
        model = Photo
        fields = ['id_photo', 'libelle_photo', 'etudiant','image']

class TuteurSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)  # Inclure les informations de l'étudiant

    class Meta:
        model = Tuteur
        fields = [
            'etudiant','id_tuteur', 'tuteur_nom', 'prenom', 'tel'
          
             ]
