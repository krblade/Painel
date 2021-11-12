from typing import List
from django.db.models.query_utils import select_related_descend
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.db import connection, reset_queries
from django.contrib import messages
from django.views import generic
from django.core.checks.messages import ERROR
from django.forms.widgets import RadioSelect
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path, include
from .views import *
from django import forms
from django.views.generic.edit import CreateView
from datetime import date, datetime
from pandas.core import indexing
from pandas.core.indexes.base import Index
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
from django.contrib.auth.forms import UserCreationForm #importando o Formulario de Criação de usuario do Django
from django.contrib.auth.decorators import login_required
import pandas as pd
from itertools import chain
import time
import numpy as np

# Create your views here.





class DisputaAbertaView(LoginRequiredMixin, ListView):    # Essa é a view da lista de Disputa Aberta. É uma view generica do Django, uma listview super simples
    model = DISPUTA_ABERTA     # Defino o model que ela puxa 
    template_name = 'table_disputaAbertaLista.html'     # defino o template que ela utiliza
    

    def get_queryset(self):    # monto a query, isso não seria necessário agora, mas futuramente vai ser, até porque se colocar qualquer filtro, tem que ser aqui
        start_time = time.time()
        self.object_list = DISPUTA_ABERTA.objects.all()    # Busco todos os dados de disputa aberta direta
        
        end_time=time.time()
        duration=(end_time - start_time)
        print(f'Executou um total de {len(connection.queries)}Queries')
        print(f'Tempo de Execuçao {round(duration, 3)}Segundos')
        reset_queries()
        return self.object_list     # Retorno a lista para o template
        
      
class LotesDetView(LoginRequiredMixin, ListView):     # Essa é a view para visualizar a lista de materiais de um determinado lote
    # ESSA É MAIS UMA VIEW GENERICA DO PROPRIO DJANGO
    model = LOTE_DET     # Nela usamos como model a tabela LOTE_DET
    template_name = 'table_lotesDetLista.html'     # Definimos o respectivo template
    context_object_name = 'lote'     # Enviamos uma variável que precisaremos para montar os links de edição
    

    def get_queryset(self, **kwargs):    # Nesse caso precisamos utilizar o get_queryset obrigatóriamente, pois não busco todos os dados da tabela e sim dados de acordo com um determinado filtro

        self.object_list = LOTE_DET.objects.filter(lode_lote=self.kwargs['pk'])   # A lista de objetos que vou retornar para o template é uma lista de LOTE_DET onde a coluna lode_lote = ao argumento passado, no caso PK
        return self.object_list    # Retorno a lista de objetos

    def get_context_data(self, **kwargs):     # Esse get context serve para enviar algumas variáveis que utilizarei para criar links 

        context = super(LotesDetView, self).get_context_data(**kwargs)
        context['lote'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])
        return context    # Retorno na variável context o número do lote também para o template

class LoteInternoView(LoginRequiredMixin, ListView):# Essa view retornar LOTE.objects para 'table_loteDetalhe.html'
    model = LOTE
    template_name = 'table_loteDetalhe.html'

    def get_queryset(self, **kwargs):

        #self.object_list = LOTE.objects.filter(lote_lote=self.kwargs['lote'])
        self.object_list = LOTE.objects.all()
        return self.object_list

class LoteUpdateView(LoginRequiredMixin, UpdateView): # Essa view é uma view já modelada pelo Django, eu passo de parametros ali o requerimento par aque o user esteja logado e o tipo dessa view, no caso uma UpdateView
    model = LOTE   # O modelo de updateView do django preciso definir o objeto que ela vai utilizar, no caso o objteo LOTE
    template_name = 'table_loteUpdate.html'    # Defino o template html
    fields = ['lote_gerencia', 'lote_proprietario', 'lote_al', 'lote_ano', 'lote_responsavel', 'lote_alienacaoAutorizada', 'lote_quantidadeFoto', 'lote_localArmazenamento', 'lote_isaSipa', 'lote_dataSipa', 'lote_tipoVenda', 'lote_leilao', 'lote_isaEnvioArm', 'lote_dataEnvoArm']
    # como é uma view de edição, eu preciso definir os campos do objeto que quero permitir que sejam alterados
    context_object_name = 'historicoLista' # já o context_object_name é uma lista que desejo retornar para a tela
## editando aqui
    widget= {
        'lote_dataSipa' : forms.DateInput(format='%d-%m-%Y'),
        'lote_al': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
        'tipoVenda' : forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),required=False)
    }  # nesse widget eu posso desenhar o formulário que eu quero jogar para a tela, serve para atribuir class em css e outros coisas relativas ao layout, quando você estiver trabalhando nas melhorias do layout, vale a pena usar

    def form_valid(self, form):   # Como a view é uma premodulada do Django, mas eu preciso fazer algumas outras operações, eu uso essa classe para pegar os valores do formulário
        lote = LOTE.objects.get(lote_lote=self.kwargs['pk'])   # lote recebe o lote que foi passado por argumento na url, no caso a pk
        url = super().form_valid(form)
        messages.success(self.request, 'Lote atualizado com sucesso!')   # após validar a alteração, a validação é automática, ele envia essa msg de sucesso

        #Abaixo começa a parte de salvar o histórico
        if(lote.lote_gerencia.pk != int(self.request.POST['lote_gerencia'])):  # Se a gerencia do lote for diferente do que foi colocado no formulario, significa que teve uma alteração na gerência, então precisamos armazenar isso no historico de alterações
            gravarHistorico('Alteração do Lote', self.request.user, lote.lote_lote,'', 'Gerência', lote.lote_gerencia.pk, self.request.POST['lote_gerencia'])
            # esse gravarHistorico faz isso, ela salva na tabela historico, o tipo de alteração, o usuário que fez a alt, o número do lote, nesse momento fica vazio aqui pois é uma alteração no lote somente, o dado anterior e o dado novo alterado.
        if(lote.lote_proprietario != self.request.POST['lote_proprietario']):  # e o mesmo se refere a todas as alterações que o usuário fez no lote
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

    def get_context_data(self, **kwargs):   # após graver o histórico de alterações, carregamos uma lista para a tela com o histórico de alterações naquele determinado lote

        context = super(LoteUpdateView, self).get_context_data(**kwargs)
        historico = HIST_LOTE.objects.filter(hist_lote=self.kwargs['pk']).filter(hist_material__isnull=True)    # a tabela historico é filtrada de acordo pela chave primaria do lote
        if historico:   # Se já tiver ocorrido alteração naquele lote
            context['historicoLista'] = historico     # historicoLista recebe a lista de alterações da tabela historico
        else:    # caso não
            context['historicoLista'] = LOTE.objects.filter(lote_lote=self.kwargs['pk'])   # ele retonra a lista de lotes 
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

def gravarHistorico(tipoAlteracao, usuario, lote, material, coluna, anterior, novo):  # Essa classe que grava as alterações que o user pode fazer tanto no lote quanto no lote_det
    historico = HIST_LOTE()
    historico.hist_tipoAlteracao = tipoAlteracao
    historico.hist_user = usuario
    if material:   # Se tiver passado o material, significa que foi uma alteração no material do lote, no lote_det
        historico.hist_lote = LOTE.objects.get(lote_lote=lote)
        historico.hist_material = LOTE_DET.objects.get(pk=material)
    else:   # Se não, foi uma alteração no lote 
        historico.hist_lote = LOTE.objects.get(lote_lote=lote)

    historico.hist_coluna = coluna
    historico.hist_dadoAnterior = anterior
    historico.hist_dadoNovo = novo
    historico.save()   # Salva os valores de alteração e retorna para o update, seja de lote ou de lote_det

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

class novoFormBusca(forms.Form): #Classe que cria os parametros para Busca de Lote
  
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
    ARMAZEM = (('Macaé - RJ', 'Macaé - RJ'), ('Rio de Janeiro - RJ', 'Rio de Janeiro - RJ'), ('Cubatão - SP','Cubatão - SP'))#Aqui é definido a escolha
    localArmazenamento = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=ARMAZEM, required=False)
    TIPOVENDA = (('Sucateamento','Sucateamento'), ('Vendido', 'Vendido'),('Leilão', 'Leilao'), ('', ''))
    tipoVenda = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}),choices=TIPOVENDA, required=False)
    nm = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'data-role':'tagsinput'}),label="NM:", required=False)
    isasipa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'data-role':'tagsinput'}),label="SIPA:", required=False)
    leilao = forms.ModelMultipleChoiceField(queryset=LEILAO.objects.prefetch_related(), required=False, widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}))
    #isasipa = forms.ModelMultipleChoiceField(queryset=lista_leilao, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control form-control-sm'}))
@login_required   #Como expliquei antes, isso serve para forçar o login anteriormente
def LotesBusca(request):

    if request.method=="POST":  # Se chegamos na página a partir de um POST do formulario:
        
        formBuscaLote = novoFormBusca(request.POST)
        if formBuscaLote.is_valid():  # Se o formulario for valido
            listaFinal = []
            lote = formBuscaLote.cleaned_data["lote"]   # lote recebe o valor de lote no formulario
            ano = formBuscaLote.cleaned_data["ano"]   # e todos os outros recebem seus respectivos valores do formulario
            gerencia = formBuscaLote.cleaned_data["gerencia"]
            proprietario = formBuscaLote.cleaned_data["proprietario"]
            al = formBuscaLote.cleaned_data["al"]
            responsavel = formBuscaLote.cleaned_data["responsavel"]
            alienacaoAutorizada = formBuscaLote.cleaned_data["alienacaoAutorizada"]
            localArmazenamento = formBuscaLote.cleaned_data["localArmazenamento"]
            tipoVenda = formBuscaLote.cleaned_data["tipoVenda"]
            nm = formBuscaLote.cleaned_data["nm"]
            isasipa= formBuscaLote.cleaned_data["isasipa"]
            leilao= formBuscaLote.cleaned_data["leilao"]
   
            lista = LOTE.objects.select_related('lote_gerencia','lote_responsavel', 'lote_leilao')   # lista recebe uma lista de todos os lotes que estão no banco de dados
            if lote:  # Se o lote não está vazio, ele utilizou o formulario o campo lote pra fazer uma busca
                lote = lote.split(',')   # Como podemos pesquisar por vários lotes, separados por (,), precisamos quebrar essa string por (,) para percorrer todos os lotes que ele quer buscar
                query = Q(lote_lote=0)    # Esse é um instrumento do Django para criar um query com vários parametros e ir juntando tudo em uma só
                for a in lote:    # Percorrendo a lista de lotes que ele tá buscando
                    query.add(Q(lote_lote=a), Q.OR)    # Vou adicionando cada um dos lotes na query que criei acima
                lista = LOTE.objects.filter(query)    # A lista onde eu busquei todos os lotes anteriormente, agora recebe um filtro de somente os lotes que ele pediu para buscar no formulário
            if ano:   # Se no formulário tinha um valor ano, nesse caso aqui sempre vai ter porque é um select com valores 2019, 2020 e 2021
                lista = lista.filter(lote_ano=ano)   # Adiciono o filtro do ano à lista geral
            if gerencia:   # Se houver gerencia preenchido no form...
                queryB = Q(lote_gerencia=0)   # Como gerencia posso adicionar uma ou mais segurando o btn ctrl do teclado, ele cria uma lista de gerencias tbm que será incluida na query
                for gere in gerencia:
                    queryB.add(Q(lote_gerencia=gere.id), Q.OR)   # Crio essa nova query vai montando a lista de gerencias a ser buscada
                lista = lista.filter(queryB)   # Adiciono a query à lista final
            if proprietario:    # Se houver proprietario na busca...
                queryC = Q(lote_proprietario="")   # Mesmo esquema acima
                for prop in proprietario:
                    queryC.add(Q(lote_proprietario=prop), Q.OR)
                lista = lista.filter(queryC)
            if al:     # Esse do AL é muito similar ao do lote, pois é uma caixa de texto onde pode-se buscar vários separados por (,)
                al = al.split(',')
                queryD = Q(lote_al="")
                for b in al:
                    queryD.add(Q(lote_al__iexact=b), Q.OR)
                lista = lista.filter(queryD)
            if responsavel:  # O mesmo serve para os campos abaixo
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
            
            if isasipa:  # Se o lote não está vazio, ele utilizou o formulario o campo lote pra fazer uma busca
                isasipa = isasipa.split(',')   # Como podemos pesquisar por vários lotes, separados por (,), precisamos quebrar essa string por (,) para percorrer todos os lotes que ele quer buscar
                queryI = Q(lote_isaSipa="a")    # 
                for sip in isasipa:    # Percorrendo a lista de lotes que ele tá buscando
                    queryI.add(Q(lote_isaSipa=sip), Q.OR)    
                lista = lista.filter(queryI) 
            
            if leilao:   
                queryJ = Q(lote_leilao=0)   # Como gerencia posso adicionar uma ou mais segurando o btn ctrl do teclado, ele cria uma lista de gerencias tbm que será incluida na query
                for leil in leilao:
                    queryJ.add(Q(lote_leilao = leil.id ), Q.OR)   
                lista = lista.filter(queryJ) 
               

            if nm:   # Esse do NM está fora da lógica, pq como te falei NM é um atributo de Materiais, e não de lote
                # Essa busca está aqui para buscarmos pelo NM e conseguirmos saber em qual lote ele está
                nm = nm.split(',')  # Como é uma caixa de texto com uma lista separada por (,)
                for a in nm:    # percorremos essa lista
                 
                    material = MATERIAL.objects.get(mate_cod=a)  # fazemos uma busca de todos os materiais com os NMs buscados
                    lode = LOTE_DET.objects.get(lode_material=material)   # fazemos uma busca de todos os lote_det com base nos materiais que foram retornados na busca acima
                    lista = LOTE.objects.filter(lote_lote = lode.lode_lote)   # fazemos uma busca de todos os lotes com base nos lote_det buscados acima
                    
                # no caso dessa busca por NM, ela apaga a busca por todos os campos anteriores, ou seja, só retorna a busca dela, pois é uma busca em tabelas diferentes

            valorContabil = 0   # Aqui eu inicializo a variavel com valor igual a zero
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')    # Defino o local para posteriormente definir a moeda
            for lotes in lista:   # percorrendo toda a lista de lotes com base na busca que foi realizada
                lodes = LOTE_DET.objects.filter(lode_lote=lotes.lote_lote)    # para cada lote eu busco na tabela lote_det
                valorVMA=0   # inicializo a variavel valorVMA
                for lode in lodes:    # percorro a lista de lote_det retornada
                    valorContabil = valorContabil + lode.lode_valorContabilTotal  # Pego o valor de cada material e vou somando
                    valorVMA = valorVMA + lode.lode_vmaTotal   # pego o valor de cada valorVMA e vou somando

            valorContabil = locale.currency(valorContabil, grouping=True)   # Apos fazer o somatório total, eu retorno o valor contabil da busca geral de lotes em formato de moeda em reais para a tela
            #round(valorContabil, 2)

                
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'valorContabil':valorContabil,
                'formBusca': formBuscaLote,
                'formBuscaB': formBuscaLote  # Aqui eu renderizo o template table_lotesLista.html, essa variável lotes recebe a lista de lotes que eu trate e o formBusca recebe o mesmo formulário que foi buscado
            })
        else:
            lista = None
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formBusca': formBuscaLote
            })
    else:  # Como viemos até essa view sem um metodo post do formulario
        lista = None   # A lista que vai carregar no template recebe valor nulo
        return render(request, 'table_lotesLista.html', {   
            'lotes':lista,
            'formBusca':novoFormBusca()     # retornamos a renderização do template table_lotesLista.html, onde lotes vai ser nulo e o formulario que vamos carregar é um novo formulário de buscas
        })

class formUpload(forms.Form):
    frmUpload = forms.FileField(label="Teste")

@login_required  #Aqui eu defino que para acessar essa página é necessário estar logado
def LotesUpload(request):  #É uma view que solicita por base de uma requisição

    if request.method=="POST":   #Se chegamos nessa view por um formulário com método post
        form = formUpload(request.POST, request.FILES)
        if form.is_valid():   #Validação se o formulário é válido 

            log = open('E:\\logPainelSAM.csv', 'w', newline='', encoding='utf-8')   #Aqui eu crio um novo arquivo csv que vai ser onde gravo o log
            
            upload = request.FILES['frmUpload'].read().decode('latin-1').splitlines() # Aqui eu faço a leitura do arquivo csv que o usuário upou
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            listaErros = []
            erro = ''
            linha = 0
            next(reader)
            for dadosLinha in reader: #aqui começo a ler o documento que fou upado, um arquivo csv no caso

                #Inserir dados até a linha: 
                if linha<30000:    # leio somente até 30mil linhas
                    print(linha+2)  # o contador de  lotes que aparece no terminal
                    #Estrutura de Lotes
                    if(dadosLinha[2]):
                        numero_lote = ''
                        try: numero_lote = LOTE.objects.get(lote_lote = dadosLinha[2])   # Aqui eu pego o número do lote e vejo no banco de dados se ele já está inserido, se esse lote já existe
                        except:
                            a = 1

                        if numero_lote: # Se o lote existir:
                            erro = inserirLoteDetalhe(dadosLinha)  # Ele executa essa função para inserir os materiais
                            if erro:
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n') # Grava no log em caso de erro na inserção de materiais do lote
                        else:   # Se o lote não existir
                            erro = inserirLote(dadosLinha)  # Ele executa essa função para inserir o lote
                            if erro:
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n')  # Grava no log em caso  de erro
                            else:
                                erroB = inserirLoteDetalhe(dadosLinha)  # Apoós inserir o lote novo, ele insere os materiais 
                                if erroB:
                                    log.write('Somente o lote foi inserido. Erro na linha: '+str(linha+2)+'. '+erroB+'\n')  # Caso dê erro nos materiais, ele iinseriu somente o lote e grava esse erro também no log
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote é obrigatório. Verifique se está vazio ou incorreto!\n')  # E caso o número de lote esteja vazio na planilha, ele grava esse erro no log
                        return render(request,'table_lotesLista')
                linha+=1

            log.close()  # Caso tenha terminado fecha o log e salva
            return render(request, 'table_lotesLista.html', {
                'lotes':listaLotes,
                'formUpload': form
            })   # renderiza o template acima, retornando o formulário anterior
        else:
            upload = request.POST['frmUpload']
            print(upload)
            lista = None
            return render(request, 'table_lotesLista.html', {
                'lotes':lista,
                'formUpload': form
            })
    else:
        lista = None
        return render(request, 'table_lotesLista.html', {
            'lotes':lista,
            'formUpload':formUpload()
        })

def inserirLote(i):  # Inserir um lote novo - Passando a linha como argumento
    lote = LOTE()  # Crio o objeto LOTE
    lote.lote_lote = i[2]  # O número do lote recebe a coluna 2 da planilha
    lote.lote_ano = 2021  # Estamos inserindo lotes do ano de 2021

    if i[0]:
        lote.lote_proprietario = i[0] # Nessa linha atributo o proprietário do lote
    if (inserirGerencia(i[1]) == True):  # Aqui eu insiro a gerência ou verifico se ela já existe
        lote.lote_gerencia = GERENCIA.objects.get(gere_nome = i[1])  # Aqui eu atribuo a chave da tabela gerência ao lote
    else: return ('Campo Gerência é obrigatório. Verifique se está vazio ou incorreto!') # Se retornar falso no inserirGerencia() ele retonar esse erro e salva no log
    
    if i[3]:
        lote.lote_al = i[3]  # Atribuo o AL ao lote
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
        lote.save()  # Aqui ele tenta salvar no lote novo criado
    except Exception as e:
        print('Erro ao salvar o lote.')  # Caso tenha dado erro, ele vai dar essa exceção 
        print('%s' % (type(e)))
        return ('Erro ao salvar o lote')  # E vai salvar no log a mensagem ao lado

def inserirGerencia(gerenciaCampo):
                   
    #Estrutura da Gerência
    if gerenciaCampo:
        nome_gerencia = ''
        try: nome_gerencia = GERENCIA.objects.get(gere_nome = gerenciaCampo)  # Aqui eu busco se a gerência já existe
        except: a=0 
        if nome_gerencia: # Se existir, retorno
            return True
        else:  # Se não existir:
            gerencia = GERENCIA()  #Crio um novo objeto do tipo GERENCIA
            gerencia.gere_nome = gerenciaCampo  # Insiro Nome
            gerencia.gere_grupo = 0 # Insiro o grupo
            gerencia.save() # E salvo a nova gerencia
            return True
    else:
        return False  # Caso dê algum erro, retorna falso

def inserirLoteDetalhe(i): # Função para inserir o material atribuido a um lote

    #Estrutura de lote detalhe
    loteDetalhe = LOTE_DET()  # Crio um novo objeto
    loteDetalhe.lode_lote = LOTE.objects.get(lote_lote = i[2])  # Insiro a chave da lote na tabela LOTE_DET

    if (inserirMaterial(i[4], i[5], i[6], i[7]) == True):  # Inserir um novo material na tabela MATERIAL
        loteDetalhe.lode_material = MATERIAL.objects.get(mate_cod = i[4])  # Busco o MATERIAL novo inserido ou caso já existisse
    else: return ('Campo Material é obrigatório. Verifique se está vazio ou incorreto!') # Caso tenha retornado falso a inserção do MATERIAL ele vai salvar essa mensagem no log
    
    loteDetalhe.lode_centroAtual = i[8]  # Atribuo o centro do material do lote
    loteDetalhe.lode_elementoPep = i[9]  # Atribuo o elemento Pep do material do lote
    loteDetalhe.lode_deposito = i[10]   # etc todos abaixo
    loteDetalhe.lode_tipoAvaliacao = i[11]
    loteDetalhe.lode_loteNm = i[12]
    loteDetalhe.lode_numeroSerie = i[13]
    if i[14]:
        try:
            loteDetalhe.lode_quantidadeOriginal = float(i[14].replace(',','.'))  # Aqui por ser um campo numério, monetário, eu troco , por .
        except: return ('Campo Quantidade Original deve ter um valor do tipo real')   # Todas essas mensagens vão para o log caso tenha um erro em qualquer uma dessas validações
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

    if i[25]:
        try:
            loteDetalhe.lode_valorTotalReposicao = float(i[25].replace(',','.'))
        except: return ('Campo Valor Total de Reposição deve ter um valor do tipo real')  
    else: loteDetalhe.lode_valorTotalReposicao = 0

    if i[27]:
        try:
            loteDetalhe.lode_vmaTotal = float(i[27].replace(',','.'))
        except: return ('Campo VMA Total deve ter um valor do tipo real') 
    else: loteDetalhe.lode_vmaTotal = 0

    try:
        loteDetalhe.save() # Salvo o materia de um lote novo criado
    except Exception as e:
        print('Erro ao salvar o detalhe do lote.')  # Caso tenha erro lanço uma exceção
        print('%s' % (type(e)))
        return ('Erro ao salvar o detalhe do lote')  # E salvo a mensagem no log


def inserirMaterial(material, descr, ncm, gm): # Função para inserir um novo material ou veririficar se ele já existe

    #Estrutura de Material
    if material:
        nm_material = ''
        try: nm_material = MATERIAL.objects.get(mate_cod = material)  # Eu busco no banco se já existe o material pelo código dele
        except: a=1
        if nm_material:
            return True # Se existir eu retorno
        else: # Se não existir
            mate = MATERIAL()  # Crio um novo objeto do tipo MATERIAL
            mate.mate_cod = material  # Insiro co código que é a chave primaria
            mate.mate_descricao = descr  # Descrição e etc abaixo
            mate.mate_ncm = ncm
            mate.mate_grupoMercadoria = gm
            mate.save()  # Salvo o material
            return True
    else:
        return False

class novoFormLeilao(forms.Form):
    frmLeilaoUpload = forms.FileField(label="Teste", required=False)
    nome = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),label="Leilão:", required=False)
    data = forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control form-control-sm'}),label="Data do Leilão:", required=False)

@login_required
def LeilaoUpload(request):    # view para inserir um novo leilao e dados da disputa aberta em massa

    if request.method=="POST":      # se o formulario for metodo post
        form = novoFormLeilao(request.POST, request.FILES)
        if form.is_valid():

            log = open('E:\\logLeiloesPainelSAM.csv', 'w', newline='', encoding='utf-8')
            upload = ""
            # AQUI TEMOS A MAIOR DIFERENÇA DA VIEW DE INSERÇÃO EM MASSA
            nome = request.POST['nome']    # Pego o valor de nome que tiver no formulário
            data = request.POST['data']    # Pelo a data que estiver no formulário
            
            leilao = LEILAO()    # Crio um novo objeto do tipo leilão
            leilao.leil_nome = nome    # Atibuo o nome
            leilao.leil_dataResultadoLeilao = datetime.strptime(data, '%d/%m/%Y').date()    # Atribuo a data
            try:
                leilao.save()     # Tento salvar
            except Exception as e:
                print('Erro ao salvar o leilao.')
                print('%s' % (type(e)))
                return ('Erro ao salvar o leilao')
            
            upload = request.FILES['frmLeilaoUpload'].read().decode('latin-1').splitlines()     # Agora começo a ler o csv que foi upado
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            erro = ''
            linha = 0
            next(reader)
            # TODA ESSA PARTE DE LEITURA DO CSV E PERCORRER O CSV E INSERIR EM NOVOS OBJETOS É IGUAL A PARTE DE LOTES
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

                        if numero_lote:      # Caso no campo lote do csv esteja tudo certinho e exista o lote:
                            if (inserirComprador(dadosLinha[1], dadosLinha[2], dadosLinha[3], dadosLinha[4], dadosLinha[5], dadosLinha[6], dadosLinha[7], dadosLinha[8], dadosLinha[10]) == True):     # Insiro o Comprador e seus dados utilizando a função inserirComprador
                                a = 1
                            else: return ('Campo Comprador é obrigatório. Verifique se está vazio ou incorreto!')    # Se não conseguir dá erro

                            numero_lote.lote_leilao = leilao      # Caso tenha inserido, ou o coprador já exista, eu insiro na tabela LOTE o leilão que o lote foi leiloado
                            numero_lote.lote_tipoVenda = "Vendido"      # Mudo na tabela lote o valor de tipoVenda para Vendido
                            numero_lote.save()      # Salvo as alterações do referido lote

                            disputaAberta = DISPUTA_ABERTA()      # Crio um novo objeto de disputa aberta
                            disputaAberta.diab_lote = numero_lote     # Insiro o lote
                            disputaAberta.diab_comprador = COMPRADOR.objects.get(comp_cnpj = dadosLinha[1])    # Insiro o novo comprador
                            try:
                                disputaAberta.diab_lanceTotal = float(dadosLinha[9].replace(',','.'))    # Insiro o lance que foi dado
                            except:
                                log.write('Erro na linha: '+str(linha+2)+'. O valor do lance não foi inserido. Não é númeral. \n')    # Validação do erro no log

                            disputaAberta.save()     # Salvo a nova disputa aberta
                            if erro:
                                log.write('Erro na linha: '+str(linha+2)+'. '+erro+'\n')
                        else: 
                            log.write('Erro na linha: '+str(linha+2)+'. O LOTE NAO FOI ENCONTRADO NO BD \n')
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote é obrigatório. Verifique se está vazio ou incorreto!\n')
                linha+=1
            log.close()     # Fecho o log

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
        })    # Rederizo para a tela de acordo com cada um dos casos





def inserirComprador(cnpj, nomeComp, telefoneRes, telefoneCom, celular, cidade, estado, endereco, email):     # Essa é a função de apoio para inserir o comprador

    # Somente insiro os valores de acordo com os atributos do model de Comprador, o cnpj é a chave primária, sem ela não insere, ou se ela já existir ele retonar true para a view
    if cnpj:
        comprador = ''
        try: comprador = COMPRADOR.objects.get(comp_cnpj = cnpj) 
        except: a=1
        if comprador:
            return True    # Se o comprador já existir retorna true
        else:     # Se não, cria um novo comprador
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
            return True
    else:
        return False    
        

@login_required
def ListaGerencial(request):     # Essa view apresenta a tabela dos dados no formato gerencial conforme solicitado pelo Tiago

    listaGerencial = []     # Crio uma nova lista gerencial
    a = 0
    lista = LOTE.objects.filter(lote_ano=2021).values("lote_isaSipa", "lote_dataSipa")      # Nessa lista eu busco todos os valores da tabela LOTES, do ano de 2021, mas somente as colunas lote_sipa e lote_data_sipa
    [listaGerencial.append(i) for i in lista if not listaGerencial.count(i)]     # Aqui inicio a criação da lista gerencial, onde pego somente os ISA Sipas sem repetir, formando uma lista somente de ISA SIPAS
    listaFinal = []
    valorContabilTotal = 0     # Esse valor contabil é somente para apresentar na parte de cima da tabela
    for c in listaGerencial:      # Agora começo a montar a lista final a ser enviada para o template
        if (c['lote_isaSipa'].find(" ")==-1):      # Selecionar somente ISA SIPAS que não possuem espaço vazio " "
            # Inicialização de variáveis que compõem a tabela, essas variaveis não são atributos de colunas e sim somatórios de valores, somatórios de contadores etc, são informações novas com base nas informações armazenadas no banco
            qtdLotes=0       # Quantidade de lotes para cada ISA
            qtdLeilao=0    # Quantidade de lotes que foram a leilão para cada ISA
            qtdSucatas=0    # Quantidade de lotes sucateados para cada ISA
            qtdVendidos=0    # Quantidade de lotes que foram vendidos
            valorContTotal=0    # Somatório de valor contábil de todos os lotes de acordo com cada ISA
            valorLeilao=0      # Somatório de valor que foi a leilão para cada ISA
            valorSucata=0     # Somatório de valor que foi sucateado para cada ISA
            for lotes in LOTE.objects.filter(lote_isaSipa__icontains = c['lote_isaSipa']):    # Buscar dentro da Tabela LOTES, na coluna lote_isaSipa, que contenha o valor da minha lista de ISA SIPAS
                gerencia = lotes.lote_gerencia     # Nessa lista nova eu adiciono a gerência desse ISA SIPA
                proprietario = lotes.lote_proprietario   # Adiciono tambem o proprietario desse ISA SPIA

                lodes = LOTE_DET.objects.filter(lode_lote=lotes.lote_lote)    # Seleciono todos os materiais desse lote
                valorCont=0
                for lode in lodes:    # Percorro a lista de materiais do determinado lote
                    valorCont = valorCont + lode.lode_valorContabilTotal    # Vou somando o valor contábil do referido lote
                    valorContTotal = valorContTotal + valorCont     # Vou somando o valor contábil do lote ao valor total do ISA SIPA

                if(lotes.lote_leilao):    # Se o lote foi a leilão
                    qtdLeilao+=1    # Adiciono mais 1 ao contador de lotes em leilão
                    valorLeilao = valorLeilao + valorCont     # O valor que foi a leilão recebe o valor contabil do lote
                if(lotes.lote_tipoVenda == 'Sucateamento'):     # Se o lote foi sucateado
                    qtdSucatas+=1    # Adciono mais 1 ao contador de lotes sucateados
                    valorSucata = valorSucata + valorCont     # Valor que foi sucateado recebe o valor contabil do lote
                if(lotes.lote_tipoVenda == 'Vendido'):     # Se o lote foi vendido
                    qtdVendidos+=1    # Adiciono mais 1 ao contador de lotes vendidos
                qtdLotes+=1    # Contador geral de lotes recebe mais 1
            c['qtdLotes'] = qtdLotes     # lista final recebe a quantidade de lotes
            c['gerencia'] = gerencia     # lista final recebe a gerencia do ISA SIPA
            c['proprietario'] = proprietario     # lista final recebe o proprietario
            c['qtdLeilao'] = qtdLeilao      # lista final recebe a quantidade de lotes que foi a leilão
            c['qtdSucatas'] = qtdSucatas     # lista final recebe a quantidade de lotes sucateados
            c['qtdVendidos'] = qtdVendidos     # lista final recebe a quantidade de lotes vendidos
            c['valorCont'] = round(valorContTotal, 2)     # lista final recebe o valor contabil total do isa sipa
            c['valorLeilao'] = round(valorLeilao, 2)     # lista final recebe o valor total dos lotes que foram a leilão
            c['valorSucata'] = round(valorSucata, 2)      # lista final recebe o valor total de lotes sucateados
            listaFinal.append(c)     # Adiciono esses dados à listaFinal
            a+=1
            valorContabilTotal = valorContabilTotal + valorContTotal     # Fecho o valor contabil total que demonstro em cima da tabela
    
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valorContabilTotal = locale.currency(valorContabilTotal, grouping=True)    # Apresento como valor monetário

    return render(request, 'table_gerencial.html', {
            'lista':listaFinal,
            'valorTotal':valorContabilTotal,
            'novoFormLeilao':novoFormLeilao()})    # Carrego para o template a variavel lista, que contem a nossa listaFinal com todos os atributos que enviamos. Carrego para o template o valorContabil e carrego um novo form que não está sendo utilizado por enquanto. O template é o table_gerencial


def export(request):   # View para exportar os lotes buscados

    if request.method=="POST":   # Novamente se chegamos aqui por um metodo post
        start_time = time.time() 
        formBuscaLote = novoFormBusca(request.POST)
        if formBuscaLote.is_valid():
            listaFinal = []
            lote = formBuscaLote.cleaned_data["lote"]   # eu atribuo a uma variavel cada um dos campos do formulário e tudo nessa view é muito similar a view de busca que falei anteriormente
            # Como ela é muito similar, eu penso que depois desses testes é possível encapsular tudo isso e colocar uma função só pra tratar dessa busca, que seriviria para ambas as views
            ano = formBuscaLote.cleaned_data["ano"]
            gerencia = formBuscaLote.cleaned_data["gerencia"]
            proprietario = formBuscaLote.cleaned_data["proprietario"]
            al = formBuscaLote.cleaned_data["al"]
            responsavel = formBuscaLote.cleaned_data["responsavel"]
            alienacaoAutorizada = formBuscaLote.cleaned_data["alienacaoAutorizada"]
            localArmazenamento = formBuscaLote.cleaned_data["localArmazenamento"]
            tipoVenda = formBuscaLote.cleaned_data["tipoVenda"]
            nm = formBuscaLote.cleaned_data["nm"]

            lista =  LOTE.objects.select_related('lote_gerencia','lote_responsavel','lote_leilao')
            if lote:
                lote = lote.split(',')
                query = Q(lote_lote=0)
                for a in lote:
                    query.add(Q(lote_lote=a), Q.OR)
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
                 listaB = LOTE_DET.objects.select_related('lode_lote','lode_material')

    queryM = Q(lode_lote=0)
    for lotes in lista:    # aqui eu percorro a lista de lotes
      queryM.add(Q(lode_lote=lotes.lote_lote), Q.OR)    # aqui eu vou fazendo uma query de busca de cada um dos materiais de cada lote, na tabela lote_det
    listaB = LOTE_DET.objects.filter(queryM).select_related('lode_lote','lode_material')  # E finalmente monto uma lista completa com lotes, materiais dos lotes e todos os atributos
    #
    # listaB =LOTE_DET.objects.all()
   
    # for lotes  in lista:
    #     listaB.lode_lote = lotes.lote_lote
    
    listaC = listaB
    for lotes in listaC:  
                lista.lote_lote = lotes.lode_lote 
                   
    
                  
    print (listaC.query)
   
    # disp =DISPUTA_ABERTA.objects.select_related('diab_lote','diab_comprador').order_by('diab_lote')
    # lot= LOTE.objects.select_related('lote_leilao')
    # for p  in lot:
    #    disp.diab_lote = p.lote_lote

    end_time=time.time()
    duration=(end_time - start_time)
    print(f'Executou um total de {len(connection.queries)}Queries')
    print(f'Tempo de Execuçao {round(duration, 3)}Segundos')
    reset_queries()
     
    response = HttpResponse(content_type='application/ms-excel')   # parametros para criar o arquivo excel

    response['Content-Disposition'] = 'attachment; filename="export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lotes')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Lote', 'Gerencia', 'Proprietario', 'AL', 'Ano', 'Responsavel', 'Alienacao Autorizada?', 
            'Quantidade de Fotos', 'Local Armazenamento', 'ISA Sipa', 'Data Sipa', 'Tipo de Venda', 'Leilao', 
            'ISA Envio ARM', 'Data de Envio ARM', 'VMA Total Lote', 'Material NM', 'Material Descrição', 
            'Material NCM', 'Material GM', 'Centro Atual', 'Elemento PEP', 'Depósito', 
            'Tipo de Avaliação', 'Lote NM', 'Número de Série', 'Quantidade Original', 'Quantidade Retirada DIP',
            'Quantidade Não Localizada', 'Quantidade Atual', 'Unidade', 'ISA de Retirada', 'Data de Retirada', 
            'Valor Contábil Unitário', 'Valor Contábil Total', 'Valor Contábil Total Atual', 'Valor Reposição Unitário',
            'Valor Total Reposição', 'Valor Comparação VMA', 'VMA Unitário', 'VMA Total', 'VMA Percentual do Lote']
    # primeira linha do excel

    for col_num in range(len(columns)):   # percorro a quantidade de colunas definido na primeira linha
        ws.write(row_num, col_num, columns[col_num], font_style)   # vou escrevendo célula por célula com os atributos ao lado

    font_style = xlwt.XFStyle()
    
    rows = listaC.values_list(
                                'lode_lote', 
                                'lode_lote__lote_gerencia__gere_nome', 
                                'lode_lote__lote_proprietario', 
                                'lode_lote__lote_al', 
                                'lode_lote__lote_ano', 
                                'lode_lote__lote_responsavel__username', 
                                'lode_lote__lote_alienacaoAutorizada', 
                                'lode_lote__lote_quantidadeFoto', 
                                'lode_lote__lote_localArmazenamento', 
                                'lode_lote__lote_isaSipa', 
                                'lode_lote__lote_dataSipa', 
                                'lode_lote__lote_tipoVenda', 
                                'lode_lote__lote_leilao__leil_nome', 
                                'lode_lote__lote_isaEnvioArm',
                                'lode_lote__lote_dataEnvoArm', 
                                'lode_lote__lote_vmaLote', 
                                'lode_material__mate_cod', 
                                'lode_material__mate_descricao', 
                                'lode_material__mate_ncm', 
                                'lode_material__mate_grupoMercadoria', 
                                'lode_centroAtual', 
                                'lode_elementoPep', 
                                'lode_deposito', 
                                'lode_tipoAvaliacao', 
                                'lode_loteNm', 
                                'lode_numeroSerie', 
                                'lode_quantidadeOriginal', 
                                'lode_quantidadeRetiradaDip', 
                                'lode_quantidadeNaoLocalizada', 
                                'lode_quantidadeAtual', 
                                'lode_unidade', 
                                'lode_isaRetirada', 
                                'lode_dataRetirada', 
                                'lode_valorContabilUnitario', 
                                'lode_valorContabilTotal', 
                                'lode_valorContabilTotalAtual', 
                                'lode_valorReposicaoUnitario', 
                                'lode_valorTotalReposicao', 
                                'lode_valorComparacaoVMA', 
                                'lode_vmaUnitario', 
                                'lode_vmaTotal', 
                                'lode_vmaPercentualLote'
        )
    
    for row in rows:   # percorro a quantidade de linhas que tem a listaB que é a nossa lista geral, com base nos argumentos definidos acima
        row_num += 1   # pulo uma linha porque a primeira já é nosso titulo das colunas
        for col_num in range(len(row)):   # vou gravando celula por celula cada linha da listaB
            ws.write(row_num, col_num, row[col_num], font_style)
 
    

    wb.save(response)   # Salvo o excel
   

    

    return response    # Retorno
    



####################################################################################
########### PAGINA NOVA PARA USO FUTURO   
@login_required  
def CadastrarUsuario(request): 

  
        return render(request, 'cadastro.html', {
       
          
         
        })

      

  
def export_disputa(request):   #VIEW PARA EXPORTAR DISPUTA ABERTA

    if request.method=="POST":  
     
     response = HttpResponse(content_type='application/ms-excel')# parametros para criar o arquivo excel

     response['Content-Disposition'] = 'attachment; filename="exportDisputa.xls"'

     wb = xlwt.Workbook(encoding='utf-8')
     ws = wb.add_sheet('Disputa Aberta')

     row_num = 0

     font_style = xlwt.XFStyle()
     font_style.font.bold = True
     columns = [
                                    'Lote',
                                    'CNPJ Comprador',
                                    'Nome',
                                    'Cidade',
                                    'Estado',
                                    'Telefone',
                                    'Email',
                                    'ComunicadoVenda Enviado',
                                    'ValorVenda Lance Total',
                                    'Valor Venda SAB',
                                    'Prazo para Pagamento',
                                    'Data do Pagamento',
                                    'Valor Pago',
                                    'Lance Total',
                                    'Leilão',
                                    'Data do Leilão' 
                    ]
    for col_num in range(len(columns)):   # percorro a quantidade de colunas definido na primeira linha
        ws.write(row_num, col_num, columns[col_num], font_style) 
    font_style = xlwt.XFStyle()

    start_time = time.time()
 
    #################################################################################################
    ############ metedo de exportação A - cria muitos parametros na query SERÁ USADO FUTURAMENTE
    # queryX= Q(lote_lote=0)
    # lista2 = DISPUTA_ABERTA.objects.select_related('diab_lote','diab_comprador')  
    # for lotes in lista2:   
    #           queryX.add(Q(lote_lote=lotes.diab_lote), Q.OR) 
    # listaq = LOTE.objects.filter(queryX).order_by('lote_lote')[:10]
    disp =DISPUTA_ABERTA.objects.select_related('diab_lote','diab_comprador').order_by('diab_lote')
    lot= LOTE.objects.select_related('lote_leilao')
    for p  in lot:
       disp.diab_lote = p.lote_lote

   
    print (disp.query)

    end_time=time.time()
    duration=(end_time - start_time)
    print(f'Executou um total de {len(connection.queries)}Queries')
    print(f'Tempo de Execuçao {round(duration, 3)}Segundos')
    
    
    rows = disp.values_list( #'disputa_aberta__diab_lote',
                                   'diab_lote',
    #                             'disputa_aberta__diab_comprador__comp_cnpj',
                                   'diab_comprador__comp_cnpj',
    #                             'disputa_aberta__diab_comprador__comp_nomeComprador',
                                   'diab_comprador__comp_nomeComprador',
    #                             'disputa_aberta__diab_comprador__comp_cidade',
                                   'diab_comprador__comp_cidade',
    #                             'disputa_aberta__diab_comprador__comp_estado',
                                   'diab_comprador__comp_estado',
    #                             'disputa_aberta__diab_comprador__comp_telefoneComercial',
                                   'diab_comprador__comp_telefoneComercial',
    #                             'disputa_aberta__diab_comprador__comp_email',
                                   'diab_comprador__comp_email',
    #                             'disputa_aberta__diab_comunicadoVendaEnviado',
                                   'diab_comunicadoVendaEnviado',
    #                             'disputa_aberta__diab_valorVendaLanceTotal',
                                   'diab_valorVendaLanceTotal',
    #                             'disputa_aberta__diab_valorVendaSab',
                                   'diab_valorVendaSab',
    #                             'disputa_aberta__diab_prazoPagamento',
                                   'diab_prazoPagamento',
    #                             'disputa_aberta__diab_dataPagamento',
                                   'diab_dataPagamento',
    #                             'disputa_aberta__diab_valorPago',
                                   'diab_valorPago',
    #                             'disputa_aberta__diab_lanceTotal',
                                   'diab_lanceTotal',
    #                             'lote_leilao__leil_nome',
                                   'diab_lote__lote_leilao__leil_nome',
    #                             'lote_leilao__leil_dataResultadoLeilao',
                                   'diab_lote__lote_leilao__leil_dataResultadoLeilao'
                                  
                                  
                                )


    for row in rows:   # percorro  a quantidade de linhas que tem a listaB que é a nossa lista geral, com base nos argumentos definidos acima
        row_num += 1   # pulo uma linha porque a primeira já é nosso titulo das colunas
        for col_num in range(len(row)):   # vou gravando celula por celula cada linha da listaB
                   ws.write(row_num, col_num, row[col_num], font_style)
     
    wb.save(response)   # Salvo o excel
    reset_queries()
    return response    # Retorno
 ################################################################################## 

@login_required
def alterar_senha(request):
    
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Senha alterada com sucesso!!')
            return redirect('alterar_perfil')
    else:
        form_senha = PasswordChangeForm(request.user)
   


    return render(request,'alterar_senha.html',{'form_senha': form_senha}
    )

@login_required
def alterar_perfil(request):
    
   
    return render(request,'alterar_senha.html',{}
    )

##############################################################################
###################RESPONSAVEL UPLOAD

class novoFormResponsavel(forms.Form):
    frmResponsavelUpload = forms.FileField(label="Teste")

@login_required  #Aqui eu defino que para acessar essa página é necessário estar logado
def responsavelUpload(request):  #É uma view que solicita por base de uma requisição

    if request.method=="POST":   #Se chegamos nessa view por um formulário com método post
        form = novoFormResponsavel(request.POST, request.FILES)
        if form.is_valid():   #Validação se o formulário é válido 

            log = open('C:\\Logs\\logPainelSAM.csv', 'w', newline='', encoding='utf-8')   #Aqui eu crio um novo arquivo csv que vai ser onde gravo o log
            
            upload = request.FILES['frmResponsavelUpload'].read().decode('latin-1').splitlines() # Aqui eu faço a leitura do arquivo csv que o usuário upou
            
           
            
            ## PRIMEIRA PASSADA PARA VERIFICAR SE EXISTEM ERROS NO CSV
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            listaErros = []
            erro = ''
            linha = 0
            next(reader)
            for dadosLinha in reader: #aqui começo a ler o documento que foi upado, um arquivo csv no caso
                
                #Inserir dados até a linha: 
                if linha<30000:    # leio somente até 30mil linhas
                    print(linha+2)  # o contador de  lotes que aparece no terminal
                    #Estrutura de Lotes
                   
                    if(dadosLinha[0]):
                        numero_lote = ''
                        usuario_id= 0
                        try: numero_lote = LOTE.objects.get(lote_lote = dadosLinha[0])   # Aqui eu pego o número do lote e vejo no banco de dados se ele já está inserido, se esse lote já existe
                        except:
                            a = 1
                        try: usuario_id = User.objects.get(id = dadosLinha[1])
                        except:
                            a = 1
                       
                        if numero_lote: # Se o lote existir:
                                  if  usuario_id:  # roda somente se usuario e usuario existir
                                      anterior = numero_lote.lote_responsavel
                                      numero_lote.lote_responsavel_id = dadosLinha[1]
                                      
                                    
                                      
                                      
                                      
                                  else: 
                                       log.write('Erro na linha: '+str(linha+2) +
                                          '. Responsável inexistente\n')
                                       print('Erro na linha : ['+str(linha+2)+'] Responsável Inexistente\n')   
                                       context ={'mensagem2':'Erro na linha = ['+str(linha+2)+'] Responsável Inexistente, Verifique se o código do Responsável está vazio ou incorreto!' }
                                       return render(request,'form_responsavel.html',context)
                        else:   # Se o lote não existir
                                log.write('Erro na linha: '+str(linha+2)+'. Lote Inexistente\n')  # Grava no log em caso  de erro
                                print('Erro na linha : '+str(linha+2)+'.Lote Inexistente, Verifique se o código está vazio ou incorreto\n')
                                context ={'mensagem3':'Erro na linha : '+str(linha+2)+' Lote Inexistente, Verifique se o codigo está vazio ou incorreto!' }
                                return render(request,'form_responsavel.html',context)
                                # Apoós inserir o lote novo, ele insere os materiais 
                             
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote VAZIO é obrigatório. Verifique se está vazio ou incorreto!\n')  # E caso o número de lote esteja vazio na planilha, ele grava esse erro no log
                        print('Erro na linha : '+str(linha+2)+'.Campo lote é obrigtório')
                        context ={'mensagem3':'Erro na linha : '+str(linha+2)+'.Vazio Campo lote é obrigtório, Verifique se está vazio ou incorreto!'}
                        return render(request,'form_responsavel.html',context)

                        
                linha+=1
            # CASO NÃO EXISTAM ERROS, RELIZA A SEGUNDA LEITURA GRAVANDO NO BANCO    
            reader = csv.reader(upload, delimiter=';', quotechar='|')
            listaLotes = []
            listaErros = []
            erro = ''
            linha = 0
            next(reader)
            for dadosLinha in reader: #aqui começo a ler o documento que foi upado, um arquivo csv no caso
                
                #Inserir dados até a linha: 
                if linha<30000:    # leio somente até 30mil linhas
                    print(linha+2)  # o contador de  lotes que aparece no terminal
                    #Estrutura de Lotes
                   
                    if(dadosLinha[0]):
                        numero_lote = ''
                        usuario_id= 0
                        try: numero_lote = LOTE.objects.get(lote_lote = dadosLinha[0])   # Aqui eu pego o número do lote e vejo no banco de dados se ele já está inserido, se esse lote já existe
                        except:
                            a = 1
                        try: usuario_id = User.objects.get(id = dadosLinha[1])
                        except:
                            a = 1
                       
                        if numero_lote: # Se o lote existir:
                                  if  usuario_id:  # roda somente se usuario e usuario existir
                                      anterior = numero_lote.lote_responsavel
                                      numero_lote.lote_responsavel_id = dadosLinha[1]
                                      gravarHistorico('Alteração do Lote', request.user, numero_lote.lote_lote,'', 'Responsável', anterior, numero_lote.lote_responsavel,) 
                                    
                                      numero_lote.save()
                                      
                                      
                                  else: 
                                       log.write('Erro na linha: '+str(linha+2) +
                                          '. Responsável inexistente\n')
                                       print('Erro na linha : ['+str(linha+2)+'] Responsável Inexistente\n')   
                                       context ={'mensagem2':'Erro na linha = ['+str(linha+2)+'] Responsável Inexistente, Verifique se o código do Responsável está vazio ou incorreto!' }
                                       return render(request,'form_responsavel.html',context)
                        else:   # Se o lote não existir
                                log.write('Erro na linha: '+str(linha+2)+'. Lote Inexistente\n')  # Grava no log em caso  de erro
                                print('Erro na linha : '+str(linha+2)+'.Lote Inexistente, Verifique se o código está vazio ou incorreto\n')
                                context ={'mensagem3':'Erro na linha : '+str(linha+2)+' Lote Inexistente, Verifique se o codigo está vazio ou incorreto!' }
                                return render(request,'form_responsavel.html',context)
                                # Apoós inserir o lote novo, ele insere os materiais 
                             
                    else:
                        log.write('Erro na linha: '+str(linha+2)+'. Campo lote VAZIO é obrigatório. Verifique se está vazio ou incorreto!\n')  # E caso o número de lote esteja vazio na planilha, ele grava esse erro no log
                        print('Erro na linha : '+str(linha+2)+'.Campo lote é obrigtório')
                        context ={'mensagem3':'Erro na linha : '+str(linha+2)+'.Vazio Campo lote é obrigtório, Verifique se está vazio ou incorreto!'}
                        return render(request,'form_responsavel.html',context)

                        
                linha+=1
            log.close()  # Caso tenha terminado fecha o log e salva
            context1 ={'sucesso':'Responsáveis atribuídos em  : '+str(linha+0)+' Lotes, com sucesso!'}
            messages.success(request,'Concluído !!')
            return render(request, 'form_responsavel.html',context1)   # renderiza o template acima, retornando o formulário anterior
        else:
            upload = request.POST['frmResponsavelUpload']
            print(upload)
            lista = None
            return render(request, 'form_responsavel.html', {
                'lotes':lista,
                'novoFormResponsavel': form
            })
    else:
        lista = None
      
        return render(request, 'form_responsavel.html', {
            'lotes':lista,
            'novoFormResponsavel':novoFormResponsavel()

        })



@login_required
def logs_erro(request):
    context ={
        'mensagem1':'Lote inexistente'
    }
   
    return render(request,'errors/table_logs.html',context)
