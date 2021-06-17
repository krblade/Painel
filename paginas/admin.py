from django.contrib import admin

# Register your models here.
from paginas.models import TesteTable
from paginas.models import TesteB

admin.site.register(TesteTable)
admin.site.register(TesteB)