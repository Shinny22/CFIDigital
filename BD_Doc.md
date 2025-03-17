```bash

from django.db import models

# Create your models here.


#CLASSE MENTION OU FILLERE
class Mention(models.Model):
    id_filiere = models.AutoField(primary_key=True)  # Auto-incrementing ID
    nom_filiere = models.CharField(max_length=255)
    libelle_filiere = models.CharField(max_length=255, null=True, blank=True)  # Optional description
    date_creation = models.DateTimeField(auto_now_add=True)  # Track when the mention is created


#CLASSE PACRCOURS OU OPTION

class Parcours(models.Model):
    id_option = models.AutoField(primary_key=True)
    nom_option = models.CharField(max_length=255)
    libelle_option = models.CharField(max_length=255, null=True, blank=True)
    mention = models.ForeignKey(Mention, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

#CLASSE CYCLE

class Cycle(models.Model):
    id_cycle = models.AutoField(primary_key=True)
    nom_cycle = models.CharField(max_length=255)
    libelle_cycle = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)


#CLASSE NIVEAU 
class Niveau(models.Model):
    id_niveau = models.AutoField(primary_key=True)
    nom_niveau = models.CharField(max_length=255)
    libelle_niveau = models.CharField(max_length=255, null=True, blank=True)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

#CLASSE CLASSE

class Classe(models.Model):
    id_classe = models.AutoField(primary_key=True)
    nom_classe = models.CharField(max_length=255)
    libelle_classe = models.CharField(max_length=255, null=True, blank=True)
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

#CLASSE ANNEE ACADEMIQUE

class AnneeAcademique(models.Model):
    id_annee_academique = models.AutoField(primary_key=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    active = models.BooleanField(default=False)  # Useful to track the current academic year
    date_creation = models.DateTimeField(auto_now_add=True)

#CLASSE ETUDIANT

class Etudiant(models.Model):
    id_etudiant = models.AutoField(primary_key=True)
    nom_etudiant = models.CharField(max_length=255)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=255)
    pays_naissance = models.CharField(max_length=255)
    nationalite = models.CharField(max_length=255)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)  # For hashed passwords
    date_creation = models.DateTimeField(auto_now_add=True)

#PHOT 

class Photo(models.Model):
    id_photo = models.AutoField(primary_key=True)
    libelle_photo = models.CharField(max_length=255)
    image = models.ImageField(upload_to="photos/")
    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE)


#CLASSE TUTEUR

class Tuteur(models.Model):
    id_tuteur = models.AutoField(primary_key=True)
    nom_tuteur = models.CharField(max_length=255)
    prenom_tuteur = models.CharField(max_length=255)
    tel_tuteur = models.CharField(max_length=15)
    email_tuteur = models.EmailField()
    nationalite_tuteur = models.CharField(max_length=255)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

# ENREGISTREMENT 

class Enregistrement(models.Model):
    id_enregistrement = models.AutoField(primary_key=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    type_enregistrement = models.CharField(max_length=20, choices=[('Inscription', 'Inscription'), ('Reinscription', 'Réinscription')])
    semestre = models.CharField(max_length=10)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)


#CLASSE FRAIS DE PAIEMENT

class FraisPaiement(models.Model):
    id_frais_paiement = models.AutoField(primary_key=True)
    libelle_frais_paiement = models.CharField(max_length=255)
    montant_frais_paiement = models.DecimalField(max_digits=10, decimal_places=2)
    enregistrement = models.ForeignKey(Enregistrement, on_delete=models.CASCADE)

#CLASSE FACTURE 

class Facture(models.Model):
    id_facture = models.AutoField(primary_key=True)
    numero_facture = models.CharField(max_length=50, unique=True)
    date_facture = models.DateField(auto_now_add=True)
    montant_facture = models.DecimalField(max_digits=10, decimal_places=2)
    frais_paiement = models.ForeignKey(FraisPaiement, on_delete=models.CASCADE)


#CLASSE PAIEMENT

class Paiement(models.Model):
    id_paiement = models.AutoField(primary_key=True)
    numero_paiement = models.CharField(max_length=50, unique=True)
    date_paiement = models.DateField(auto_now_add=True)
    montant_paiement = models.DecimalField(max_digits=10, decimal_places=2)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
```