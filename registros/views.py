from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LOTE

# Create your views here.
class LotesDetalheView(LoginRequiredMixin, ListView):
    model = LOTE
    template_name = 'table_lotesDetalhados.html'

    def get_queryset(self):

        #lote = self.get('buscaLote')
        #self.object_list = LOTE.objects.filter(lote_lote=lote)
        self.object_list = LOTE.objects.all()
        return self.object_list
