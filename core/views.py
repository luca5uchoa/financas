from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Receita, Despesa
from .forms import ReceitaForm, DespesaForm

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user  # Associa a receita ao usuário autenticado
            receita.save()
            return redirect('listar_receitas')
    else:
        form = ReceitaForm()
    return render(request, 'core/cadastrar_receita.html', {'form': form})

@login_required
def cadastrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user  # Associa a despesa ao usuário autenticado
            despesa.save()
            return redirect('listar_despesas')
    else:
        form = DespesaForm()
    return render(request, 'core/cadastrar_despesa.html', {'form': form})

@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user)  # Filtra receitas do usuário autenticado
    return render(request, 'core/listar_receitas.html', {'receitas': receitas})

@login_required
def listar_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user)  # Filtra despesas do usuário autenticado
    return render(request, 'core/listar_despesas.html', {'despesas': despesas})
