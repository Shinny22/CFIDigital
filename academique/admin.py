from django.contrib import admin
from .models import Mention, Parcours, Cycle, Niveau, Classe

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom_classe', 'niveau', 'libelle_classe', 'parcours')  
    # Définit les colonnes visibles dans la liste des classes dans l’admin.
    
    search_fields = ('nom_classe', 'niveau')  
    # Ajoute une barre de recherche pour permettre de chercher par `nom` ou `niveau`.
    
    list_filter = ('nom_classe', 'niveau')  
    # Ajoute des filtres sur le côté droit pour filtrer par `semestre` ou `niveau`.

    ordering = ('niveau',)  
    # Définit un tri par défaut des classes par `niveau`.

class ParcoursAdmin(admin.ModelAdmin):
    list_display = ('id_option', 'nom_option', 'libelle_option', 'mention')
    search_fields = ('nom_option', 'libelle_option', 'mention__nom_mention')  # Recherche par nom et mention
    list_filter = ('mention',)


class CycleAdmin(admin.ModelAdmin):
    list_display = ('id_cycle', 'nom_cycle', 'libelle_cycle')
    search_fields = ('nom_cycle', 'libelle_cycle')  # Permet de rechercher parmi les noms et libellés


admin.site.register(Mention)
admin.site.register(Parcours,ParcoursAdmin)
admin.site.register(Cycle, CycleAdmin)    
admin.site.register(Niveau)
admin.site.register(Classe,ClasseAdmin)
