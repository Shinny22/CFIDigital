from django.contrib import admin
from .models import Enregistrement,AnneeAcademique, Universite



class EnregistrementAdmin(admin.ModelAdmin):

    list_display = ('etudiant', 'classe', 'annee_academique')




# Register your models here.
admin.site.register(Enregistrement, EnregistrementAdmin)
admin.site.register(AnneeAcademique)
admin.site.register(Universite)
