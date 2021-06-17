from typing import List
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic.edit import CreateView
from .models import LOTE, LOTE_HIS, TESTES, HIST_LOTE
from django.urls import reverse_lazy
import csv

# Create your views here.
class LotesDetalheView(LoginRequiredMixin, ListView):
    model = LOTE
    template_name = 'table_lotesLista.html'

    def get_queryset(self):

        #lote = self.get('buscaLote')
        #self.object_list = LOTE.objects.filter(lote_lote=lote)
        self.object_list = LOTE.objects.all()
        return self.object_list

class LotesDetView(LoginRequiredMixin, ListView):
    model = LOTE_HIS
    template_name = 'table_lotesDetLista.html'

    def get_queryset(self, **kwargs):

        #lote = self.get('buscaLote')
        #self.object_list = LOTE.objects.filter(lote_lote=lote)
        self.object_list = LOTE_HIS.objects.filter(lohi_lote=self.kwargs['pk'])
        return self.object_list

class LoteInternoView(LoginRequiredMixin, ListView):
    model = LOTE
    template_name = 'table_loteDetalhe.html'

    def get_queryset(self, **kwargs):

        #self.object_list = LOTE.objects.filter(lote_lote=self.kwargs['lote'])
        self.object_list = LOTE.objects.all()
        return self.object_list

class LoteUpdateView(LoginRequiredMixin, UpdateView):
    model = LOTE
    template_name = 'table_loteDetalhe.html'
    fields = ['lote_gerencia', 'lote_al', 'lote_centro', 'lote_elementoPep', 'lote_deposito', 'lote_tipoVenda', 'lote_alienacaoAutorizada', 'lote_superbid', 'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_fase', 'lote_dataSipa', 'lote_dataEnvioLotesLeilao', 'lote_dataSolicitacaoLeilao', 'lote_dataResultadoLeilao', 'lote_ano']
    context_object_name = 'historicoLista'
    # widget= {
    #     'lote_gerencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
    #     'lote_al': forms.TextInput(attrs={'class':'form-control form-control-sm'})
    # }

    def form_valid(self, form):
        lote = LOTE.objects.get(lote_lote=self.kwargs['pk'])
        print(lote.lote_al)
        print(self.request.POST['lote_al'])
        url = super().form_valid(form)
        if(lote.lote_al != self.request.POST['lote_al']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'AL', lote.lote_al, self.request.POST['lote_al'])
        if(lote.lote_gerencia != self.request.POST['lote_gerencia']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Gerência', lote.lote_gerencia.pk, self.request.POST['lote_gerencia'])
        if(lote.lote_centro != self.request.POST['lote_centro']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Centro', lote.lote_centro, self.request.POST['lote_centro'])
        if(lote.lote_elementoPep != self.request.POST['lote_elementoPep']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Elemento PEP', lote.lote_elementoPep, self.request.POST['lote_elementoPep'])
        if(lote.lote_deposito != self.request.POST['lote_deposito']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Depósito', lote.lote_deposito, self.request.POST['lote_deposito'])
        if(lote.lote_alienacaoAutorizada != self.request.POST['lote_alienacaoAutorizada']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Alienação Autorizada', lote.lote_alienacaoAutorizada, self.request.POST['lote_alienacaoAutorizada'])
        if(lote.lote_superbid != self.request.POST['lote_superbid']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Superbid', lote.lote_superbid, self.request.POST['lote_superbid'])
        if(lote.lote_quantidadeFoto != self.request.POST['lote_quantidadeFoto']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Quantidade de Fotos', lote.lote_quantidadeFoto, self.request.POST['lote_quantidadeFoto'])
        if(lote.lote_localArmazenamento != self.request.POST['lote_localArmazenamento']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Local Armazenamento', lote.lote_localArmazenamento, self.request.POST['lote_localArmazenamento'])
        if(lote.lote_fase != self.request.POST['lote_fase']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Fase', lote.lote_fase, self.request.POST['lote_fase'])
        if(lote.lote_dataSipa != self.request.POST['lote_dataSipa']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Data SIPA', lote.lote_dataSipa, self.request.POST['lote_dataSipa'])
        if(lote.lote_dataEnvioLotesLeilao != self.request.POST['lote_dataEnvioLotesLeilao']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Data Envio Lotes Leilão', lote.lote_dataEnvioLotesLeilao, self.request.POST['lote_dataEnvioLotesLeilao'])
        if(lote.lote_dataSolicitacaoLeilao != self.request.POST['lote_dataSolicitacaoLeilao']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Data Solicitação Leilão', lote.lote_dataSolicitacaoLeilao, self.request.POST['lote_dataSolicitacaoLeilao'])
        if(lote.lote_dataResultadoLeilao != self.request.POST['lote_dataResultadoLeilao']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Data Resultado Leilão', lote.lote_dataResultadoLeilao, self.request.POST['lote_dataResultadoLeilao'])
        if(lote.lote_ano != self.request.POST['lote_ano']):
            gravarHistorico('Alteração', self.request.user, lote.lote_lote, 'Ano', lote.lote_ano, self.request.POST['lote_ano'])
        return url

    def get_context_data(self, **kwargs):

        context = super(LoteUpdateView, self).get_context_data(**kwargs)
        historico = HIST_LOTE.objects.filter(hist_lote=self.kwargs['pk'])
        if historico:
            context['historicoLista'] = historico
        else:
            context['historicoLista'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])
        return context

class LoteCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = LOTE
    fields = ['lote_lote', 'lote_gerencia', 'lote_al', 'lote_centro', 'lote_elementoPep', 'lote_deposito', 'lote_tipoVenda', 'lote_alienacaoAutorizada', 'lote_superbid', 'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_fase', 'lote_dataSipa', 'lote_dataEnvioLotesLeilao', 'lote_dataSolicitacaoLeilao', 'lote_dataResultadoLeilao', 'lote_ano']
    template_name = 'form_loteNovo.html'
            
    def form_valid(self, form):
        url = super().form_valid(form)
        gravarHistorico(
            'Novo Lote',
            self.request.user,
            self.request.POST['lote_lote'],
            'Todas',
            '',
            '',
            )
        #success_url = reverse_lazy('lote-interno', kwargs={'pk': self.pk})
        return url

def gravarHistorico(tipoAlteracao, usuario, lote, coluna, anterior, novo):
    historico = HIST_LOTE()
    historico.hist_tipoAlteracao = tipoAlteracao
    historico.hist_user = usuario
    historico.hist_lote = LOTE.objects.get(lote_lote=lote)
    historico.hist_coluna = coluna
    historico.hist_dadoAnterior = anterior
    historico.hist_dadoNovo = novo
    historico.save()

class LoteInternoCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = LOTE_HIS
    fields = ['lohi_material', 'lohi_tipoAvaliacao', 'lohi_quantidadeOriginal', 'lohi_quantidadeRetiradaDip', 'lohi_quantidadeNaoLocalizada', 'lohi_quantidadeAtual', 'lohi_unidade', 'lohi_retirada', 'lohi_valorContabilUnitario', 'lohi_valorContabilTotal', 'lohi_valorReposicaoUnitario', 'lohi_valorTotalReposicao', 'lohi_valorComparacaoVMA', 'lohi_vmaUnitario', 'lohi_vmaTotal']
    template_name = 'form_loteDetNovo.html'

    def form_valid(self, form):
        form.instance.lohi_lote = self.kwargs['lote']
        url = super().form_valid(form)
        return url

class novoFormBusca(forms.Form):
    lote = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),label="Lote:", required=False)
    OPCOES = ((2019, 2019), (2020, 2020), (2021, 2021))
    ano = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm'}),choices=OPCOES)

def LotesBusca(request):

    if request.method=="POST":
        formBuscaLote = novoFormBusca(request.POST)
        if formBuscaLote.is_valid():
            lote = formBuscaLote.cleaned_data["lote"]
            ano = formBuscaLote.cleaned_data["ano"]
            if lote:
                lista = LOTE.objects.filter(lote_lote=lote)
            else:
                lista = LOTE.objects.filter(lote_ano=ano)
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formBusca': formBuscaLote
            })
        else:
            lista = LOTE.objects.all()
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formBusca': formBuscaLote
            })
    else:
        lista = LOTE.objects.all()
        return render(request, 'table_lotesLista.html', {
            'lotes':lista,
            'formBusca':novoFormBusca()
        })


def teste(request):
    teste = "TESTE"
    doc = open(r'C:\Users\Bp6g\Desktop\lotesdet.csv', 'r')
    reader = csv.reader(doc)
    print("teste")

    for i in reader:
        # linha = i.split(";")
        # for b in linha:
        #     print(b)
        print(i)

    return render(request, 'teste.html', {
        "lista" : teste
    })
