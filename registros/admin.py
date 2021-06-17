from django.contrib import admin
from registros.models import LOTE, GERENCIA, MATERIAL, LOTE_HIS

# Register your models here.
admin.site.register(LOTE)
admin.site.register(GERENCIA)
admin.site.register(MATERIAL)
admin.site.register(LOTE_HIS)