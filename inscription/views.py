from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.decorators import action
from rest_framework import  viewsets, status
from etudiant.models import Tuteur,Etudiant
from .serializers import (
    AnneeAcademiqueSerializer, EtudiantSerializer,  EnregistrementSerializer, UniversiteSerializer
)
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AnneeAcademique, Etudiant, Enregistrement, Universite
from .serializers import (
    EtudiantSerializer, EnregistrementSerializer,
)
from academique.models import Classe
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import time
import hmac
import hashlib
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from dotenv import load_dotenv
import logging


# Vue pour inscrire un étudiant
class UniversiteViewSet(viewsets.ModelViewSet):
    queryset = Universite.objects.all()
    serializer_class = UniversiteSerializer

    @action(detail=False, methods=['post'])
    def inscrire_etudiant(self, request):
        from etudiant.models import Etudiant, Photo, Tuteur
        from academique.models import Mention, Parcours, Cycle, Niveau, Classe
        from inscription.models import AnneeAcademique, Enregistrement
        from paiement.models import Facture, Paiement
        
        required_fields = ["etudiant", "photo", "tuteur", "mention", "parcours", "cycle", "niveau", "classe", "annee_academique", "enregistrement", "facture", "paiement"]
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response({"error": f"Champs manquants: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            etudiant = Etudiant.objects.get(id=request.data["etudiant"])
            photo = Photo.objects.get(id=request.data["photo"], etudiant=etudiant)
            tuteur = Tuteur.objects.get(id=request.data["tuteur"], etudiant=etudiant)
            mention = Mention.objects.get(id=request.data["mention"])
            parcours = Parcours.objects.get(id=request.data["parcours"], mention=mention)
            cycle = Cycle.objects.get(id=request.data["cycle"])
            niveau = Niveau.objects.get(id=request.data["niveau"], cycle=cycle)
            classe = Classe.objects.get(id=request.data["classe"], niveau=niveau, parcours=parcours)
            annee_academique = AnneeAcademique.objects.get(id=request.data["annee_academique"])
            enregistrement = Enregistrement.objects.get(id=request.data["enregistrement"], etudiant=etudiant, annee_academique=annee_academique)
            facture = Facture.objects.get(id=request.data["facture"])
            paiement = Paiement.objects.get(id=request.data["paiement"], facture=facture)
        except (Etudiant.DoesNotExist, Photo.DoesNotExist, Tuteur.DoesNotExist, Mention.DoesNotExist, Parcours.DoesNotExist, Cycle.DoesNotExist, Niveau.DoesNotExist, Classe.DoesNotExist, AnneeAcademique.DoesNotExist, Enregistrement.DoesNotExist, Facture.DoesNotExist, Paiement.DoesNotExist):
            return Response({"error": "Une ou plusieurs données sont invalides ou inexistantes."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Universite.objects.filter(etudiant=etudiant, annee_academique=annee_academique).exists():
            return Response({"error": "L'étudiant est déjà inscrit pour cette année académique."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Universite
from etudiant.models import Etudiant, Photo, Tuteur
from academique.models import Mention, Parcours, Cycle, Niveau, Classe
from inscription.models import AnneeAcademique, Enregistrement

class UniversiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universite
        fields = '__all__'

class UniversiteValidationViewSet(viewsets.ViewSet):
    queryset = Universite.objects.all()
    serializer_class = UniversiteSerializer
    @action(detail=False, methods=['post'])
    def valider_donnees(self, request):
        """
        Vérifie si les données soumises existent bien dans la base de données en comparant par nom et vérifie les champs requis.
        """
        data = request.data
        if not data:
            return Response({"error": "Aucune donnée reçue"}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération des données
        etudiant_data = data.get('etudiant', {})
        tuteur_data = data.get('tuteur', {})
        enregistrement_data = data.get('enregistrement', {})

        # Champs requis
        required_etudiant_fields = ['nom', 'prenom', 'date_naissance', 'lieu_naissance', 'nationalite']
        required_tuteur_fields = ['nom', 'prenom', 'tel']
        required_enregistrement_fields = ['classe']

        # Vérifier les champs manquants
        missing_fields = {
            "etudiant": [field for field in required_etudiant_fields if not etudiant_data.get(field)],
            "tuteur": [field for field in required_tuteur_fields if not tuteur_data.get(field)],
            "enregistrement": [field for field in required_enregistrement_fields if not enregistrement_data.get(field)]
        }

        # Retourner les erreurs de champs manquants
        if any(missing_fields.values()):
            return Response({
                "error": "Certains champs sont manquants.",
                "missing_fields": {key: value for key, value in missing_fields.items() if value}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'existence de l'étudiant
        try:
            etudiant = Etudiant.objects.get(
                nom=etudiant_data["nom"],
                prenom=etudiant_data["prenom"],
                date_naissance=etudiant_data["date_naissance"]
            )
        except Etudiant.DoesNotExist:
            return Response({"error": "L'étudiant n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification des données de l'étudiant
        errors = {}
        if etudiant.lieu_naissance != etudiant_data.get("lieu_naissance"):
            errors["lieu_naissance"] = "Le lieu de naissance ne correspond pas."
        if etudiant.nationalite != etudiant_data.get("nationalite"):
            errors["nationalite"] = "La nationalité ne correspond pas."

        # Vérification de l'existence du tuteur
        try:
            tuteur = Tuteur.objects.get(
                nom=tuteur_data["nom"],
                prenom=tuteur_data["prenom"],
                tel=tuteur_data["tel"]
            )
        except Tuteur.DoesNotExist:
            return Response({"error": "Le tuteur n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'enregistrement
        try:
            classe = Classe.objects.get(nom=enregistrement_data['classe'])
            enregistrement = Enregistrement.objects.get(
                etudiant=etudiant,
                classe=classe
            )
        except (Classe.DoesNotExist, Enregistrement.DoesNotExist):
            return Response({"error": "Les données académiques sont incorrectes."}, status=status.HTTP_400_BAD_REQUEST)

        # Si des erreurs existent dans les champs de l'étudiant
        if errors:
            return Response({
                "error": "Certains champs ne correspondent pas.",
                "details": errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validation réussie
        return Response({
            "message": "Validation réussie, les données sont conformes.",
            "etudiant": etudiant.id,
            "tuteur": tuteur.id,
            "enregistrement": enregistrement.id
        }, status=status.HTTP_200_OK)
 

class AnneeAcademiqueViewSet(ModelViewSet):
    queryset = AnneeAcademique.objects.all()
    serializer_class = AnneeAcademiqueSerializer

class EtudiantViewSet(ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer

class EnregistrementViewSet(ModelViewSet):
    queryset = Enregistrement.objects.all()
    serializer_class = EnregistrementSerializer


@csrf_exempt 
@api_view(['POST'])
def valider_inscription(request):
    if request.method == 'POST':
        # Récupérer les données avec vérification
        if not request.data:
            return Response({
                "error": "Aucune donnée reçue"
            }, status=status.HTTP_400_BAD_REQUEST)

        etudiant_data = request.data.get('etudiant', {})
        tuteur_data = request.data.get('tuteur', {})
        enregistrement_data = request.data.get('enregistrement', {})

        # Vérifier que toutes les données requises sont présentes
        required_etudiant_fields = ['nom', 'prenom', 'date_naissance']
        required_tuteur_fields = ['nom', 'prenom', 'tel']
        required_enregistrement_fields = ['classe']

        # Vérifier les champs de l'étudiant
        missing_etudiant = [field for field in required_etudiant_fields if not etudiant_data.get(field)]
        if missing_etudiant:
            return Response({
                "error": "Données étudiant manquantes",
                "missing_fields": missing_etudiant
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier les champs du tuteur
        missing_tuteur = [field for field in required_tuteur_fields if not tuteur_data.get(field)]
        if missing_tuteur:
            return Response({
                "error": "Données tuteur manquantes",
                "missing_fields": missing_tuteur
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier les champs d'enregistrement
        missing_enregistrement = [field for field in required_enregistrement_fields if not enregistrement_data.get(field)]
        if missing_enregistrement:
            return Response({
                "error": "Données enregistrement manquantes",
                "missing_fields": missing_enregistrement
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            etudiant = Etudiant.objects.get(
                nom=etudiant_data.get("nom"),
                prenom=etudiant_data.get("prenom"),
                date_naissance=etudiant_data.get("date_naissance"),
                lieu_naissance=etudiant_data.get("lieu_naissance"),
                nationalite=etudiant_data.get("nationalite"),
                telephone=etudiant_data.get("telephone"),
                sexe=etudiant_data.get("sexe"),
            )
        except Etudiant.DoesNotExist:
            return Response({"error": "L'étudiant n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier les informations de l'étudiant
        erreurs_etudiant = {}
        if etudiant.nom != etudiant_data.get("nom"):
            erreurs_etudiant["nom"] = "Le nom ne correspond pas."
        if etudiant.prenom != etudiant_data.get("prenom"):
            erreurs_etudiant["prenom"] = "Le prénom ne correspond pas."
        if etudiant.date_naissance.strftime("%Y-%m-%d") != etudiant_data.get("date_naissance"):
            erreurs_etudiant["date_naissance"] = "La date de naissance ne correspond pas."
        if etudiant.lieu_naissance != etudiant_data.get("lieu_naissance"):
            erreurs_etudiant["lieu_naissance"] = "Le lieu de naissance ne correspond pas."
        if etudiant.nationalite != etudiant_data.get("nationalite"):
            erreurs_etudiant["nationalite"] = "La nationalité ne correspond pas."
        if etudiant.telephone != etudiant_data.get("telephone"):
            erreurs_etudiant["telephone"] = "Le numero telephone ne correspond pas."
        if etudiant.sexe != etudiant_data.get("sexe"):
            erreurs_etudiant["sexe"] = "Le sexe ne correspond pas."

        # Vérifier le tuteur
        try:
            tuteur = Tuteur.objects.get(
                nom=tuteur_data.get("nom"),
                prenom=tuteur_data.get("prenom"),
                tel=tuteur_data.get("tel")
            )
        except Tuteur.DoesNotExist:
            return Response({"error": "Le tuteur n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier l'enregistrement
        try:
            classe = Classe.objects.get(nom_classe=enregistrement_data.get('classe'))
            annee_academique = AnneeAcademique.objects.get(nom_annee_academique=enregistrement_data.get('annee_academique'))

            enregistrement = Enregistrement.objects.filter(
                etudiant=etudiant,
                classe=classe,
                annee_academique=annee_academique
            ).first()

        except (Classe.DoesNotExist, Enregistrement.DoesNotExist):
            return Response({"error": "Les données académiques sont incorrectes."}, status=status.HTTP_400_BAD_REQUEST)

        # Si tout est valide
        return Response({
            "message": "Validation réussie, les données sont conformes.",
            "etudiant": etudiant.id_etudiant,
            "tuteur": tuteur.id_tuteur,
            "enregistrement": enregistrement.id_enregistrement
        }, status=status.HTTP_200_OK)

    return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


logger = logging.getLogger(__name__)
# load_dotenv()  
# @csrf_exempt 
# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# def place_payment(request):
#     try:
#         phone = request.data.get('phonenumber')
#         amount = request.data.get('amount')

#         # Vérification des données requises
#         if not phone or not amount:
#             return Response({
#                 'error': 'Données manquantes',
#                 'details': {
#                     'phonenumber': 'Requis' if not phone else None,
#                     'amount': 'Requis' if not amount else None
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Clé du service MonetBil
#         # Préparation des données à envoyer
#         data = {
           
#             "service": settings.MONETBIL_SERVICE_KEY,
#             "phonenumber": phone,
#             "amount": amount,
#             "country": "CG",
#             "currency": "XAF",
#             "notify_url" : settings.MONETBIL_NOTIFY_URL 
#         }

#         # URL de l'API MonetBil
#         url = 'https://api.monetbil.com/payment/v1/placePayment'

#         # En-têtes HTTP
#         headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             "Authorization": f"Bearer {settings.MONETBIL_SECRET_KEY}"
#             "Bearer RLoDzGvirr5Xikm24fX0EobXjNBmxq8CTqQQL5mByKl0qj66jDveYk8Rf743abSg"
#         }

#         # Envoi de la requête à MonetBil
#         response = requests.post(url, json=data, headers=headers, timeout=30, verify=False)

#         print(settings.MONETBIL_SECRET_KEY)
#         # Vérification du code HTTP de réponse
#         if response.status_code == 200:

#             return Response(response.json(), status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'error': 'Échec de la requête de paiement',
#                 'details': response.text
#             }, status=response.status_code)

#     except requests.exceptions.RequestException as e:
#         return Response({
#             'error': 'Erreur de connexion à MonetBil',
#             'details': str(e)
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt 
@api_view(['POST'])
@permission_classes([AllowAny]) 
def place_payment(request):
    try:
        phone = request.data.get('phonenumber')
        amount = request.data.get('amount')

        if not phone or not amount:
            return Response({
                'error': 'Données manquantes',
                'details': {
                    'phonenumber': 'Requis' if not phone else None,
                    'amount': 'Requis' if not amount else None
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "service": settings.MONETBIL_SERVICE_KEY,
            "phonenumber": phone,
            "amount": amount,
            "country": "CG",
            "currency": "XAF",
        }

        url = 'https://api.monetbil.com/payment/v1/placePayment'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f"Bearer {settings.MONETBIL_SECRET_KEY}"
        }

        response = requests.post(url, json=data, headers=headers, timeout=30, verify=False)
        print("Réponse MonetBil:", response.text)  # Debugging

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Échec de la requête de paiement',
                'details': response.json()
            }, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({
            'error': 'Erreur de connexion à MonetBil',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt 
# @api_view(['POST'])
# def check_payment(request):
#     # Récupérer et valider l'ID du paiement
#     print(request.data)
#     payment_id = request.data.get('paymentId')

#     if not payment_id:
#         return Response({
#             'error': 'ID de paiement requis'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     data = {'paymentId': payment_id}
#     url = 'https://api.monetbil.com/payment/v1/checkPayment'

#     try:
#         response = requests.post(url, json=data, timeout=30)
#         response_data = response.json() if response.content else {}
#         print(response_data)
#         if response.status_code == 200:
#             if 'transaction' in response_data:
#                 transaction = response_data['transaction']
#                 status_code = transaction.get('status')

#                 if status_code == 1:
#                     return Response({
#                         'message': 'Paiement réussi',
#                         'transaction': transaction
#                     }, status=status.HTTP_200_OK)
#                 elif status_code == -1:
#                     return Response({
#                         'message': 'Paiement annulé',
#                         'transaction': transaction
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({
#                         'message': 'Paiement échoué',
#                         'transaction': transaction
#                     }, status=status.HTTP_200_OK)
#             else:
#                 return Response({
#                     'error': 'Détails de transaction non trouvés'
#                 }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({
#                 'error': 'Échec de la vérification du paiement',
#                 'details': response_data
#             }, status=status.HTTP_400_BAD_REQUEST)

#     except requests.exceptions.RequestException as e:
#         return Response({
#             'error': 'Erreur lors de la vérification du paiement',
#             'details': str(e)
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt 
@api_view(['POST'])
def check_payment(request):
    print("Données reçues :", request.data)  # Debugging
    payment_id = request.data.get('paymentId')

    if not payment_id:
        return Response({'error': 'ID de paiement requis'}, status=status.HTTP_400_BAD_REQUEST)

    data = {'paymentId': payment_id}
    url = 'https://api.monetbil.com/payment/v1/checkPayment'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Bearer {settings.MONETBIL_SECRET_KEY}"
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        print("Réponse MonetBil:", response.text)  # Debugging

        response_data = response.json() if response.content else {}

        if response.status_code == 200:
            transaction = response_data.get('transaction')
            if not transaction:
                return Response({'error': 'Détails de transaction non trouvés'}, status=status.HTTP_400_BAD_REQUEST)

            status_code = transaction.get('status')

            if status_code == 1:
                return Response({'message': 'Paiement réussi', 'transaction': transaction}, status=status.HTTP_200_OK)
            elif status_code == -1:
                return Response({'message': 'Paiement annulé', 'transaction': transaction}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Paiement en attente ou échoué', 'transaction': transaction}, status=status.HTTP_200_OK)

        return Response({'error': 'Échec de la vérification du paiement', 'details': response_data}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({'error': 'Erreur lors de la vérification du paiement', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt 
# @api_view(["POST"])
# def monetbil_notification(request):
#     """Gérer les notifications de paiement de Monetbil"""
    
#     # Vérifier si request.data est bien un dictionnaire
#     if not request.data:
#         return Response({"error": "Aucune donnée reçue"}, status=status.HTTP_400_BAD_REQUEST)

#     if not isinstance(request.data, dict):
#         return Response({"error": "Format de données invalide"}, status=status.HTTP_400_BAD_REQUEST)

#     data = request.data
#     print("Notification reçue :", data)  # Debugging

#     # Vérifier si Monetbil a bien envoyé le statut du paiement
#     status_paiement = data.get("status", "")
#     transaction_id = data.get("transaction_id", "")

#     if not status_paiement:
#         return Response({"error": "Statut de paiement manquant"}, status=status.HTTP_400_BAD_REQUEST)

#     if status_paiement == "SUCCESS":
#         # TODO: Ajouter ici la logique métier (mise à jour en base, etc.)
#         print(f"✅ Paiement réussi pour transaction ID {transaction_id}")
#         return Response({"message": "Paiement validé"}, status=status.HTTP_200_OK)
#     else:
#         print(f"⚠️ Paiement échoué ou en attente: {status_paiement}")
#         return Response({"message": "Notification traitée, mais paiement non validé"}, status=status.HTTP_200_OK)




@csrf_exempt 
@api_view(["POST"])
def monetbil_notification(request):
    """Gérer les notifications de paiement de Monetbil"""

    print("Content-Type reçu :", request.content_type)  # Afficher le Content-Type
    print("Données brutes reçues :", request.body)  # Voir le contenu brut

    # Si le contenu est en text/plain, on tente de le convertir en JSON
    if request.content_type == "text/plain":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return Response({"error": "Format de données invalide"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = request.data  # Django REST Framework gère déjà le JSON

    print("Notification complète reçue :", data)  # Debugging

    # Vérification du statut de paiement
    status_paiement = data.get("status")
    transaction_id = data.get("paymentId")  # Assure-toi que MonetBil utilise bien "paymentId"

    if not status_paiement:
        return Response({
            "error": "Statut de paiement manquant",
            "details": data
        }, status=status.HTTP_400_BAD_REQUEST)

    if status_paiement == "REQUEST_ACCEPTED":
        return Response({
            "message": "Paiement en attente",
            "transaction_id": transaction_id,
            "details": data
        }, status=status.HTTP_200_OK)

    return Response({
        "message": "Notification traitée",
        "transaction_id": transaction_id,
        "details": data
    }, status=status.HTTP_200_OK)





# @api_view(["POST"])
# def place_payment(request):
#     """Démarrer un paiement"""
#     phone = request.data.get("phonenumber")  # Correction ici
#     amount = request.data.get("amount")

#     if not phone or not amount:
#         return Response({"error": "Numéro et montant requis"}, status=status.HTTP_400_BAD_REQUEST)

#     url = settings.MONETBIL_BASE_URL + "placePayment"
#     payload = {
#         "service": settings.MONETBIL_SERVICE_KEY,
#         "phonenumber": phone,
#         "amount": amount,
#         "notify_url": settings.MONETBIL_NOTIFY_URL,
#     }

#     try:
#         response = requests.post(url, json=payload)
#         print("Réponse brute de Monetbil :", response.text)  # Debugging

#         if "application/json" in response.headers.get("Content-Type", ""):
#             data = response.json()
#         else:
#             data = {"raw_response": response.text}  # Retourne la réponse brute si ce n'est pas du JSON

#         if response.status_code == 200:
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
#     except requests.RequestException as e:
#         return Response({"error": "Problème de connexion à Monetbil", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     except json.JSONDecodeError as e:
#         return Response({"error": "Réponse invalide de Monetbil", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(["POST"])
# def check_payment(request):
#     """Vérifier un paiement"""
#     payment_id = request.data.get("paymentId")

#     if not payment_id:
#         return Response({"error": "paymentId requis"}, status=status.HTTP_400_BAD_REQUEST)

#     url = settings.MONETBIL_BASE_URL + "checkPayment"
#     response = requests.post(url, json={"paymentId": payment_id})
#     data = response.json()

#     return Response(data, status=status.HTTP_200_OK)


# @csrf_exempt
# def monetbil_notification(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # Récupération des données
#             payment_id = data.get("paymentId")
#             status = data.get("transaction", {}).get("status")

#             if payment_id and status is not None:
#                 # Mise à jour du statut du paiement en BDD
#                 if status == 1:
#                     message = "Paiement réussi"
#                 elif status == -1:
#                     message = "Paiement annulé"
#                 else:
#                     message = "Paiement échoué"

#                 print(f"Paiement {payment_id} - {message}")
#                 return JsonResponse({"message": message}, status=200)
#             else:
#                 return JsonResponse({"error": "Données invalides"}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Format JSON invalide"}, status=400)
#     return JsonResponse({"error": "Méthode non autorisée"}, status=405)





# import os
# import requests
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from urllib.parse import urlencode
# from .models import Transaction  # Importation du modèle de transaction
# from .serializers import PaymentSerializer, CheckPaymentSerializer, WithdrawalSerializer
# from dotenv import load_dotenv

# load_dotenv()  # Charger les variables d'environnement

# class PlacePaymentView(APIView):
#     """
#     Vue pour initier un paiement via Monetbil.
#     """

#     def post(self, request):
#         serializer = PaymentSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         monetbil_key = os.getenv("MONETBIL_KEY")
#         if not monetbil_key:
#             return Response({"error": "Les clés Monetbil ne sont pas configurées."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         url = "https://api.monetbil.com/payment/v1/placePayment"
#         data = {
#             "phonenumber": f"{serializer.validated_data['senderIndicatif']}{serializer.validated_data['senderPhone']}",
#             "service": monetbil_key,
#             "country": "CG",
#             "currency": "XAF",
#             "operator": serializer.validated_data['senderOperator'],
#             "amount": serializer.validated_data['amount'],
#             "user": serializer.validated_data['user']
#         }

#         try:
#             response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
#             return Response(response.json(), status=response.status_code)
#         except requests.RequestException as e:
#             return Response({"error": "Une erreur est survenue", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CheckPaymentView(APIView):
#     """
#     Vue pour vérifier le statut d'un paiement via Monetbil.
#     """

#     def post(self, request):
#         serializer = CheckPaymentSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         url = "https://api.monetbil.com/payment/v1/checkPayment"
#         data = urlencode({"paymentId": serializer.validated_data['paymentId']})

#         try:
#             response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
#             result_data = response.json()

#             if "transaction" in result_data and "status" in result_data["transaction"]:
#                 status_code = result_data["transaction"]["status"]

#                 if status_code == "1":
#                     return Response({"message": "Paiement réussi"}, status=status.HTTP_200_OK)
#                 elif status_code == "-1":
#                     return Response({"message": "Paiement annulé"}, status=status.HTTP_400_BAD_REQUEST)
#                 elif status_code == "0":
#                     return Response({"message": "Paiement échoué"}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response({"message": "Statut inconnu ou en attente"}, status=status.HTTP_202_ACCEPTED)
#             else:
#                 return Response({"error": "Transaction non valide"}, status=status.HTTP_400_BAD_REQUEST)

#         except requests.RequestException as e:
#             return Response({"error": "Une erreur est survenue", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class WithdrawalView(APIView):
#     """
#     Vue pour effectuer un retrait via Monetbil.
#     """

#     def post(self, request):
#         serializer = WithdrawalSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         monetbil_key = os.getenv("MONETBIL_KEY")
#         monetbil_secret = os.getenv("MONETBIL_SECRET")

#         if not monetbil_key or not monetbil_secret:
#             return Response({"error": "Les clés Monetbil ne sont pas configurées."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         url = "https://api.monetbil.com/v1/payouts/withdrawal"
#         data = {
#             "service_key": monetbil_key,
#             "service_secret": monetbil_secret,
#             "phonenumber": f"{serializer.validated_data['receiverIndicatif']}{serializer.validated_data['receiverPhone']}",
#             "amount": str(serializer.validated_data['amount']),
#             "operator": serializer.validated_data['receiverOperator'],
#         }

#         try:
#             response = requests.post(url, data=urlencode(data), headers={"Content-Type": "application/x-www-form-urlencoded"})
#             response_data = response.json()

#             # Sauvegarder la transaction en base de données
#             transaction = Transaction.objects.create(
#                 paymentId=serializer.validated_data['paymentId'],
#                 receiverPhone=serializer.validated_data['receiverPhone'],
#                 senderOperator=serializer.validated_data['senderOperator'],
#                 receiverOperator=serializer.validated_data['receiverOperator'],
#                 senderIndicatif=serializer.validated_data['senderIndicatif'],
#                 receiverIndicatif=serializer.validated_data['receiverIndicatif'],
#                 senderPhone=serializer.validated_data['senderPhone'],
#                 amount=response_data.get("amount"),
#                 transactionStatus=response_data.get("success"),
#             )

#             return Response({"message": "Retrait effectué avec succès", "data": response_data}, status=status.HTTP_200_OK)

#         except requests.RequestException as e:
#             return Response({"error": "Erreur lors du retrait", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





























# class ValiderInscriptionView(APIView):
#     def post(self, request):
#         etudiant_data = request.data.get('etudiant')
#         photo_data = request.data.get('photo')
#         tuteur_data = request.data.get('tuteur')
#         enregistrement_data = request.data.get('enregistrement')
#         paiement_data = request.data.get('paiement')

#         etudiant_serializer = EtudiantSerializer(data=etudiant_data)
#         photo_serializer = PhotoSerializer(data=photo_data)
#         tuteur_serializer = TuteurSerializer(data=tuteur_data)
#         enregistrement_serializer = EnregistrementSerializer(data=enregistrement_data)
#         paiement_serializer = PaiementSerializer(data=paiement_data)

#         if (etudiant_serializer.is_valid() and photo_serializer.is_valid() and
#             tuteur_serializer.is_valid() and enregistrement_serializer.is_valid() and
#             paiement_serializer.is_valid()):

#             etudiant = etudiant_serializer.save()
#             photo_serializer.save(etudiant=etudiant)
#             tuteur_serializer.save(etudiant=etudiant)
#             enregistrement_serializer.save(etudiant=etudiant)
#             paiement_serializer.save()

#             return Response({"message": "Inscription validée avec succès"}, status=status.HTTP_201_CREATED)

#         return Response({
#             "etudiant": etudiant_serializer.errors,
#             "photo": photo_serializer.errors,
#             "tuteur": tuteur_serializer.errors,
#             "enregistrement": enregistrement_serializer.errors,
#             "paiement": paiement_serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    




# class UniversiteViewSet(viewsets.ModelViewSet):
#     queryset = Universite.objects.all()
#     serializer_class = UniversiteSerializer

#     @action(detail=False, methods=['post'])
#     def inscrire_etudiant(self, request):
#         from etudiant.models import Etudiant, Photo, Tuteur
#         from academique.models import Mention, Parcours, Cycle, Niveau, Classe
#         from inscription.models import AnneeAcademique, Enregistrement
#         from paiement.models import Facture, Paiement
        
#         required_fields = ["etudiant_nom", "photo_nom", "tuteur_nom", "mention_nom", "parcours_nom", "cycle_nom", "niveau_nom", "classe_nom", "annee_academique_nom", "enregistrement_nom", "facture_nom", "paiement_nom"]
#         missing_fields = [field for field in required_fields if field not in request.data]
        
#         if missing_fields:
#             return Response({"error": f"Champs manquants: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             etudiant = Etudiant.objects.get(nom=request.data["etudiant_nom"])
#             photo = Photo.objects.get(nom=request.data["photo_nom"], etudiant=etudiant)
#             tuteur = Tuteur.objects.get(nom=request.data["tuteur_nom"], etudiant=etudiant)
#             mention = Mention.objects.get(nom=request.data["mention_nom"])
#             parcours = Parcours.objects.get(nom=request.data["parcours_nom"], mention=mention)
#             cycle = Cycle.objects.get(nom=request.data["cycle_nom"])
#             niveau = Niveau.objects.get(nom=request.data["niveau_nom"], cycle=cycle)
#             classe = Classe.objects.get(nom=request.data["classe_nom"], niveau=niveau, parcours=parcours)
#             annee_academique = AnneeAcademique.objects.get(nom=request.data["annee_academique_nom"])
#             enregistrement = Enregistrement.objects.get(nom=request.data["enregistrement_nom"], etudiant=etudiant, annee_academique=annee_academique)
#             facture = Facture.objects.get(nom=request.data["facture_nom"])
#             paiement = Paiement.objects.get(nom=request.data["paiement_nom"], facture=facture)
#         except (Etudiant.DoesNotExist, Photo.DoesNotExist, Tuteur.DoesNotExist, Mention.DoesNotExist, Parcours.DoesNotExist, Cycle.DoesNotExist, Niveau.DoesNotExist, Classe.DoesNotExist, AnneeAcademique.DoesNotExist, Enregistrement.DoesNotExist, Facture.DoesNotExist, Paiement.DoesNotExist):
#             return Response({"error": "Une ou plusieurs données sont invalides ou inexistantes."}, status=status.HTTP_400_BAD_REQUEST)
        
#         if Universite.objects.filter(etudiant=etudiant, annee_academique=annee_academique).exists():
#             return Response({"error": "L'étudiant est déjà inscrit pour cette année académique."}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reinscription_etudiant(request):
    etudiant_id = request.data.get('etudiant_id')
    annee_id = request.data.get('annee_academique')

    try:
        etudiant = Etudiant.objects.get(id=etudiant_id)
        dernier_enregistrement = Enregistrement.objects.filter(etudiant=etudiant).order_by('-annee_academique').first()

        if not dernier_enregistrement:
            return Response({"error": "L'étudiant n'a pas encore été inscrit."}, status=400)

        # Vérification de la validation des examens
        if etudiant.a_valide_examens():  
            nouvelle_classe = get_classe_superieure(dernier_enregistrement.classe)
            statut = 'ancien'
        else:
            nouvelle_classe = dernier_enregistrement.classe  # Il redouble
            statut = 'redoublant'

        # Créer un nouvel enregistrement pour la réinscription
        enregistrement = Enregistrement.objects.create(
            etudiant=etudiant,
            annee_academique_id=annee_id,
            type_enregistrement="Reinscription",
            semestre="S3" if nouvelle_classe.niveau.ordre % 2 == 1 else "S5",
            classe=nouvelle_classe,
            statut_etudiant=statut
        )

        return Response({"message": "Réinscription réussie", "statut": statut, "classe": nouvelle_classe.nom_classe}, status=201)

    except Etudiant.DoesNotExist:
        return Response({"error": "Étudiant introuvable"}, status=404)

