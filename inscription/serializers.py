from rest_framework import serializers
from .models import AnneeAcademique, Enregistrement, Universite
from etudiant.serializers import EtudiantSerializer,PhotoSerializer, TuteurSerializer
from academique.serializers import ClasseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response




# Serializers
class UniversiteSerializer(serializers.ModelSerializer):
    etudiant = serializers.StringRelatedField()
    photo = serializers.StringRelatedField()
    tuteur = serializers.StringRelatedField()
    mention = serializers.StringRelatedField()
    parcours = serializers.StringRelatedField()
    cycle = serializers.StringRelatedField()
    niveau = serializers.StringRelatedField()
    classe = serializers.StringRelatedField()
    annee_academique = serializers.StringRelatedField()
    enregistrement = serializers.StringRelatedField()
    # facture = serializers.StringRelatedField()
    # paiement = serializers.StringRelatedField()

    class Meta:
        model = Universite
        fields = '__all__'

class AnneeAcademiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeAcademique
        fields = ['id_annee_academique', 'date_debut', 'date_fin']

# class EnregistrementSerializer(serializers.ModelSerializer):
    # etudiant = EtudiantSerializer(read_only=True)  # Inclure les informations de l'étudiant
    # annee_academique = AnneeAcademiqueSerializer(read_only=True)  # Inclure les informations de l'année académique
  
    # class Meta:
    #     model = Enregistrement
    #     fields = [
    #         'id_enregistrement', 'date_enregistrement', 'type_enregistrement', 
    #         'semestre', 'annee_academique', 'etudiant'
    #     ]
      



class EnregistrementSerializer(serializers.ModelSerializer):
    # etudiant = EtudiantSerializer()
    # photo = PhotoSerializer()  # Si photo est un champ de Etudiant
    tuteur = TuteurSerializer(read_only=True)  # Correction ici
    classe = serializers.CharField(source="classe.nom_classe",read_only=True)
    filiere = serializers.CharField(source="classe.filiere.nom_filiere", read_only=True)
    niveau = serializers.CharField(source="classe.niveau.nom_niveau", read_only=True)
    cycle = serializers.CharField(source="classe.niveau.cycle.nom_cycle", read_only=True)
    # paiement_status = serializers.SerializerMethodField()
    # libelle_photo = serializers.CharField(max_length=255)
    # image = serializers.ImageField()

    class Meta:
        model = Enregistrement
        fields = [
            "id_enregistrement", 
            "date_enregistrement",
            "etudiant",
            "tuteur",
            "annee_academique",
            "semestre",
            "classe",
            "filiere",
            "niveau",
            "cycle",
            # "paiement_status",
        ]


    # @api_view(['POST'])
    # def verifier_etudiant(request):
    #     matricule = request.data.get("matricule")
    #     nom = request.data.get("nom")
    #     prenom = request.data.get("prenom")
        
    #     try:
    #         etudiant = Compte.objects.get(matricule=matricule)
    #         if etudiant.nom == nom and etudiant.prenom == prenom:
    #             return Response({"valide": True})
    #         else:
    #             return Response({"valide": False, "message": "Données incorrectes."})
    #     except Compte.DoesNotExist:
    #         return Response({"valide": False, "message": "Matricule introuvable."})
    
    # def get_paiement_status(self, obj):
    #     """
    #     Retourne le statut de paiement de l'étudiant (exemple : "en attente", "payé")
    #     """
    #     # Supposons que tu as un modèle Paiement lié à Enregistrement
    #     paiement = getattr(obj, "paiement", None)  # Vérifie si un paiement existe
    #     if paiement and paiement.est_paye:  # Vérifie si le paiement est validé
    #         return "payé"
    #     return "en attente"
