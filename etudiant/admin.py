from django.contrib import admin
from .models import Etudiant,Tuteur, Photo


# Register your models here.

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'matricule', 'date_naissance')  # Affiche le matricule dans la liste
    readonly_fields = ('matricule')  # Matricule non modifiable

admin.site.register(Etudiant)
admin.site.register(Photo)
admin.site.register(Tuteur)


