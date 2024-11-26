from django.db import models
from django.contrib.auth.models import User

class Receita(models.Model):
    descricao = models.CharField(max_length=200)  # Descrição da receita
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da receita
    data = models.DateField()  # Data da receita
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

class Despesa(models.Model):
    descricao = models.CharField(max_length=200)  # Descrição da despesa
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da despesa
    data = models.DateField()  # Data da despesa
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
