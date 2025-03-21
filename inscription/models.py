from django.db import models
from datetime import datetime
from django.forms import ValidationError
from etudiant.models import Etudiant
from academique.models import Classe


class AnneeAcademique(models.Model):
    id_annee_academique = models.AutoField(primary_key=True)
    nom_annee_academique = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.date_debut.year}-{self.date_fin.year}"


class Enregistrement(models.Model):
  
    id_enregistrement = models.AutoField(primary_key=True)
    date_enregistrement = models.DateField()
    type_enregistrement = models.CharField(max_length=15)
    semestre = models.CharField(max_length=2)  # Ajout des choix prédéfinis
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name="enregistrements")
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="enregistrements")
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, related_name="enregistrements")

    def __str__(self):
        return f"{self.type_enregistrement} - {self.semestre} ({self.etudiant.nom}) {self.classe}"
    
    def clean(self):
        if self.type_enregistrement == "Inscription" and self.semestre != "S1":
            raise ValidationError("Pour une Inscription, le semestre doit être S1.")
        if self.type_enregistrement == "Reinscription" and self.semestre not in ["S3", "S5"]:
            raise ValidationError("Pour une Réinscription, le semestre doit être S3 ou S5.")
        
    def save(self, *args, **kwargs):
        # Générer le matricule si non défini
        if not self.etudiant.matricule:
            self.etudiant.matricule = self.generer_matricule()
            self.etudiant.save()  # Sauvegarder l'étudiant avec le matricule généré
        super().save(*args, **kwargs)

    def generer_matricule(self):
        """
        Générer le matricule au format :
        date_de_naissance + classe.nom + annee_academique
        """
        date_naissance_str = self.etudiant.date_naissance.strftime('%d%m%Y')  # Format DDMMYYYY
        return f"{date_naissance_str}{self.classe.nom_classe}{self.annee_academique}"


class Universite(models.Model):
    etudiant = models.OneToOneField("etudiant.Etudiant", on_delete=models.CASCADE, related_name="universite")
    photo = models.OneToOneField("etudiant.Photo", on_delete=models.CASCADE, related_name="universite")
    tuteur = models.ForeignKey("etudiant.Tuteur", on_delete=models.CASCADE, related_name="universites")
    mention = models.ForeignKey("academique.Mention", on_delete=models.CASCADE, related_name="universites")
    parcours = models.ForeignKey("academique.Parcours", on_delete=models.CASCADE, related_name="universites")
    cycle = models.ForeignKey("academique.Cycle", on_delete=models.CASCADE, related_name="universites")
    niveau = models.ForeignKey("academique.Niveau", on_delete=models.CASCADE, related_name="universites")
    classe = models.ForeignKey("academique.Classe", on_delete=models.CASCADE, related_name="universites")
    annee_academique = models.ForeignKey("inscription.AnneeAcademique", on_delete=models.CASCADE, related_name="universites")
    enregistrement = models.ForeignKey("inscription.Enregistrement", on_delete=models.CASCADE, related_name="universites")
    # facture = models.ForeignKey("paiement.Facture", on_delete=models.CASCADE, related_name="universites")
    # paiement = models.ForeignKey("paiement.Paiement", on_delete=models.CASCADE, related_name="universites")

    def __str__(self):
        return f"{self.etudiant.nom} - {self.annee_academique}" 





























# class Semestre(models.Model):
#     id_semestre=models.AutoField(primary_key=True)
#     nom_semestre=models.CharField(max_length=15, blank=True, null=True)
#     libelle_semestre=models.CharField(max_length=15)
#     # annee_Academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name="semestres")
      
#     def __str__(self):
#         return f"{self.nom_semestre}"

#    ------------------------------------------------------------------------------------------------
# MAIN ------------------------------------------------------------------------------------------------



# from rest_framework import serializers

# class CustomInscriptionSerializer(serializers.Serializer):
#     nom_etudiant = serializers.CharField()
#     prenom_etudiant = serializers.CharField()
#     matricule = serializers.CharField()
#     cours_inscrits = serializers.SerializerMethodField()
#     statut_inscription = serializers.CharField()
#     total_paiements = serializers.DecimalField(max_digits=10, decimal_places=2)

#     def get_cours_inscrits(self, obj):
#         return [cours.titre for cours in obj["inscription"].cours.all()]

#     def to_representation(self, instance):
#         return {
#             "nom_etudiant": instance["etudiant"].nom,
#             "prenom_etudiant": instance["etudiant"].prenom,
#             "matricule": instance["etudiant"].matricule,
#             "cours_inscrits": self.get_cours_inscrits(instance),
#             "statut_inscription": instance["inscription"].statut,
#             "total_paiements": instance["paiement"].montant_paye if instance["paiement"] else 0.00,
#         }
