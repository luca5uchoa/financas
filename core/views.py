from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from .models import Receita, Despesa, Reserva, Categoria
from .forms import ReceitaForm, DespesaForm, ReservaForm

@login_required
def home(request):
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    # Calcular receitas e despesas do mês atual
    receitas_mes = Receita.objects.filter(
        usuario=request.user, data__month=mes_atual, data__year=ano_atual
    ).aggregate(total=Sum('valor'))['total'] or 0

    despesas_mes = Despesa.objects.filter(
        usuario=request.user, data__month=mes_atual, data__year=ano_atual
    ).aggregate(total=Sum('valor'))['total'] or 0

    # Consultar reservas e calcular total reservado, gasto e restante
    reservas = Reserva.objects.filter(
        usuario=request.user, mes=mes_atual, ano=ano_atual
    )

    reservas_com_dados = []
    for reserva in reservas:
        # Total gasto pela categoria da reserva
        total_gasto = Despesa.objects.filter(
            usuario=request.user,
            categoria=reserva.categoria,  # Alteração aqui
            data__month=mes_atual,
            data__year=ano_atual
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        # Calculando o saldo restante da reserva
        saldo_restante = reserva.valor_reservado - total_gasto
        
        reservas_com_dados.append({
            'reserva': reserva,
            'total_gasto': total_gasto,
            'saldo_restante': saldo_restante,
        })

    # Passando os dados para o template
    context = {
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'reservas_por_categoria': reservas_com_dados,
    }

    return render(request, 'core/home.html', context)

# Funções para cadastrar receita, despesa e reserva permanecem as mesmas
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
def listar_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('categoria')
    return render(request, 'core/listar_reservas.html', {'reservas': reservas})
