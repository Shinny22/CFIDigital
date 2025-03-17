### Pourquoi créer une application dans Django ?

1. **Modularité** : Django utilise le concept d'applications pour diviser un projet en modules indépendants. Chaque application peut être pensée comme un ensemble de fonctionnalités ou un domaine spécifique (exemple : gestion des utilisateurs, gestion des paiements, etc.).
   
2. **Réutilisabilité** : Une application bien conçue peut être réutilisée dans d'autres projets Django sans beaucoup de modifications. Par exemple, si tu crées une application pour gérer les paiements, tu pourrais l'utiliser dans un autre projet.

3. **Organisation** : Les applications permettent de mieux structurer le code en regroupant les modèles, vues, templates, tests, etc., selon leurs responsabilités.

4. **Scalabilité** : Avec des applications modulaires, il est plus facile d'ajouter ou de modifier des fonctionnalités dans un projet au fil du temps.

---

### Comment structurer ta base de données en applications Django

Dans ton cas, avec les tables fournies (gestion des inscriptions/réinscriptions), voici une suggestion de structuration en applications :

#### Structure suggérée des applications

| **Application**       | **Responsabilités/Tables associées**                                            |
|------------------------|-------------------------------------------------------------------------------|
| `academique`           | Gestion des mentions, parcours, cycles, niveaux, et classes.                 |
| `etudiant`             | Gestion des étudiants, photos et tuteurs.                                    |
| `inscription`          | Gestion des inscriptions/réinscriptions et des années académiques.           |
| `paiement`             | Gestion des frais, paiements, factures, et tout ce qui est lié aux finances. |

---

#### Organisation et mise en place

##### 1. **Créer les applications** :
Utilise la commande pour chaque module :
```bash
python manage.py startapp academique
python manage.py startapp etudiant
python manage.py startapp inscription
python manage.py startapp paiement
```

##### 2. **Définir les modèles pour chaque application** :
Chaque application contient ses propres modèles dans `models.py`. Voici un exemple pour chaque application :

---

**App : `academique`**
```python
from django.db import models

class Mention(models.Model):
    id_filiere = models.AutoField(primary_key=True)
    nom_filiere = models.CharField(max_length=100)
    libelle_filiere = models.TextField()

    def __str__(self):
        return self.nom_filiere


class Parcours(models.Model):
    id_option = models.AutoField(primary_key=True)
    nom_option = models.CharField(max_length=100)
    libelle_option = models.TextField()
    mention = models.ForeignKey(Mention, on_delete=models.CASCADE, related_name="parcours")

    def __str__(self):
        return self.nom_option


class Cycle(models.Model):
    id_cycle = models.AutoField(primary_key=True)
    nom_cycle = models.CharField(max_length=100)
    libelle_cycle = models.TextField()

    def __str__(self):
        return self.nom_cycle


class Niveau(models.Model):
    id_niveau = models.AutoField(primary_key=True)
    nom_niveau = models.CharField(max_length=100)
    libelle_niveau = models.TextField()
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="niveaux")

    def __str__(self):
        return self.nom_niveau


class Classe(models.Model):
    id_classe = models.AutoField(primary_key=True)
    nom_classe = models.CharField(max_length=100)
    libelle_classe = models.TextField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="classes")
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return self.nom_classe
```

---

**App : `etudiant`**
```python
from django.db import models

class Etudiant(models.Model):
    id_etudiant = models.AutoField(primary_key=True)
    nom_etudiant = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    pays_naissance = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=50)
    sexe = models.CharField(max_length=10)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    def __str__(self):
        return self.nom_etudiant


class Photo(models.Model):
    id_photo = models.AutoField(primary_key=True)
    libelle_photo = models.CharField(max_length=100)
    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE, related_name="photo")

    def __str__(self):
        return f"Photo de {self.etudiant.nom_etudiant}"


class Tuteur(models.Model):
    id_tuteur = models.AutoField(primary_key=True)
    nom_tuteur = models.CharField(max_length=100)
    prenom_tuteur = models.CharField(max_length=100)
    tel_tuteur = models.CharField(max_length=15)
    email_tuteur = models.EmailField(unique=True)
    nationalite_tuteur = models.CharField(max_length=50)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="tuteurs")

    def __str__(self):
        return f"{self.nom_tuteur} {self.prenom_tuteur}"
```

---

**App : `inscription`**
```python
from django.db import models
from etudiant.models import Etudiant

class AnneeAcademique(models.Model):
    id_annee_academique = models.AutoField(primary_key=True)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.date_debut.year}-{self.date_fin.year}"


class Enregistrement(models.Model):
    TYPE_CHOICES = [
        ("Inscription", "Inscription"),
        ("Reinscription", "Reinscription"),
    ]
    id_enregistrement = models.AutoField(primary_key=True)
    date_enregistrement = models.DateField()
    type_enregistrement = models.CharField(max_length=15, choices=TYPE_CHOICES)
    semestre = models.CharField(max_length=20)
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name="enregistrements")
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="enregistrements")

    def __str__(self):
        return f"{self.type_enregistrement} - {self.semestre} ({self.etudiant.nom_etudiant})"
```

---

**App : `paiement`**
```python
from django.db import models
from inscription.models import Enregistrement

class FraisPaiement(models.Model):
    id_frais_paiement = models.AutoField(primary_key=True)
    libelle_frais_paiement = models.CharField(max_length=100)
    montant_frais_paiement = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.libelle_frais_paiement


class Facture(models.Model):
    id_facture = models.AutoField(primary_key=True)
    numero_facture = models.CharField(max_length=20)
    date_facture = models.DateField()
    montant_facture = models.DecimalField(max_digits=10, decimal_places=2)
    frais_paiement = models.ForeignKey(FraisPaiement, on_delete=models.CASCADE, related_name="factures")

    def __str__(self):
        return self.numero_facture


class Paiement(models.Model):
    id_paiement = models.AutoField(primary_key=True)
    numero_paiement = models.CharField(max_length=20)
    date_paiement = models.DateField()
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="paiements")

    def __str__(self):
        return self.numero_paiement
```

---

### Avantages de cette structure

1. **Lisibilité** : Chaque application se concentre sur un domaine spécifique.
2. **Facilité de gestion** : Les relations entre tables sont définies au sein des applications.
3. **Réutilisation** : Si tu souhaites développer un autre projet similaire, tu pourras réutiliser certaines applications.
4. **Clarté pour les tests et API** : Tu peux écrire des tests unitaires et des serializers par application.

Si tu veux des détails sur la création des **API** ou des migrations, fais-le-moi savoir ! 😊


super user info :

Username (leave blank to use 'pauloyeremoke'): shinny
Email address: shinny@gmail.com
Password:shinny
Password (again):shinny



#info database owner

'NAME': 'cfi_bd',
#            'USER': 'admin',
#            'PASSWORD': 'admin123',
#            'HOST': 'localhost',
#            'PORT': '5432',


#commande de connexion à pgadmin  CLI de cfi_bd :
psql -U admin -d cfi_bd -h localhost
