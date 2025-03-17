from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator
# Create your models here.

class Tuteur(models.Model):
    id_tuteur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    nationalite_tuteur = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nom}"

class Etudiant(models.Model):
    # STATUS_CHOICES = [
    #     ('Nouveau', 'nouveau'),
    #     ('Ancien', 'ancien'),
    #     ('Redoublant', 'redoublant'),
    #     ('Travailleur', 'travailleur'),
    # ]
     
    id_etudiant = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100,default='shinny')
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    pays_naissance = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=50)
    # addresse=models.CharField(max_length=50)
    sexe = models.CharField(max_length=10)
    telephone = models.CharField(max_length=15, unique=True)
    # email = models.EmailField(unique=True,validators=[
    
    #     RegexValidator(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    #                    message='Veuillez entrer une adresse email valide.'
    #                    ) ])
    # mot_de_passe = models.CharField(max_length=128, unique=True)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE, related_name="etudiant",default='')
    matricule = models.CharField(max_length=50, unique=True, blank=True,null=True)  # Champ pour le matricule
    status=models.CharField(max_length=20,null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom}"
    

class Photo(models.Model):
    id_photo = models.AutoField(primary_key=True)
    libelle_photo = models.CharField(max_length=100)
    etudiant = models.OneToOneField('Etudiant', on_delete=models.CASCADE, related_name="photo")
    image = models.ImageField(upload_to='photos_etudiants/', null=True, blank=True, unique=True)  # Champ pour stocker la photo

    def __str__(self):
        return f"Photo de {self.etudiant.nom}"




