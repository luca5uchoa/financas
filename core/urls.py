from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('cadastrar_receita/', views.cadastrar_receita, name='cadastrar_receita'),
    path('cadastrar_despesa/', views.cadastrar_despesa, name='cadastrar_despesa'),
    path('listar_receitas/', views.listar_receitas, name='listar_receitas'),
    path('listar_despesas/', views.listar_despesas, name='listar_despesas'),
]
