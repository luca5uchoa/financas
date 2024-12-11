import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from .models import Receita, Despesa, Reserva
from .forms import ReceitaForm, DespesaForm, ReservaForm
from django.utils import timezone

# Função para calcular o saldo restante de cada categoria
def get_saldo_restante():
    reservas = Reserva.objects.all()
    saldos = []
    for reserva in reservas:
        valor_gasto = Despesa.objects.filter(categoria=reserva.categoria).aggregate(Sum('valor'))['valor__sum'] or 0
        saldo_restante = reserva.valor_reservado - valor_gasto
        saldos.append({
            'categoria': reserva.categoria,
            'saldo_restante': saldo_restante,
            'valor_gasto': valor_gasto,
            'valor_reservado': reserva.valor_reservado,
            'percentual': (valor_gasto / reserva.valor_reservado) * 100 if reserva.valor_reservado > 0 else 0
        })
    return saldos

@login_required
def home(request):
    # Calcular as receitas e despesas do mês
    receitas_mes = Receita.objects.filter(data__month=timezone.now().month).aggregate(total=Sum('valor'))['total'] or 0
    despesas_mes = Despesa.objects.filter(data__month=timezone.now().month).aggregate(total=Sum('valor'))['total'] or 0
    
    # Calcular o saldo
    saldo = receitas_mes - despesas_mes
    
    # Calcular o saldo por categoria
    reservas_por_categoria = get_saldo_restante()  # Chama a função para pegar os saldos restantes das categorias

    # Extrair as informações necessárias para o gráfico
    categorias_nome = [reserva['categoria'] for reserva in reservas_por_categoria]
    valores_gastos = [reserva['valor_gasto'] for reserva in reservas_por_categoria]
    valores_restantes = [reserva['saldo_restante'] for reserva in reservas_por_categoria]
    
    # Contexto para o template
    context = {
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'saldo': saldo,
        'reservas_por_categoria': reservas_por_categoria,
        'categorias_nome': categorias_nome,
        'valores_gastos': valores_gastos,
        'valores_restantes': valores_restantes,
    }

    return render(request, 'core/home.html', context)

@login_required
def listar_reservas(request):
    # Agrupa as reservas por categoria e calcula o total reservado
    categorias = (
        Reserva.objects.filter(usuario=request.user)
        .values('categoria')
        .annotate(total_reservado=Sum('valor_reservado'))
        .order_by('categoria')
    )

    # Carrega todas as reservas do usuário
    reservas = Reserva.objects.filter(usuario=request.user)

    # Contexto para o template
    context = {
        'categorias': categorias,
        'reservas': reservas,
    }

    return render(request, 'core/listar_reservas.html', context)

@login_required
def listar_reservas_por_categoria(request, categoria):
    # Filtro das reservas por categoria e usuário
    reservas = Reserva.objects.filter(usuario=request.user, categoria=categoria)
    return render(request, 'core/listar_reservas_por_categoria.html', {'reservas': reservas, 'categoria': categoria})

@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
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
            despesa.usuario = request.user
            despesa.save()
            return redirect('listar_despesas')
    else:
        form = DespesaForm()
    return render(request, 'core/cadastrar_despesa.html', {'form': form})

@login_required
def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('listar_reservas')
    else:
        form = ReservaForm()
    return render(request, 'core/cadastrar_reserva.html', {'form': form})

@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user)
    return render(request, 'core/listar_receitas.html', {'receitas': receitas})

@login_required
def listar_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'core/listar_despesas.html', {'despesas': despesas})

@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('listar_reservas')
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'core/editar_reserva.html', {'form': form, 'reserva': reserva})
