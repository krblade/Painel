from django.contrib import admin

# Register your models here.
from paginas.models import TesteTable
from paginas.models import TesteB
from registros.models import LOTE, GERENCIA

admin.site.register(TesteTable)
admin.site.register(TesteB)
admin.site.register(LOTE)
admin.site.register(GERENCIA)
