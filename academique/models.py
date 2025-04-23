from django.db import models

# Create your models here.


class Mention(models.Model):

    id_filiere = models.AutoField(primary_key=True)
    nom_filiere = models.CharField(max_length=100, unique=True)  # Utilisation des choix
    libelle_filiere = models.TextField()

    def __str__(self):
        # Affiche le libellé de la mention en utilisant les choix
        return f"{self.nom_filiere}"


class Parcours(models.Model):
  
    id_option = models.AutoField(primary_key=True)
    nom_option = models.CharField(max_length=100, unique=True)  # Utilisation des choix
    libelle_option = models.TextField()
    mention = models.ForeignKey(Mention,on_delete=models.CASCADE, related_name="parcours")


    # def __str__(self):
    #     """
    #     Retourne le libellé du parcours. Si `nom_option` est dans `PARCOURS_CHOICES`, 
    #     retourne le libellé correspondant. Sinon, retourne `nom_option` comme nouvelle entrée dynamique.
    #     """
    #     choix_existants = dict(self.PARCOURS_CHOICES)
    #     return choix_existants.get(self.nom_option, self.nom_option)

    def __str__(self):
        # Affiche le libellé du parcours
        return f"{self.nom_option}"


class Cycle(models.Model):
   

    id_cycle = models.AutoField(primary_key=True)
    nom_cycle = models.CharField(max_length=100, unique=True)  # Utilisation des choix
    libelle_cycle = models.TextField()

    def __str__(self):
        # Affiche le libellé du cycle en utilisant les choix
        return f"{self.nom_cycle}"
 
    

class Niveau(models.Model):

    id_niveau = models.AutoField(primary_key=True)
    nom_niveau = models.CharField(max_length=100, unique=True)  # Utilisation des choix
    libelle_niveau = models.TextField()
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="niveaux")

    def __str__(self):
        return f"{self.nom_niveau}"
 

class Classe(models.Model):

    id_classe = models.AutoField(primary_key=True)
    nom_classe = models.CharField(max_length=100, unique=True)
    capacité = models.CharField(max_length=90, blank=True,)
    libelle_classe = models.TextField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="classes")
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return self.nom_classe



