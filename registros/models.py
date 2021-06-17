from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    lote_dataSipa = models.CharField(max_length=50, null=False)
    lote_dataEnvioLotesLeilao = models.CharField(max_length=50, null=False)
    lote_dataSolicitacaoLeilao = models.CharField(max_length=50, null=False)
    lote_dataResultadoLeilao = models.CharField(max_length=50, null=False)
    lote_ano = models.BigIntegerField()

    def get_absolute_url(self):
       return reverse("lote-interno", kwargs={"pk": self.pk})

    def __str__(self):
        return self.lote_lote

class MATERIAL(models.Model):
    mate_cod = models.CharField(primary_key=True, max_length=50, null=False)
    mate_descricao = models.CharField(max_length=50, null=True)
    mate_ncm = models.CharField(max_length=50, null=True)
    mate_grupoMercadoria = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.mate_descricao

class LOTE_HIS(models.Model):
   lohi_lote = models.ForeignKey(LOTE, on_delete=models.CASCADE)
   lohi_material = models.ForeignKey(MATERIAL, on_delete=models.CASCADE)
   lohi_tipoAvaliacao = models.CharField(max_length=50, null=True)
   lohi_quantidadeOriginal = models.FloatField(null=True)
   lohi_quantidadeRetiradaDip = models.FloatField(null=True)
   lohi_quantidadeNaoLocalizada = models.FloatField(null=True)
   lohi_quantidadeAtual = models.FloatField(null=True)
   lohi_unidade = models.CharField(max_length=50, null=True)
   #lohi_dipSipa = models.FloatField(null=True)
   lohi_retirada = models.CharField(max_length=50, null=True)
   lohi_valorContabilUnitario = models.FloatField(null=True)
   lohi_valorContabilTotal = models.FloatField(null=True)
   lohi_valorReposicaoUnitario = models.FloatField(null=True)
   lohi_valorTotalReposicao = models.FloatField(null=True)
   lohi_valorComparacaoVMA = models.FloatField(null=True)
   lohi_vmaUnitario = models.FloatField(null=True)
   lohi_vmaTotal = models.FloatField(null=True)

   def __str__(self):
        return self.lohi_lote

class TESTES(models.Model):
    testeA = models.CharField(max_length=50, null=True)
    testeB = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.testeA

class HIST_LOTE(models.Model):
    hist_tipoAlteracao = models.CharField(max_length=50, null=False)
    hist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    hist_lote = models.ForeignKey(LOTE, on_delete=models.CASCADE)
    hist_coluna = models.CharField(max_length=50, null=False)
    hist_dadoAnterior = models.CharField(max_length=50, null=False)
    hist_dadoNovo = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.hist_tipoAlteracao

