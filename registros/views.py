from typing import List
from django.core.checks.messages import ERROR
from django.forms.widgets import RadioSelect
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django import forms
from django.views.generic.edit import CreateView
from datetime import date, datetime
from .models import DISPUTA_ABERTA, GERENCIA, LEILAO, LOTE, LOTE_DET, MATERIAL, TESTES, HIST_LOTE, COMPRADOR
from django.db.models import Q
from django.urls import reverse_lazy
import csv
import xlwt
import locale
import xdrlib
from django.contrib import messages
from django.http import HttpResponse
from itertools import chain

from django.contrib.auth.decorators import login_required


# Create your views here.
class LotesDetalheView(LoginRequiredMixin, ListView):
    model = LOTE
    template_name = 'table_lotesLista.html'

    def get_queryset(self):

        #lote = self.get('buscaLote')
        #self.object_list = LOTE.objects.filter(lote_lote=lote)
        self.object_list = LOTE.objects.all()
        return self.object_list

class DisputaAbertaView(LoginRequiredMixin, ListView):
    model = DISPUTA_ABERTA
    template_name = 'table_disputaAbertaLista.html'

    def get_queryset(self):

        self.object_list = DISPUTA_ABERTA.objects.all()
        return self.object_list

class LotesDetView(LoginRequiredMixin, ListView):
    model = LOTE_DET
    template_name = 'table_lotesDetLista.html'
    context_object_name = 'lote'
    

    def get_queryset(self, **kwargs):

        #lote = self.get('buscaLote')
        #self.object_list = LOTE.objects.filter(lote_lote=lote)
        self.object_list = LOTE_DET.objects.filter(lode_lote=self.kwargs['pk'])
        return self.object_list

    def get_context_data(self, **kwargs):

        context = super(LotesDetView, self).get_context_data(**kwargs)
        context['lote'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])
        return context

class LoteInternoView(LoginRequiredMixin, ListView):
    model = LOTE
    template_name = 'table_loteDetalhe.html'

    def get_queryset(self, **kwargs):

        #self.object_list = LOTE.objects.filter(lote_lote=self.kwargs['lote'])
        self.object_list = LOTE.objects.all()
        return self.object_list

class LoteUpdateView(LoginRequiredMixin, UpdateView):
    model = LOTE
    template_name = 'table_loteUpdate.html'
    fields = ['lote_gerencia', 'lote_proprietario', 'lote_al', 'lote_ano', 'lote_responsavel', 'lote_alienacaoAutorizada', 'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_isaSipa', 'lote_dataSipa', 'lote_tipoVenda', 'lote_leilao', 'lote_isaEnvioArm', 'lote_dataEnvoArm']
    context_object_name = 'historicoLista'

    widget= {
        'lote_dataSipa' : forms.DateInput(format='%d-%m-%Y'),
        'lote_al': forms.TextInput(attrs={'class':'form-control form-control-sm'})
    }

    def form_valid(self, form):
        lote = LOTE.objects.get(lote_lote=self.kwargs['pk'])
        url = super().form_valid(form)
        messages.success(self.request, 'Lote atualizado com sucesso!')

        if(lote.lote_gerencia.pk != int(self.request.POST['lote_gerencia'])):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Gerência', lote.lote_gerencia.pk, self.request.POST['lote_gerencia'])
        if(lote.lote_proprietario != self.request.POST['lote_proprietario']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Proprietario', lote.lote_proprietario, self.request.POST['lote_proprietario'])
        if(lote.lote_al != self.request.POST['lote_al']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'AL', lote.lote_al, self.request.POST['lote_al'])
        if(lote.lote_ano != int(self.request.POST['lote_ano'])):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Ano', lote.lote_ano, self.request.POST['lote_ano'])
        if (lote.lote_responsavel):
            if(lote.lote_responsavel.pk != int(self.request.POST['lote_responsavel'])):
                gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Responsável', lote.lote_responsavel.pk, self.request.POST['lote_responsavel'])        
        if(lote.lote_alienacaoAutorizada != self.request.POST['lote_alienacaoAutorizada']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Alienacao Autorizada', lote.lote_alienacaoAutorizada, self.request.POST['lote_alienacaoAutorizada'])        
        if(lote.lote_quantidadeFoto != int(self.request.POST['lote_quantidadeFoto'])):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Quantidade Fotos', lote.lote_quantidadeFoto, self.request.POST['lote_quantidadeFoto'])        
        if(lote.lote_localArmazenamento != self.request.POST['lote_localArmazenamento']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Local Armazenamento', lote.lote_localArmazenamento, self.request.POST['lote_localArmazenamento'])
        if(lote.lote_isaSipa != self.request.POST['lote_isaSipa']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'ISA SIPA', lote.lote_isaSipa, self.request.POST['lote_isaSipa'])
        if(lote.lote_dataSipa != self.request.POST['lote_dataSipa']):
            if(self.request.POST['lote_dataSipa']):
                gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Data SIPA', lote.lote_dataSipa, self.request.POST['lote_dataSipa'])
        if(lote.lote_tipoVenda != self.request.POST['lote_tipoVenda']):
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Tipo Venda', lote.lote_tipoVenda, self.request.POST['lote_tipoVenda'])
        if(lote.lote_isaEnvioArm != self.request.POST['lote_isaEnvioArm']):
            if(self.request.POST['lote_isaEnvioArm']):
                gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'ISA Envio ARM', lote.lote_isaEnvioArm, self.request.POST['lote_isaEnvioArm'])
        if(lote.lote_dataEnvoArm != self.request.POST['lote_dataEnvoArm']):
            if(self.request.POST['lote_dataSipa']):
                gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Data Envio ARM', lote.lote_dataEnvoArm, self.request.POST['lote_dataEnvoArm'])
        return url

    def get_context_data(self, **kwargs):

        context = super(LoteUpdateView, self).get_context_data(**kwargs)
        historico = HIST_LOTE.objects.filter(hist_lote=self.kwargs['pk']).filter(hist_material__isnull=True)
        if historico:
            context['historicoLista'] = historico
        else:
            context['historicoLista'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])
        return context

class LoteCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = LOTE
    fields = ['lote_lote', 'lote_gerencia', 'lote_proprietario', 'lote_al', 'lote_ano', 'lote_responsavel', 'lote_alienacaoAutorizada', 'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_isaSipa', 'lote_dataSipa', 'lote_tipoVenda', 'lote_leilao', 'lote_isaEnvioArm', 'lote_dataEnvoArm'] 
    template_name = 'form_loteNovo.html'
            
    def form_valid(self, form):
        url = super().form_valid(form)
        messages.success(self.request, 'Lote inserido com sucesso!')
        gravarHistorico(
            'Novo Lote',
            self.request.user,
            self.request.POST['lote_lote'],
            'Todas',
            '',
            '',
            )
        success_url = reverse_lazy('lote-interno', kwargs={'pk': self.pk})
        return url

def gravarHistorico(tipoAlteracao, usuario, lote, material, coluna, anterior, novo):
    historico = HIST_LOTE()
    historico.hist_tipoAlteracao = tipoAlteracao
    historico.hist_user = usuario
    if material:
        historico.hist_lote = LOTE.objects.get(lote_lote=lote)
        historico.hist_material = LOTE_DET.objects.get(pk=material)
    else:
        historico.hist_lote = LOTE.objects.get(lote_lote=lote)

    historico.hist_coluna = coluna
    historico.hist_dadoAnterior = anterior
    historico.hist_dadoNovo = novo
    historico.save()

class LoteDetCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = LOTE_DET
    fields = ['lode_material', 'lode_centroAtual', 'lode_elementoPep', 'lode_deposito', 'lode_tipoAvaliacao', 'lode_loteNm', 'lode_numeroSerie', 'lode_quantidadeOriginal', 'lode_quantidadeRetiradaDip', 'lode_quantidadeNaoLocalizada', 'lode_unidade', 'lode_isaRetirada', 'lode_dataRetirada', 'lode_valorContabilTotal', 'lode_valorTotalReposicao', 'lode_vmaTotal']
    template_name = 'form_loteDetNovo.html'
    context_object_name = 'lote'

    def form_valid(self, form):
        lote = self.kwargs['pk']
        form.instance.lode_lote = LOTE.objects.get(lote_lote=self.kwargs['pk'])
        url = super().form_valid(form)
        messages.success(self.request, 'Material inserido com sucesso!')

        # print(lode.lode_lote)
        #if(lote.lote_gerencia.pk != int(self.request.POST['lote_gerencia'])):
        #    gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Gerência', lote.lote_gerencia.pk, self.request.POST['lote_gerencia'])
        #if(lote.lote_proprietario != self.request.POST['lote_proprietario']):
        #    gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Proprietario', lote.lote_proprietario, self.request.POST['lote_proprietario'])

        return url
    
    def get_success_url(self):
        lote = self.kwargs['pk']
        return reverse_lazy('lotes-det-lista', kwargs={'pk': lote})

    def get_context_data(self, **kwargs):
        context = super(LoteDetCreateView, self).get_context_data(**kwargs)
        context['lote'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])
        return context

class LoteDetUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = LOTE_DET
    fields = ['lode_centroAtual', 'lode_elementoPep', 'lode_deposito', 'lode_tipoAvaliacao', 'lode_loteNm', 'lode_numeroSerie', 'lode_quantidadeOriginal', 'lode_quantidadeRetiradaDip', 'lode_quantidadeNaoLocalizada', 'lode_unidade', 'lode_isaRetirada', 'lode_dataRetirada', 'lode_valorContabilTotal', 'lode_valorTotalReposicao', 'lode_vmaTotal']
    template_name = 'form_loteDetUpdate.html'
    context_object_name = 'historicoDetLista'

    def form_valid(self, form):
        lode = LOTE_DET.objects.get(pk=self.kwargs['pk'])
        url = super().form_valid(form)
        messages.success(self.request, 'Material atualizado com sucesso!')

        if(lode.lode_centroAtual != self.request.POST['lode_centroAtual']):
            if(self.request.POST['lode_centroAtual']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Centro Atual', lode.lode_centroAtual, self.request.POST['lode_centroAtual'])
        if(lode.lode_elementoPep != self.request.POST['lode_elementoPep']):
            if(self.request.POST['lode_elementoPep']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Elemento Pep', lode.lode_elementoPep, self.request.POST['lode_elementoPep'])
        if(lode.lode_deposito != self.request.POST['lode_deposito']):
            if(self.request.POST['lode_deposito']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Deposito', lode.lode_deposito, self.request.POST['lode_deposito'])
        if(lode.lode_tipoAvaliacao != self.request.POST['lode_tipoAvaliacao']):
            if(self.request.POST['lode_tipoAvaliacao']):
                print('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Tipo de Avaliacao', lode.lode_tipoAvaliacao, self.request.POST['lode_tipoAvaliacao'])
        if(lode.lode_loteNm != self.request.POST['lode_loteNm']):
            if(self.request.POST['lode_loteNm']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Lote do NM', lode.lode_loteNm, self.request.POST['lode_loteNm'])
        if(lode.lode_numeroSerie != self.request.POST['lode_numeroSerie']):
            if(self.request.POST['lode_numeroSerie']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Numero de Serie', lode.lode_numeroSerie, self.request.POST['lode_numeroSerie'])
        if(self.request.POST['lode_quantidadeOriginal']):
            if(lode.lode_quantidadeOriginal != float(self.request.POST['lode_quantidadeOriginal'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Quantidade Original', lode.lode_quantidadeOriginal, self.request.POST['lode_quantidadeOriginal'])
        if(self.request.POST['lode_quantidadeRetiradaDip']):
            if(lode.lode_quantidadeRetiradaDip != float(self.request.POST['lode_quantidadeRetiradaDip'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Quantidade Retirada Dip', lode.lode_quantidadeRetiradaDip, self.request.POST['lode_quantidadeRetiradaDip'])
        if(self.request.POST['lode_quantidadeNaoLocalizada']):
            if(lode.lode_quantidadeNaoLocalizada != float(self.request.POST['lode_quantidadeNaoLocalizada'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Quantidade Nao Localizada', lode.lode_quantidadeNaoLocalizada, self.request.POST['lode_quantidadeNaoLocalizada'])
        if(lode.lode_unidade != self.request.POST['lode_unidade']):
            if(self.request.POST['lode_unidade']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Unidade', lode.lode_unidade, self.request.POST['lode_unidade'])
        if(lode.lode_isaRetirada != self.request.POST['lode_isaRetirada']):
            if(self.request.POST['lode_isaRetirada']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'ISA Retirada', lode.lode_isaRetirada, self.request.POST['lode_isaRetirada'])
        if(lode.lode_dataRetirada != self.request.POST['lode_dataRetirada']):
            if(self.request.POST['lode_dataRetirada']):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Data de Retirada', lode.lode_dataRetirada, self.request.POST['lode_dataRetirada'])
        if(self.request.POST['lode_valorContabilTotal']):
            if(lode.lode_valorContabilTotal != float(self.request.POST['lode_valorContabilTotal'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Valor Contabil Total', lode.lode_valorContabilTotal, self.request.POST['lode_valorContabilTotal'])
        if(self.request.POST['lode_valorTotalReposicao']):
            if(lode.lode_valorTotalReposicao != float(self.request.POST['lode_valorTotalReposicao'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'Valor Total Reposicao', lode.lode_valorTotalReposicao, self.request.POST['lode_valorTotalReposicao'])
        if(self.request.POST['lode_vmaTotal']):
            if(lode.lode_vmaTotal != float(self.request.POST['lode_vmaTotal'])):
                gravarHistorico('Alteração do Material', self.request.user, lode.lode_lote, lode.pk, 'VMA Total', lode.lode_vmaTotal, self.request.POST['lode_vmaTotal'])
       
        return url

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('lote-det-editar', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):

        context = super(LoteDetUpdateView, self).get_context_data(**kwargs)
        historico = HIST_LOTE.objects.filter(hist_material=self.kwargs['pk'])
        if historico:
            context['historicoDetLista'] = historico
        else:
            context['historicoDetLista'] = LOTE_DET.objects.filter(pk=self.kwargs['pk'])
        return context

class novoFormBusca(forms.Form):
    lote = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'data-role':'tagsinput'}),label="Lote:", required=False)
    ANO = ((2019, 2019), (2020, 2020), (2021, 2021))
    ano = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm'}),choices=ANO, required=False)
    gerencia = forms.ModelMultipleChoiceField(queryset=GERENCIA.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}))
    PROPRIETARIO = (('Petrobras', 'Petrobras'), ('Consorcio', 'Consorcio'))
    proprietario = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=PROPRIETARIO, required=False)
    al = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'data-role':'tagsinput'}),label="AL:", required=False)
    responsavel = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}))
    AUTORIZADA = (('Autorizada', 'Autorizada'),('Não Autorizado', 'Não Autorizado'))
    alienacaoAutorizada = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=AUTORIZADA, required=False)
    ARMAZEM = (('Macaé - RJ', 'Macaé - RJ'), ('Rio de Janeiro - RJ', 'Rio de Janeiro - RJ'))
    localArmazenamento = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=ARMAZEM, required=False)
    TIPOVENDA = (('Sucateamento','Sucateamento'), ('Vendido', 'Vendido'), ('', ''))
    tipoVenda = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=TIPOVENDA, required=False)
    #lote_leilao
    nm = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'data-role':'tagsinput'}),label="NM:", required=False)

@login_required
def LotesBusca(request):

    if request.method=="POST":
        
        formBuscaLote = novoFormBusca(request.POST)
        if formBuscaLote.is_valid():
            listaFinal = []
            lote = formBuscaLote.cleaned_data["lote"]
            ano = formBuscaLote.cleaned_data["ano"]
            gerencia = formBuscaLote.cleaned_data["gerencia"]
            proprietario = formBuscaLote.cleaned_data["proprietario"]
            al = formBuscaLote.cleaned_data["al"]
            responsavel = formBuscaLote.cleaned_data["responsavel"]
            alienacaoAutorizada = formBuscaLote.cleaned_data["alienacaoAutorizada"]
            localArmazenamento = formBuscaLote.cleaned_data["localArmazenamento"]
            tipoVenda = formBuscaLote.cleaned_data["tipoVenda"]
            nm = formBuscaLote.cleaned_data["nm"]

            lista = LOTE.objects.all()
            if lote:
                lote = lote.split(',')
                query = Q(lote_lote=0)
                for a in lote:
                    query.add(Q(lote_lote=a), Q.OR)
                #    filtros.append(LOTE.objects.filter(lote_lote=a))
                #lista = LOTE.objects.filter(lote_lote=0)
                #for b in filtros:
                #    lista = chain(lista,b)
                lista = LOTE.objects.filter(query)
            if ano:
                lista = lista.filter(lote_ano=ano)
            if gerencia:
                queryB = Q(lote_gerencia=0)
                for gere in gerencia:
                    queryB.add(Q(lote_gerencia=gere.id), Q.OR)
                lista = lista.filter(queryB)
            if proprietario:
                queryC = Q(lote_proprietario="")
                for prop in proprietario:
                    queryC.add(Q(lote_proprietario=prop), Q.OR)
                lista = lista.filter(queryC)
            if al:
                al = al.split(',')
                queryD = Q(lote_al="")
                for b in al:
                    queryD.add(Q(lote_al__iexact=b), Q.OR)
                lista = lista.filter(queryD)
            if responsavel:
                queryE = Q(lote_responsavel=0)
                for resp in responsavel:
                    queryE.add(Q(lote_responsavel=resp.id), Q.OR)
                lista = lista.filter(queryE)
            if alienacaoAutorizada:
                queryF = Q(lote_alienacaoAutorizada="a")
                for auto in alienacaoAutorizada:
                    queryF.add(Q(lote_alienacaoAutorizada=auto), Q.OR)
                lista = lista.filter(queryF)
            if localArmazenamento:
                queryG = Q(lote_localArmazenamento="a")
                for armazem in localArmazenamento:
                    queryG.add(Q(lote_localArmazenamento=armazem), Q.OR)
                lista = lista.filter(queryG)
            if tipoVenda:
                queryH = Q(lote_tipoVenda="a")
                for tipo in tipoVenda:
                    queryH.add(Q(lote_tipoVenda=tipo), Q.OR)
                lista = lista.filter(queryH)
            if nm:
                nm = nm.split(',')
                for a in nm:
                 
                    material = MATERIAL.objects.get(mate_cod=a)  
                    lode = LOTE_DET.objects.get(lode_material=material) 
                    lista = LOTE.objects.filter(lote_lote = lode.lode_lote)
                    

            valorContabil = 0
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            for lotes in lista:
                lodes = LOTE_DET.objects.filter(lode_lote=lotes.lote_lote)
                valorVMA=0
                for lode in lodes:
                    valorContabil = valorContabil + lode.lode_valorContabilTotal
                    valorVMA = valorVMA + lode.lode_vmaTotal

                    #lode.lode_vmaPercentualLote = round(100* lode.lode_vmaTotal / lotes.lote_vmaLote, 2)
                    #print(lode.lode_vmaPercentualLote)
                    #lode.save()
                
                #if not(lotes.lote_vmaLote):
                #lotes.lote_vmaLote = valorVMA
                #lotes.save()
                #print(valorVMA)

            valorContabil = locale.currency(valorContabil, grouping=True)
            #round(valorContabil, 2)
                
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'valorContabil':valorContabil,
                'formBusca': formBuscaLote,
                'formBuscaB': formBuscaLote
            })
        else:
            lista = None
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formBusca': formBuscaLote
            })
    else:
        lista = None
        return render(request, 'table_lotesLista.html', {
            'lotes':lista,
            'formBusca':novoFormBusca()
        })

class formUpload(forms.Form):
    #upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control form-control-sm'}),label="Upload:")
    frmUpload = forms.FileField(label="Teste")

@login_required
def LotesUpload(request):

    if request.method=="POST":
        form = formUpload(request.POST, request.FILES)
        if form.is_valid():

            log = open('C:\\Users\\bp6g\\logPainelSAM.csv', 'w', newline='', encoding='utf-8')
            
            upload = request.FILES['frmUpload'].read().decode('latin-1').splitlines()
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            listaErros = []
            erro = ''
            linha = 0
            next(reader)
            for dadosLinha in reader:

                #Inserir dados até a linha: 
                if linha<30000:
                    print(linha+2)
                    #Estrutura de Lotes
                    if(dadosLinha[2]):
                        numero_lote = ''
                        try: numero_lote = LOTE.objects.get(lote_lote = dadosLinha[2]) 
                        except:
                            #print(linha)
                            #print('----------------')
                            #print(dadosLinha[2])
                            #print("O lote não existe, criando um novo...")
                            a = 1

                        if numero_lote:
                            #print(' O lote já existe! Inserindo um lote detalhe...')
                            #inserir_lote-det(i)
                            erro = inserirLoteDetalhe(dadosLinha)
                            if erro:
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n')
                                #messages.warning(request, 'Erro na linha: '+str(linha+2)+'. '+erro)
                            # else:
                            #     log.write('Linha:'+str(linha+2)+' - Lote e Detalhe inseridos\n')
                        else:
                            erro = inserirLote(dadosLinha)
                            if erro:
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n')
                                #messages.warning(request, 'Erro na linha: '+str(linha+2)+'. '+erro)
                                #sair de um looping
                            else:
                                erroB = inserirLoteDetalhe(dadosLinha)
                                if erroB:
                                    log.write('Somente o lote foi inserido. Erro na linha: '+str(linha+2)+'. '+erroB+'\n')
                                    #messages.warning(request, 'Erro na linha: '+str(linha+2)+'. '+erroB)
                                # else:
                                #     log.write('Linha:'+str(linha+2)+' - Lote e Detalhe inseridos\n')
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote é obrigatório. Verifique se está vazio ou incorreto!\n')
                        #messages.warning(request, 'Erro na linha: '+str(linha+2)+'. Campo lote é obrigatório. Verifique se está vazio ou incorreto!')

                linha+=1

            log.close()

            return render(request, 'table_lotesLista.html', {
                'lotes':listaLotes,
                'formUpload': form
            })
        else:
            
            upload = request.POST['frmUpload']
            print(upload)
            print('TESTEEEEEBBBBBBB     TESTEEEEEEEEEEEE')
            lista = None
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formUpload': form
            })
    else:
        lista = None
        print('TESTEEEEECCCCCCCCC     TESTEEEEEEEEEEEE')
        return render(request, 'table_lotesLista.html', {
            'lotes':lista,
            'formUpload':formUpload()
        })

def inserirLote(i):
    lote = LOTE()
    lote.lote_lote = i[2]
    lote.lote_ano = 2021

    if i[0]:
        lote.lote_proprietario = i[0]
    # else:
    #     lote.lote_proprietario = 'Petrobras'
    #     print('O campo Proprietario está vazio, foi inserido Petrobras como Padrão')
    
    if (inserirGerencia(i[1]) == True):
        lote.lote_gerencia = GERENCIA.objects.get(gere_nome = i[1])
    else: return ('Campo Gerência é obrigatório. Verifique se está vazio ou incorreto!')
    
    if i[3]:
        lote.lote_al = i[3]
    else: return ('Campo AL é obrigatório. Verifique se está vazio ou incorreto!')

    if i[19]:
        if i[19] in ('Autorizada', 'Não Autorizado'):
            lote.lote_alienacaoAutorizada = i[19]
        else: return ('Campo Alienção Autorizada deve conter somente Autorizada ou Não Autorizado')
    else: return ('Campo Alienação Autorizada é obrigatório. Verifique se está vazio ou incorreto!')
    
    if i[22]:
        if i[22].isnumeric():
            lote.lote_quantidadeFoto = i[22]
        else: return ('Campo Quantidade de Fotos deve ter um valor numérico')
    else: lote.lote_quantidadeFoto = 0

    lote.lote_localArmazenamento = i[28]
    lote.lote_isaSipa = i[29]
    
    if i[30]:
        try:
            lote.lote_dataSipa = datetime.strptime(i[30], '%d/%m/%Y').date()
        except: return ('Campo Data SIPA não está no padrão de data (dd/mm/aaaa)')

    lote.lote_tipoVenda = i[31]
    # Leilão foi realizado? - calculado

    try:
        lote.save()
    except Exception as e:
        print('Erro ao salvar o lote.')
        print('%s' % (type(e)))
        return ('Erro ao salvar o lote')

def inserirGerencia(gerenciaCampo):
                   
    #Estrutura da Gerência
    if gerenciaCampo:
        nome_gerencia = ''
        try: nome_gerencia = GERENCIA.objects.get(gere_nome = gerenciaCampo) 
        except: a=0 #print('Gerência não Existe, vou inserir uma nova')
        if nome_gerencia:
            #print('Já existe a gerência')
            return True
        else:
            gerencia = GERENCIA()
            gerencia.gere_nome = gerenciaCampo
            gerencia.gere_grupo = 0
            gerencia.save()
            #print('Gerencia nova criada')
            return True
    else:
        return False

def inserirLoteDetalhe(i):

    #Estrutura de lote detalhe
    loteDetalhe = LOTE_DET()
    loteDetalhe.lode_lote = LOTE.objects.get(lote_lote = i[2])

    if (inserirMaterial(i[4], i[5], i[6], i[7]) == True):
        loteDetalhe.lode_material = MATERIAL.objects.get(mate_cod = i[4])
    else: return ('Campo Material é obrigatório. Verifique se está vazio ou incorreto!') #reinserir l356 vg
    
    loteDetalhe.lode_centroAtual = i[8]
    loteDetalhe.lode_elementoPep = i[9]
    loteDetalhe.lode_deposito = i[10]
    loteDetalhe.lode_tipoAvaliacao = i[11]
    loteDetalhe.lode_loteNm = i[12]
    loteDetalhe.lode_numeroSerie = i[13]
    if i[14]:
        try:
            loteDetalhe.lode_quantidadeOriginal = float(i[14].replace(',','.'))
        except: return ('Campo Quantidade Original deve ter um valor do tipo real')  
    else: loteDetalhe.lode_quantidadeOriginal = 0

    if i[15]:
        try:
            loteDetalhe.lode_quantidadeRetiradaDip = float(i[15].replace(',','.'))
        except: return ('Campo Quantidade Retirada DIP deve ter um valor do tipo real')  
    else: loteDetalhe.lode_quantidadeRetiradaDip = 0

    if i[16]:
        try:
            loteDetalhe.lode_quantidadeNaoLocalizada = float(i[16].replace(',','.'))
        except: return ('Campo Quantidade Não Localizada deve ter um valor do tipo real')  
    else: loteDetalhe.lode_quantidadeNaoLocalizada = 0

    if i[17]:
        try:
            loteDetalhe.lode_quantidadeAtual = float(i[17].replace(',','.'))
        except: return ('Campo Quantidade Atual deve ter um valor do tipo real')  
    else: loteDetalhe.lode_quantidadeAtual = 0
    
    loteDetalhe.lode_unidade = i[18]

    loteDetalhe.lode_isaRetirada = i[20]

    if i[21]:
        try:
            loteDetalhe.lode_dataRetirada = datetime.strptime(i[21], '%d/%m/%Y').date()
        except: return ('Campo Data Retirada não está no padrão de data (dd/mm/aaaa)')

    if i[23]:
        try:
            loteDetalhe.lode_valorContabilTotal = float(i[23].replace(',','.'))
        except: return ('Campo Valor Contabil Total deve ter um valor do tipo real')
    else: loteDetalhe.lode_valorContabilTotal = 0

    # COLUNA CALCULADA
    # if i[24]:
    #     try:
    #         loteDetalhe.lode_valorReposicaoUnitario = float(i[24].replace(',','.'))
    #     except: return ('Campo Valor de Reposição Unitario deve ter um valor do tipo real')
    # else: loteDetalhe.lode_valorReposicaoUnitario = 0

    if i[25]:
        try:
            loteDetalhe.lode_valorTotalReposicao = float(i[25].replace(',','.'))
        except: return ('Campo Valor Total de Reposição deve ter um valor do tipo real')  
    else: loteDetalhe.lode_valorTotalReposicao = 0

    # if i[27]:
    #     #CALCULADO
    #     lote.lote_valorComparacaoVMA = float(i[27].replace(',','.'))
    # else: lote.lote_valorComparacaoVMA = 0

    # CALCULADA VER MODELS
    # if i[26]:
    #     try:
    #         loteDetalhe.lode_vmaUnitario = float(i[26].replace(',','.'))
    #     except: return ('Campo VMA Unitario deve ter um valor do tipo real')  
    # else: loteDetalhe.lode_vmaUnitario = 0

    if i[27]:
        try:
            loteDetalhe.lode_vmaTotal = float(i[27].replace(',','.'))
        except: return ('Campo VMA Total deve ter um valor do tipo real') 
    else: loteDetalhe.lode_vmaTotal = 0

    try:
        loteDetalhe.save()
    except Exception as e:
        print('Erro ao salvar o detalhe do lote.')
        print('%s' % (type(e)))
        return ('Erro ao salvar o detalhe do lote')


def inserirMaterial(material, descr, ncm, gm):

    #Estrutura de Material
    if material:
        nm_material = ''
        try: nm_material = MATERIAL.objects.get(mate_cod = material) 
        except: a=1 #print('Material não Existe, vou inserir um novo')
        if nm_material:
            #print('Já existe o material')
            return True
        else:
            mate = MATERIAL()
            mate.mate_cod = material
            mate.mate_descricao = descr
            mate.mate_ncm = ncm
            mate.mate_grupoMercadoria = gm
            mate.save()
            #print('Material novo criado')
            return True
    else:
        return False

class novoFormLeilao(forms.Form):
    frmLeilaoUpload = forms.FileField(label="Teste", required=False)
    nome = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),label="Leilão:", required=False)
    data = forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control form-control-sm'}),label="Data do Leilão:", required=False)

@login_required
def LeilaoUpload(request):

    if request.method=="POST":
        form = novoFormLeilao(request.POST, request.FILES)
        if form.is_valid():

            log = open('C:\\Users\\BP6G\\logLeiloesPainelSAM.csv', 'w', newline='', encoding='utf-8')
            
            #upload = request.FILES['frmLeilaoUpload'].read().decode('latin-1').splitlines()
            upload = ""
            nome = request.POST['nome']
            data = request.POST['data']
            
            
            leilao = LEILAO()  
            leilao.leil_nome = nome
            leilao.leil_dataResultadoLeilao = datetime.strptime(data, '%d/%m/%Y').date()
            try:
                leilao.save()
            except Exception as e:
                print('Erro ao salvar o leilao.')
                print('%s' % (type(e)))
                return ('Erro ao salvar o leilao')
            #CRIO um novo leilao e insiro o nome e data na tabela
            
            upload = request.FILES['frmLeilaoUpload'].read().decode('latin-1').splitlines()
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            erro = ''
            linha = 0
            next(reader)

            #for para ler a planilha
            for dadosLinha in reader:

                #Inserir dados até a linha: 
                if linha<30000:
                    print(linha+2)
                    #Estrutura de Lotes

                    if(dadosLinha[0]):
                        numero_lote = ''
                        try: numero_lote = LOTE.objects.get(lote_lote = dadosLinha[0]) 
                        except:
                            a = 1

                        if numero_lote:
                            # Existindo o lote da planilha la no banco

                            # Insere na tabela LOTE os dados do Leilão e atualiza as colunas de tipo de venda

                            # Verifica se o comprador ja existe
                           
                            if (inserirComprador(dadosLinha[1], dadosLinha[2], dadosLinha[3], dadosLinha[4], dadosLinha[5], dadosLinha[6], dadosLinha[7], dadosLinha[8], dadosLinha[10]) == True):
                                #disputaabertadirate.dispi_comprador = COMPRADOR.objects.get(comp_cnpj = dadosLinha[1])
                                a = 1
                            else: return ('Campo Comprador é obrigatório. Verifique se está vazio ou incorreto!') #reinserir l356 vg

                            # Se existir, insere na disputa aberta o Numero do Lote, o Num Leilão, o Num do Comprador e os valores
                            # Se não existir, insere um novo comprador com os dados da planilha, depois insere os mesmos dados acima        
                            
                            numero_lote.lote_leilao = leilao
                            numero_lote.lote_tipoVenda = "Vendido"
                            numero_lote.save()

                            #FAZER VALIDCAO PARA NAO INSERIR MESMO LOTE 2 vezes
                            disputaAberta = DISPUTA_ABERTA()
                            disputaAberta.diab_lote = numero_lote
                            disputaAberta.diab_comprador = COMPRADOR.objects.get(comp_cnpj = dadosLinha[1])
                            try:
                                disputaAberta.diab_lanceTotal = float(dadosLinha[9].replace(',','.'))
                            except:
                                log.write('Erro na linha: '+str(linha+2)+'. O valor do lance não foi inserido. Não é númeral. \n')

                            disputaAberta.save()
                            #print(' O lote já existe! Inserindo um leilao...')
                            #erro = inserirLeilao(dadosLinha)
                            #    -> erro = inserirLeilao(dadosLinha)
                            #    -> ligar leilao ao lote
                            if erro:
                                # ERRO AO INSERIR O LEILAO
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n')
                            
                        else: 
                            log.write('Erro na linha: '+str(linha+2)+'. O LOTE NAO FOI ENCONTRADO NO BD \n')
                            
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote é obrigatório. Verifique se está vazio ou incorreto!\n')

                linha+=1

            log.close()

            return render(request, 'form_leilaoNovo.html', {
                'lotes':listaLotes,
                'novoFormLeilao': form
            })
        else:
            
            upload = request.POST['novoFormLeilao']
            lista = None
            return render(request, 'form_leilaoNovo.html', {
                'lotes':lista,
                'novoFormLeilao': form
            })
    else:
        lista = None
        return render(request, 'form_leilaoNovo.html', {
            'lotes':lista,
            'novoFormLeilao':novoFormLeilao()
        })

def inserirComprador(cnpj, nomeComp, telefoneRes, telefoneCom, celular, cidade, estado, endereco, email):

    #Estrutura de Material
    if cnpj:
        comprador = ''
        try: comprador = COMPRADOR.objects.get(comp_cnpj = cnpj) 
        except: a=1 #print('Material não Existe, vou inserir um novo')
        if comprador:
            #print('Já existe o comprador')
            return True
        else:
            comp = COMPRADOR()
            comp.comp_cnpj = cnpj
            comp.comp_nomeComprador = nomeComp
            comp.comp_telefoneResidencial = telefoneRes
            comp.comp_telefoneComercial = telefoneCom
            comp.comp_celular = celular
            comp.comp_cidade = cidade
            comp.comp_estado = estado
            comp.comp_endereco = endereco
            comp.comp_email = email
            comp.save()
            #print('Comprador novo criado')
            return True
    else:
        return False    
        
    #- Desenvolver visões de listas gerenciais
    #- Inserção de leilões em massa por csv (Testes Finais)
    #- Popular tabela de disputa aberta
    #- Somatório de Valores nas consultas totais (Pronto, apenas ajustar layout)
    #- Sistema de sessões para usuários 
    #- Sistema de login com níveis de prioridade
    #- Limpar código e subir para gitlab petrobras
    #- Validações das entradas de texto

@login_required
def ListaGerencial(request):

    listaGerencial = []
    a = 0
    lista = LOTE.objects.filter(lote_ano=2021).values("lote_isaSipa", "lote_dataSipa")
    [listaGerencial.append(i) for i in lista if not listaGerencial.count(i)]
    listaFinal = []
    valorContabilTotal = 0
    for c in listaGerencial:
        qtdLotes=0
        qtdLeilao=0
        qtdSucatas=0
        qtdVendidos=0
        valorContTotal=0
        valorLeilao=0
        valorSucata=0
        for lotes in LOTE.objects.filter(lote_isaSipa = c['lote_isaSipa']):
            gerencia = lotes.lote_gerencia
            proprietario = lotes.lote_proprietario

            lodes = LOTE_DET.objects.filter(lode_lote=lotes.lote_lote)
            valorCont=0
            for lode in lodes:
                valorCont = valorCont + lode.lode_valorContabilTotal
                valorContTotal = valorContTotal + valorCont

            if(lotes.lote_leilao):
                qtdLeilao+=1
                valorLeilao = valorLeilao + valorCont
            if(lotes.lote_tipoVenda == 'Sucateamento'):
                qtdSucatas+=1
                valorSucata = valorSucata + valorCont
            if(lotes.lote_tipoVenda == 'Vendido'):
                qtdVendidos+=1
            qtdLotes+=1
        c['qtdLotes'] = qtdLotes
        c['gerencia'] = gerencia
        c['proprietario'] = proprietario
        c['qtdLeilao'] = qtdLeilao
        c['qtdSucatas'] = qtdSucatas
        c['qtdVendidos'] = qtdVendidos
        c['valorCont'] = round(valorContTotal, 2)
        c['valorLeilao'] = round(valorLeilao, 2)
        c['valorSucata'] = round(valorSucata, 2)
        listaFinal.append(c)
        #print(listaFinal['isaSipa'])
        #listaFinal['dataSipa'] = c['lote_dataSipa']
        #print(listaFinal[a].dataSipa)
        #b=0
        #for lotes in LOTE.objects.filter(lote_isaSipa = c['lote_isaSipa']):
        #    b+=1
        #listaFinal['qtdLotes'] = b  
        #print(listaFinal[a].qtdLotes)
        a+=1
        valorContabilTotal = valorContabilTotal + valorContTotal
    
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valorContabilTotal = locale.currency(valorContabilTotal, grouping=True)

    return render(request, 'table_gerencial.html', {
            'lista':listaFinal,
            'valorTotal':valorContabilTotal,
            'novoFormLeilao':novoFormLeilao()})


def export(request):

    if request.method=="POST":
        
        formBuscaLote = novoFormBusca(request.POST)
        if formBuscaLote.is_valid():
            listaFinal = []
            lote = formBuscaLote.cleaned_data["lote"]
            ano = formBuscaLote.cleaned_data["ano"]
            gerencia = formBuscaLote.cleaned_data["gerencia"]
            proprietario = formBuscaLote.cleaned_data["proprietario"]
            al = formBuscaLote.cleaned_data["al"]
            responsavel = formBuscaLote.cleaned_data["responsavel"]
            alienacaoAutorizada = formBuscaLote.cleaned_data["alienacaoAutorizada"]
            localArmazenamento = formBuscaLote.cleaned_data["localArmazenamento"]
            tipoVenda = formBuscaLote.cleaned_data["tipoVenda"]
            nm = formBuscaLote.cleaned_data["nm"]

            lista = LOTE.objects.all()
            if lote:
                lote = lote.split(',')
                query = Q(lote_lote=0)
                for a in lote:
                    query.add(Q(lote_lote=a), Q.OR)
                #    filtros.append(LOTE.objects.filter(lote_lote=a))
                #lista = LOTE.objects.filter(lote_lote=0)
                #for b in filtros:
                #    lista = chain(lista,b)
                lista = LOTE.objects.filter(query)
            if ano:
                lista = lista.filter(lote_ano=ano)
            if gerencia:
                queryB = Q(lote_gerencia=0)
                for gere in gerencia:
                    queryB.add(Q(lote_gerencia=gere.id), Q.OR)
                lista = lista.filter(queryB)
            if proprietario:
                queryC = Q(lote_proprietario="")
                for prop in proprietario:
                    queryC.add(Q(lote_proprietario=prop), Q.OR)
                lista = lista.filter(queryC)
            if al:
                al = al.split(',')
                queryD = Q(lote_al="")
                for b in al:
                    queryD.add(Q(lote_al__iexact=b), Q.OR)
                lista = lista.filter(queryD)
            if responsavel:
                queryE = Q(lote_responsavel=0)
                for resp in responsavel:
                    queryE.add(Q(lote_responsavel=resp.id), Q.OR)
                lista = lista.filter(queryE)
            if alienacaoAutorizada:
                queryF = Q(lote_alienacaoAutorizada="a")
                for auto in alienacaoAutorizada:
                    queryF.add(Q(lote_alienacaoAutorizada=auto), Q.OR)
                lista = lista.filter(queryF)
            if localArmazenamento:
                queryG = Q(lote_localArmazenamento="a")
                for armazem in localArmazenamento:
                    queryG.add(Q(lote_localArmazenamento=armazem), Q.OR)
                lista = lista.filter(queryG)
            if tipoVenda:
                queryH = Q(lote_tipoVenda="a")
                for tipo in tipoVenda:
                    queryH.add(Q(lote_tipoVenda=tipo), Q.OR)
                lista = lista.filter(queryH)
            if nm:
                nm = nm.split(',')
                for a in nm:
                 
                    material = MATERIAL.objects.get(mate_cod=a)  
                    lode = LOTE_DET.objects.get(lode_material=material) 
                    lista = LOTE.objects.filter(lote_lote = lode.lode_lote)

    listaB = LOTE_DET.objects.all()
    queryM = Q(lode_lote=0)
    for lotes in lista:
        queryM.add(Q(lode_lote=lotes.lote_lote), Q.OR)
    listaB = LOTE_DET.objects.filter(queryM)
          
    response = HttpResponse(content_type='application/ms-excel')

    response['Content-Disposition'] = 'attachment; filename="export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lotes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    #columns = ['Lotes', 'Gerencia', 'Proprietario', 'AL', 'Ano', 
    #    'Responsavel', 'Alienacao Autorizada?', 'Quantidade de Fotos', 
    #    'Local Armazenamento', 'ISA Sipa', 'Data Sipa', 'Tipo de Venda',
    #    'Leilao', 'ISA Envio ARM', 'Data de Envio ARM', 'VMA Total Lote']

    columns = ['Lote', 'Gerencia', 'Proprietario', 'AL', 'Ano', 'Responsavel', 'Alienacao Autorizada?', 
            'Quantidade de Fotos', 'Local Armazenamento', 'ISA Sipa', 'Data Sipa', 'Tipo de Venda', 'Leilao', 
            'ISA Envio ARM', 'Data de Envio ARM', 'VMA Total Lote', 'Material NM', 'Material Descrição', 
            'Material NCM', 'Material GM', 'Centro Atual', 'Elemento PEP', 'Depósito', 
            'Tipo de Avaliação', 'Lote NM', 'Número de Série', 'Quantidade Original', 'Quantidade Retirada DIP',
            'Quantidade Não Localizada', 'Quantidade Atual', 'Unidade', 'ISA de Retirada', 'Data de Retirada', 
            'Valor Contábil Unitário', 'Valor Contábil Total', 'Valor Contábil Total Atual', 'Valor Reposição Unitário',
            'Valor Total Reposição', 'Valor Comparação VMA', 'VMA Unitário', 'VMA Total', 'VMA Percentual do Lote']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = lista.values_list('lote_lote', 'lote_gerencia__gere_nome', 'lote_proprietario', 
    #    'lote_al', 'lote_ano', 'lote_responsavel__username', 'lote_alienacaoAutorizada', 
    #    'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_isaSipa', 'lote_dataSipa', 
    #    'lote_tipoVenda', 'lote_leilao__leil_nome', 'lote_isaEnvioArm', 'lote_dataEnvoArm', 'lote_vmaLote')

    rows = listaB.values_list('lode_lote', 'lode_lote__lote_gerencia__gere_nome', 'lode_lote__lote_proprietario', 
        'lode_lote__lote_al', 'lode_lote__lote_ano', 'lode_lote__lote_responsavel__username', 
        'lode_lote__lote_alienacaoAutorizada', 'lode_lote__lote_quantidadeFoto', 'lode_lote__lote_localArmazenamento', 
        'lode_lote__lote_isaSipa', 'lode_lote__lote_dataSipa', 'lode_lote__lote_tipoVenda', 
        'lode_lote__lote_leilao__leil_nome', 'lode_lote__lote_isaEnvioArm', 'lode_lote__lote_dataEnvoArm', 
        'lode_lote__lote_vmaLote', 'lode_material__mate_cod', 'lode_material__mate_descricao', 
        'lode_material__mate_ncm', 'lode_material__mate_grupoMercadoria', 'lode_centroAtual', 'lode_elementoPep', 
        'lode_deposito', 'lode_tipoAvaliacao', 'lode_loteNm', 'lode_numeroSerie', 'lode_quantidadeOriginal', 
        'lode_quantidadeRetiradaDip', 'lode_quantidadeNaoLocalizada', 'lode_quantidadeAtual', 'lode_unidade', 
        'lode_isaRetirada', 'lode_dataRetirada', 'lode_valorContabilUnitario', 'lode_valorContabilTotal', 
        'lode_valorContabilTotalAtual', 'lode_valorReposicaoUnitario', 'lode_valorTotalReposicao', 
        'lode_valorComparacaoVMA', 'lode_vmaUnitario', 'lode_vmaTotal', 'lode_vmaPercentualLote')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def inserirLotesCsv(lista):
    for i in lista:
        print(i)


def teste(request):
    teste = "TESTE"
    doc = open(r'C:\Users\Bp6g\Desktop\lotesdet.csv', 'r', newline='')
    reader = csv.reader(doc, delimiter=';', quotechar='|')
    print("teste")

    #for i in reader:
    #    #linha = i[0].split(";")
    #    for b in i:
    #        print(b)
    #    
    #    print("--------------------------------")

    return render(request, 'teste.html', {
        "lista" : reader
    })