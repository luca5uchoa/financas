from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)  # Nome da categoria
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return self.nome

class Receita(models.Model):
    descricao = models.CharField(max_length=200)  # Descrição da receita
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da receita
    data = models.DateField()  # Data da receita
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Associação com o usuário

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

class Reserva(models.Model):
    # Definindo as categorias como opções predefinidas para a reserva
    CATEGORIA_CHOICES = [
        ('saude', 'Saúde'),
        ('lazer', 'Lazer'),
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('outros', 'Outros'),
    ]
    
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        default='outros',  # Categoria padrão caso o usuário não escolha
    )  # Categoria da reserva

    valor_reservado = models.DecimalField(max_digits=10, decimal_places=2)  # Valor reservado
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Valor gasto
    mes = models.IntegerField()  # Mês da reserva
    ano = models.IntegerField()  # Ano da reserva
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Adicionando o campo usuario

    @property
    def saldo_restante(self):
        # Calcula o saldo restante, subtraindo as despesas da categoria
        total_despesas_categoria = Despesa.objects.filter(
            categoria=self.categoria,  # Filtra pela categoria da reserva
            data__month=self.mes,  # Mês da despesa
            data__year=self.ano,   # Ano da despesa
            usuario=self.usuario  # Filtra pelo usuário
        ).aggregate(models.Sum('valor'))['valor__sum'] or 0  # Soma das despesas ou 0 se não houver
        return self.valor_reservado - total_despesas_categoria

    def __str__(self):
        return f"Reserva em {self.get_categoria_display()}: R$ {self.valor_reservado} (Saldo: R$ {self.saldo_restante})"


class Despesa(models.Model):
    CATEGORIAS = [
        ('lazer', 'Lazer'),
        ('saude', 'Saúde'),
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('habituacao', 'Habitação'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)  # Campo para escolher a categoria
    descricao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.get_categoria_display()} - {self.valor}"
