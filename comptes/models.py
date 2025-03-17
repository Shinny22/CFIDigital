from django.contrib.auth.models import Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission, PermissionsMixin
# Create your models here.
from django.db import models

class CompteManager(BaseUserManager):
    def create_user(self, email, password=None, role='etudiant', **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)

class Compte(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('etudiant', 'Etudiant'),
        ('professeur', 'Professeur'),
        ('tuteur', 'Tuteur'),
    ]
    
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='compte_user_set',  # Ajoutez un related_name unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='compte_user_permissions_set',  # Ajoutez un related_name unique
        blank=True
    )

    objects = CompteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"
