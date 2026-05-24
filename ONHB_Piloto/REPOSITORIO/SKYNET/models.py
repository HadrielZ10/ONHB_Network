from django.db import models

class EDICAO(models.Model):

    id_edicao = models.AutoField(primary_key=True)

    num_edicao = models.IntegerField(verbose_name="Número da Edição")

    ano_edicao = models.IntegerField(verbose_name="Ano da Edição")

def __str__(self):
    return f"{self.num_edicao}ª ONHB ({self.ano_edicao})"

class FASE(models.Model):

    id_fase = models.AutoField(primary_key=True)

    num_fase = models.IntegerField(verbose_name="Número da Fase")

    tipo_fase = models.IntegerField(verbose_name="Tipo da Fase")

    id_edicao = models.ForeignKey(
        EDICAO,
        on_delete=models.CASCADE,
        related_name='fases',
        verbose_name="Edição")

def __str__(self):
    return f"{self.num_fase} - {self.id_edicao}"

class TIPO_QUESTAO(models.Model):

    id_tipo_questao = models.AutoField(primary_key=True)

    tipo_nome = models.CharField(verbose_name="Tipo de Questao")

def __str__(self):
    return f"{self.tipo_nome}"

class QUESTAO(models.Model):

    id_questao = models.AutoField(primary_key=True)

    num_questao = models.IntegerField(verbose_name="Número da Questão")

    enunciado = models.TextField(verbose_name="Enunciado da Questão")

    id_fase = models.ForeignKey(
        FASE,
        on_delete=models.CASCADE,
        related_name='Questoes',
        verbose_name="Fase")
    
    id_tipo_questao = models.ForeignKey(
        TIPO_QUESTAO,
        on_delete=models.CASCADE,
        related_name='Questoes',
        verbose_name="Tipo De Questao")

def __str__(self):
    return f"{self.num_questao} - {self.enunciado}"

class ITEM(models.Model):

    id_item = models.AutoField(primary_key=True)

    pontuacao = models.IntegerField(verbose_name="Pontuação do Item")

    identificador = models.CharField(verbose_name="Identificador")

    enunciado_item = models.TextField(verbose_name="Enunciado do Item")

    id_questao = models.ForeignKey(
        QUESTAO,
        on_delete=models.CASCADE,
        related_name='Tipos',
        verbose_name="Questoes")

def __str__(self):
    return f"{self.pontuacao} - {self.identificador} - {self.texto}"