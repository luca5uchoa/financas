from django import forms
from django.core.exceptions import ValidationError
from .models import Receita, Despesa, Reserva, CATEGORIAS_CHOICES
from django.contrib.auth.models import User

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})  # Campo de data com seletor de calendário
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['valor', 'data', 'categoria', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),  # Campo de data com seletor de calendário
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove 'user' de kwargs
        super().__init__(*args, **kwargs)  # Chama o __init__ da classe pai

        # Corrigido para usar a constante global
        self.fields['categoria'].choices = CATEGORIAS_CHOICES

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['categoria', 'valor_reservado', 'mes', 'ano']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].choices = CATEGORIAS_CHOICES  # Usando a constante CATEGORIAS_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        mes = cleaned_data.get("mes")
        ano = cleaned_data.get("ano")

        if categoria and mes and ano:
            # Verifica se já existe uma reserva com a mesma categoria, mês e ano, excluindo a própria instância em caso de edição
            reservas_existentes = Reserva.objects.filter(
                categoria=categoria,
                mes=mes,
                ano=ano
            ).exclude(pk=self.instance.pk)
            if reservas_existentes.exists():
                raise ValidationError(
                    f"Já existe uma reserva para a categoria '{categoria}' no mês {mes}/{ano}. Pode altera-la na página de metas"
                )

        return cleaned_data
