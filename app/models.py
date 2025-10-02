from django.db import models
import os

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    celular = models.CharField(max_length=255)
    plano = models.IntegerField(null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True) 
    data_nascimento = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calc_mensal(self):

        diaria = self.valor/(self.plano*4)
        return round(diaria, 2)

    def __str__(self):
        return self.nome
class Receber(models.Model):
    id_cliente = models.IntegerField(null=True)
    pagamento = models.DateField(null=True)
    vencimento = models.DateField(null=True)

    def __str__(self):
        return self.vencimento

class CategoriaTreino(models.Model):
    titulo = models.CharField(max_length=255)
    imagem = models.FileField(upload_to='imagens', null=True)
    grupo = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=255)

    def delete(self, *args, **kwargs):
        if self.imagem:
            if os.path.exists(self.imagem.path):
                os.remove(self.imagem.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
class Exercicios(models.Model):
    categoria = models.ForeignKey(CategoriaTreino, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=255)
    imagem = models.FileField(upload_to='imagens', null=True)

    def __str__(self):
        return self.categoria
    
class Treino(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=255)
    data_inicio = models.DateField(null=True)
    data_final = models.DateField(null=True)

    def __str__(self):
        return self.titulo

class treinoSemana(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.treino} for {self.titulo}"

class exercicioDia(models.Model):
    dia_semana = models.ForeignKey(treinoSemana, on_delete=models.CASCADE, null=True)
    exercicio = models.CharField(max_length=255)
    imagem = models.CharField(max_length=255, null=True)
    series = models.IntegerField(null=True)
    repeticoes = models.IntegerField(null=True)
    observacao = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.dia_semana} for {self.exercicio}"
