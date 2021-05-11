from django.db import models

# Create your models here.

class GERENCIA(models.Model):
    gere_nome = models.CharField(max_length=50, null=False)
    gere_grupo = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.gere_nome

class LOTE(models.Model):
    lote_lote = models.CharField(primary_key=True, max_length=50, null=False)
    lote_gerencia = models.ForeignKey(GERENCIA, on_delete=models.CASCADE)
    lote_al = models.CharField(max_length=50, null=False)
    lote_centro = models.CharField(max_length=50, null=False)
    lote_elementoPep = models.CharField(max_length=50, null=True)
    lote_deposito = models.CharField(max_length=50, null=True)
    lote_tipoVenda = models.CharField(max_length=50, null=True)
    lote_alienacaoAutorizada = models.CharField(max_length=50, null=True)
    lote_superbid = models.CharField(max_length=200, null=True)
    lote_quantidadeFoto = models.BigIntegerField()
    lote_localArmazenamento = models.CharField(max_length=50, null=True)
    lote_fase = models.CharField(max_length=50, null=False)
    lote_dataSipa = models.DateField()
    lote_dataEnvioLotesLeilao = models.DateField()
    lote_dataSolicitacaoLeilao = models.DateField()
    lote_dataResultadoLeilao = models.DateField()

    def __str__(self):
        return self.lote_lote