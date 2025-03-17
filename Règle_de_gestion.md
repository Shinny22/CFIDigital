

Règle de production du système



•	Modélisation des tables en Django
•	Voici un aperçu de chaque table et de ses relations avec les autres :
•	1. Mention
•	Une Mention a plusieurs Parcours.
•	Relation : Mention 1,N → Parcours 1,1
•	2. Parcours
•	Un Parcours appartient à une Mention et a plusieurs Classes.
•	Relation :
•	Mention 1,N → Parcours 1,1
•	Parcours 1,N → Classe 1,1
•	3. Cycle et Niveau
•	Un Cycle contient plusieurs Niveaux.
•	Relation : Cycle 1,N → Niveau 1,1
•	4. Classe
•	Une Classe appartient à un Parcours et un Niveau.
•	Relation :
•	Parcours 1,N → Classe 1,1
•	Niveau 1,N → Classe 1,1
•	5. Année académique
•	Une Année académique contient plusieurs Enregistrements.
•	Relation : Année_academique 1,N → Enregistrement 1,1
•	6. Enregistrement
•	Un Enregistrement appartient à une Année académique, un Étudiant et peut avoir plusieurs Frais de paiement.
•	Relation :
•	Enregistrement 1,1 → Étudiant 1,N
•	Enregistrement 1,N → Frais_paiement 1,1
•	7. Frais de paiement
•	Les Frais de paiement sont associés à un Enregistrement et génèrent une Facture.
•	Relation :
•	Frais_paiement 1,N → Facture 1,1
•	8. Facture
•	Une Facture peut avoir plusieurs Paiements.
•	Relation : Facture 1,N → Paiement 1,1
•	9. Étudiant
•	Un Étudiant peut avoir plusieurs Tuteurs et une seule Photo.
•	Relation :
•	Étudiant 1,1 → Photo 1,1
•	Étudiant 1,1 → Tuteur 1,N
