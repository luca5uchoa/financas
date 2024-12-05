from django.urls import path
from core.views import home, listar_reservas, listar_reservas_por_categoria, listar_receitas, listar_despesas, cadastrar_receita, cadastrar_despesa, cadastrar_reserva, editar_reserva

urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('cadastrar_receita/', cadastrar_receita, name='cadastrar_receita'),
    path('cadastrar_despesa/', cadastrar_despesa, name='cadastrar_despesa'),
    path('listar_receitas/', listar_receitas, name='listar_receitas'),
    path('listar_despesas/', listar_despesas, name='listar_despesas'),
    path('cadastrar_reserva/', cadastrar_reserva, name='cadastrar_reserva'),
    path('listar_reservas/', listar_reservas, name='listar_reservas'),
    path('reservas/categoria/<str:categoria>/', listar_reservas_por_categoria, name='listar_reservas_por_categoria'),  # Rota para reservas por categoria
    path('editar_reserva/<int:id>/', editar_reserva, name='editar_reserva'),
]
