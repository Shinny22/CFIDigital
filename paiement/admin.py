from django.contrib import admin
from .models import (
 FraisPaiement, Facture, Paiement
)

# Register your models here.

admin.site.register(FraisPaiement)
admin.site.register(Facture)
admin.site.register(Paiement)
