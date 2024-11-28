from django import forms
from .models import Receita, Despesa, Reserva, Categoria
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
        widget=forms.Select(attrs={'class': 'form-control'})
    

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})  # Campo de data com seletor de calendário
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove 'user' de kwargs
        super().__init__(*args, **kwargs)  # Chama o __init__ da classe pai

        if user:
            # Filtra as categorias associadas ao usuário
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
        else:
            # Se não houver usuário, não exibe categorias
            self.fields['categoria'].queryset = Categoria.objects.none()

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['categoria', 'valor_reservado', 'mes', 'ano']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove 'user' de kwargs para não causar erro
        super().__init__(*args, **kwargs)

        if user:
            # Associa o usuário à instância do formulário, garantindo que a reserva seja associada ao usuário correto
            self.instance.usuario = user
            # Filtra as categorias associadas ao usuário
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
        else:
            # Se não houver usuário, não exibe categorias (ou pode definir um queryset padrão)
            self.fields['categoria'].queryset = Categoria.objects.none()
