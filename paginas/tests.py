from django.test import TestCase
from registos.models import LOTE
# Create your tests here.
lista = LOTE.objects.select_related(
    'lote_gerencia', 'lote_responsavel').select_related('lote_leilao')
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
                 listaB = LOTE_DET.objects.select_related('lode_lote').select_related('lote_material')
                 

queryM = Q(lode_lote=0)
for lotes in lista:   
 queryM.add(Q(lode_lote=lotes.lote_lote), Q.OR)   
listaB = LOTE_DET.objects.filter(queryM)  
