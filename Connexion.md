````sql

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Manager personnalisé pour gérer la création d'utilisateurs
class CompteManager(BaseUserManager):
    def create_user(self, matricule, email, password=None, **extra_fields):
        """
        Crée et renvoie un utilisateur avec un matricule et un mot de passe.
        """
        if not matricule:
            raise ValueError('Le matricule doit être renseigné')
        user = self.model(matricule=matricule, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule, email, password=None, **extra_fields):
        """
        Crée et renvoie un superutilisateur avec un matricule et un mot de passe.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(matricule, email, password, **extra_fields)

# Modèle de Compte personnalisé
class Compte(AbstractBaseUser):
    # Identifiant unique pour l'utilisateur, les étudiants l'auront comme matricule
    matricule = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Matricule des étudiants
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  # Si le compte est actif ou non
    is_staff = models.BooleanField(default=False)  # Permet d'identifier les administrateurs
    date_creation = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)  # Dernière connexion

    # Définir le manager pour ce modèle
    objects = CompteManager()

    USERNAME_FIELD = 'matricule'  # Utiliser le matricule comme identifiant pour les étudiants
    REQUIRED_FIELDS = ['email']  # Les autres champs obligatoires

    def __str__(self):
        return f'Compte de {self.matricule or self.email}'

    def save(self, *args, **kwargs):
        """
        Override save pour gérer des actions personnalisées si nécessaire
        """
        super().save(*args, **kwargs)

# Utilisation de ce modèle de compte pour l'étudiant
class Etudiant(models.Model):
    id_etudiant = models.AutoField(primary_key=True)
    nom_etudiant = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20, unique=True)  # Matricule unique pour chaque étudiant
    date_naissance = models.DateField()
    # Autres champs relatifs à l'étudiant...

    compte = models.OneToOneField(Compte, on_delete=models.CASCADE, related_name='etudiant')

    def __str__(self):
        return f'{self.nom_etudiant} - {self.matricule}'
