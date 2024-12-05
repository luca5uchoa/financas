from django.db import models
from django.contrib.auth.models import User

# Definindo categorias fixas em uma constante para consistência
CATEGORIAS_CHOICES = [
    ('Lazer', 'Lazer'),
    ('Saúde', 'Saúde'),
    ('Alimentação', 'Alimentação'),
    ('Transporte', 'Transporte'),
    ('Outros', 'Outros'),
]

class Receita(models.Model):
    descricao = models.CharField(max_length=200)  # Descrição da receita
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da receita
    data = models.DateField()  # Data da receita
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

class Reserva(models.Model):
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES)  # Categoria da reserva
    valor_reservado = models.DecimalField(max_digits=10, decimal_places=2)  # Valor reservado
    mes = models.PositiveSmallIntegerField()  # Mês da reserva
    ano = models.PositiveSmallIntegerField()  # Ano da reserva
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return f"{self.get_categoria_display()} - R$ {self.valor_reservado} - {self.mes}/{self.ano}"

class Despesa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da despesa
    data = models.DateField()  # Data da despesa
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES)  # Categoria da despesa
    descricao = models.CharField(max_length=200, blank=True)  # Descrição da despesa

    def __str__(self):
        return f"{self.descricao} - {self.get_categoria_display()} - R$ {self.valor}"
