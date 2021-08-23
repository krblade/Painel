from django.contrib import admin
from registros.models import LOTE, GERENCIA, LEILAO, COMPRADOR, DISPUTA_ABERTA, MATERIAL, LOTE_DET, HIST_LOTE

# Register your models here.
admin.site.register(LOTE)
admin.site.register(GERENCIA)
admin.site.register(MATERIAL)
admin.site.register(LOTE_DET)
admin.site.register(LEILAO)
admin.site.register(COMPRADOR)
admin.site.register(DISPUTA_ABERTA)
admin.site.register(HIST_LOTE)