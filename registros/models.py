from django.db import models
from django.db.models.fields import DateField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class GERENCIA(models.Model):
    gere_nome = models.CharField(max_length=50, null=False)
    gere_grupo = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.gere_nome

class LEILAO(models.Model):
    leil_nome = models.CharField(max_length=50, null=False)
    leil_dataResultadoLeilao = models.DateField(null=False)

    def __str__(self):
        return f"{self.id} : {self.leil_nome}"

class LOTE(models.Model):

    AUTORIZADA = (
        ('Autorizada', 'Autorizada'), 
        ('Não Autorizado', 'Não Autorizado')
    )
    PROPRIETARIO = (
        ('Petrobras', 'Petrobras'),
        ('Consorcio', 'Consorcio')
    )
    TIPOVENDA = (
        ('Sucateamento','Sucateamento'),
        ('Vendido', 'Vendido'),
        ('', '')
    )
    ANO = (
        (2019, 2019),
        (2020, 2020),
        (2021, 2021)
    )

    lote_lote = models.CharField(primary_key=True, max_length=50, null=False)
    lote_gerencia = models.ForeignKey(GERENCIA, on_delete=models.SET_NULL, null=True)
    lote_proprietario = models.CharField(choices=PROPRIETARIO, max_length=50, null=False)
    lote_al = models.CharField(max_length=50, null=False)
    lote_ano = models.IntegerField(choices=ANO)
    lote_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lote_alienacaoAutorizada = models.CharField(max_length=50, choices=AUTORIZADA, null=False)
    lote_quantidadeFoto = models.BigIntegerField(null=True, blank=True)
    lote_localArmazenamento = models.CharField(max_length=50, null=True, blank=True)
    lote_isaSipa = models.CharField(max_length=50, null=True, blank=True)
    lote_dataSipa = models.DateField(null=True, blank=True)
    lote_tipoVenda = models.CharField(choices=TIPOVENDA, max_length=50, null=True, blank=True)
    lote_leilao = models.ForeignKey(LEILAO, on_delete=models.SET_NULL, null=True, blank=True)
    lote_isaEnvioArm = models.CharField(max_length=50, null=True, blank=True)
    lote_dataEnvoArm = models.DateField(null=True, blank=True)
    lote_vmaLote = models.FloatField(null=True, blank=True)

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

class LOTE_DET(models.Model):
    lode_lote = models.ForeignKey(LOTE, on_delete=models.CASCADE)
    lode_material = models.ForeignKey(MATERIAL, on_delete=models.CASCADE)
    lode_centroAtual = models.CharField(max_length=50, null=True, blank=True)
    lode_elementoPep = models.CharField(max_length=50, null=True, blank=True)
    lode_deposito = models.CharField(max_length=50, null=True, blank=True)
    lode_tipoAvaliacao = models.CharField(max_length=50, null=True, blank=True)
    lode_loteNm = models.CharField(max_length=50, null=True, blank=True)
    lode_numeroSerie = models.CharField(max_length=50, null=True, blank=True)
    lode_quantidadeOriginal = models.FloatField(null=True, blank=True)
    lode_quantidadeRetiradaDip = models.FloatField(null=True, blank=True)
    lode_quantidadeNaoLocalizada = models.FloatField(null=True, blank=True)
    lode_quantidadeAtual = models.FloatField(null=True, blank=True)
    # Coluna calculada -> Original - Retirada - Localizada
    lode_unidade = models.CharField(max_length=50, null=True, blank=True)
    lode_isaRetirada = models.CharField(max_length=50, null=True, blank=True)
    lode_dataRetirada = models.DateField(null=True, blank=True)
    lode_valorContabilUnitario = models.FloatField(null=True, blank=True)
    # Coluna calculada -> Valor contabil total / qtd original
    lode_valorContabilTotal = models.FloatField(null=True, blank=True)
    lode_valorContabilTotalAtual = models.FloatField(null=True, blank=True)
    # Coluna calculada -> Qtd ATUAL * Valor contabil unitario
    lode_valorReposicaoUnitario = models.FloatField(null=True, blank=True)
    # Coluna calculada -> Valor total reposicao / qtd original
    lode_valorTotalReposicao = models.FloatField(null=True, blank=True)
    lode_valorComparacaoVMA = models.FloatField(null=True, blank=True)
    # Coluna calculada -> Maior valor entre Valor Contabil Total e Valor Total Reposicao
    lode_vmaUnitario = models.FloatField(null=True, blank=True)
    # Coluna calculada -> VMA Total / qtd original
    lode_vmaTotal = models.FloatField(null=True, blank=True)
    # Coluna calculada -> VMA Parcial do lote (VMA total do material / VMA total do lote)
    lode_vmaPercentualLote = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if(self.lode_quantidadeOriginal):
            self.lode_quantidadeAtual = self.lode_quantidadeOriginal
            if(self.lode_quantidadeRetiradaDip):
                self.lode_quantidadeAtual = self.lode_quantidadeOriginal - self.lode_quantidadeRetiradaDip
            if(self.lode_quantidadeNaoLocalizada):
                self.lode_quantidadeAtual = self.lode_quantidadeAtual - self.lode_quantidadeNaoLocalizada
        if(self.lode_valorContabilTotal):
            if(self.lode_quantidadeOriginal):
                self.lode_valorContabilUnitario = self.lode_valorContabilTotal/self.lode_quantidadeOriginal
                if(self.lode_quantidadeAtual):
                    self.lode_valorContabilTotalAtual = self.lode_quantidadeAtual*self.lode_valorContabilUnitario
            if(self.lode_valorTotalReposicao):
                if(self.lode_valorTotalReposicao>self.lode_valorContabilTotal):
                    self.lode_valorComparacaoVMA = self.lode_valorTotalReposicao
                else:
                    self.lode_valorComparacaoVMA = self.lode_valorContabilTotal
        if(self.lode_quantidadeOriginal):
            if(self.lode_valorTotalReposicao):
                self.lode_valorReposicaoUnitario = self.lode_valorTotalReposicao/self.lode_quantidadeOriginal
            if(self.lode_vmaTotal):
                self.lode_vmaUnitario = self.lode_vmaTotal/self.lode_quantidadeOriginal    
        return super(LOTE_DET, self).save(*args,**kwargs)
   
    def __str__(self):
        return f"{self.id} : {self.lode_lote} - {self.lode_material}"

class COMPRADOR(models.Model):

    ESTADO = (
        ("RJ", "Rio de Janeiro"), ("MG", "Minas Gerais"), ("ES", "Rio de Janeiro"), ("SP", "São Paulo"),
        ("RS", "Rio Grande do Sul"), ("SC", "Santa Catarina"), ("PR", "Paraná"),
        ("GO", "Goias"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("DF", "Distrito Federal"),
        ("BA", "Bahia"), ("SE", "Sergipe"), ("AL", "Alagoas"), ("PE", "Pernambuco"), ("PB", "Paraíba"), ("RN", "Rio Grande do Norte"), ("CE", "Ceará"), ("PI", "Piau"), ("MA", "Maranhão"),
        ("PA", "Pará"), ("AP", "Amapá"), ("AM", "Amazonas"), ("AC", "Acre"), ("RR", "Roraima"), ("RO", "Rondonia")
    )

    comp_nomeComprador = models.CharField(max_length=50, null=True)
    comp_estado = models.CharField(max_length=50, choices=ESTADO)
    comp_cidade = models.CharField(max_length=50, null=True)
    comp_endereco = models.CharField(max_length=50, null=True) 
    comp_cnpj = models.CharField(max_length=50, null=False)
    comp_telefoneComercial = models.CharField(max_length=50, null=True)
    comp_telefoneResidencial = models.CharField(max_length=50, null=True)
    comp_email = models.CharField(max_length=50, null=True)
    comp_celular = models.CharField(max_length=50, null=True)
    comp_codigoSap = models.BigIntegerField(null=True)

    def __str__(self):
        return self.comp_nomeComprador


class DISPUTA_ABERTA(models.Model):
    diab_lote = models.ForeignKey(LOTE, on_delete=models.CASCADE)
    diab_comprador = models.ForeignKey(COMPRADOR, on_delete=models.SET_NULL, null=True)   # Ja temos as infos abaixo na tabela comprador
    diab_comunicadoVendaEnviado = models.CharField(max_length=50, null=True)
    diab_valorVendaLanceTotal = models.FloatField(null=True)
    diab_valorVendaSab = models.FloatField(null=True)
    diab_prazoPagamento = models.FloatField(null=True)
    diab_dataPagamento = models.DateField(null=True)
    diab_valorPago = models.FloatField(null=True)
    diab_email = models.CharField(max_length=50, null=True)     # RETIRAR
    diab_telefone = models.CharField(max_length=50, null=True)    # RETIRAR
    diab_lanceUnitario = models.FloatField(null=True)
    diab_lanceTotal = models.FloatField(null=True)

    def __str__(self):
        return f"{self.diab_lote} : {self.diab_comprador}"

class TESTES(models.Model):
    testeA = models.CharField(max_length=50, null=True)
    testeB = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.testeA

class HIST_LOTE(models.Model):
    hist_tipoAlteracao = models.CharField(max_length=50, null=False)
    hist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    hist_lote = models.ForeignKey(LOTE, on_delete=models.SET_NULL, null=True)
    hist_material = models.ForeignKey(LOTE_DET, on_delete=models.SET_NULL, null=True)
    hist_coluna = models.CharField(max_length=50, null=False)
    hist_dadoAnterior = models.CharField(max_length=50, null=True)
    hist_dadoNovo = models.CharField(max_length=50, null=True)
    hist_dataAlteracao = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.hist_dataAlteracao = timezone.now()
        return super(HIST_LOTE, self).save(*args,**kwargs)

    def __str__(self):
        return self.hist_tipoAlteracao