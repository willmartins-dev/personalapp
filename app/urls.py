from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('clientes', views.clientes, name='clientes'),
    path('view_clientes/<int:id>', views.view_clientes, name='view_clientes'),
    path('pagar_clientes/<int:id>', views.pagar_clientes, name='pagar_clientes'),
    path('atualizar_pagamento/<int:id>', views.atualizar_pagamento, name='atualizar_pagamento'),
    path('treinos', views.treinos, name='treinos'),
    path('view_treino/<int:id>', views.view_treino, name='view_treino'),
    path('treino_cliente/<int:id>', views.treino_cliente, name='treino_cliente'),
    path('view_treino_cliente/<int:id>', views.view_treino_cliente, name='view_treino_cliente'),
    path('view_exercicio/<int:id>', views.view_exercicio, name='view_exercicio'),
    path('atualiza_treinos/<int:id>', views.atualiza_treinos, name='atualiza_treinos'),
    path('buscar_exercicio/', views.buscar_exercicio, name='buscar_exercicio'),
    path('buscar_exercicio_sessao/', views.buscar_exercicio_sessao, name='buscar_exercicio_sessao'),
    path('upload/<int:id>', views.upload, name='upload'),
    path('exercicios', views.exercicios, name='exercicios'),
    path('delete_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
    path('delete_categoria_exercicio/<int:id>', views.delete_categoria_exercicio, name='delete_categoria_exercicio'),
    path('delete_exercicio/<int:id>', views.delete_exercicio, name='delete_exercicio'),
    path('delete_treino_cliente/<int:id>', views.delete_treino_cliente, name='delete_treino_cliente'),
    path('add_treino_cliente/<int:id>', views.add_treino_cliente, name='add_treino_cliente'),
    path('add_semana/<int:id>', views.add_semana, name='add_semana'),
    path('update_treino/<int:id>', views.update_treino, name='update_treino'),
    path('add_exercicio_sessao/<int:id>', views.add_exercicio_sessao, name='add_exercicio_sessao'),
    path('inserir_exercicio', views.inserir_exercicio, name='inserir_exercicio'),
    path('delete_sessao/<int:id>', views.delete_sessao, name='delete_sessao'),
    path('delete_exercicio_sessao/<int:id>', views.delete_exercicio_sessao, name='delete_exercicio_sessao'),
    path('lista_exercicio_sessao/<int:id>', views.lista_exercicio_sessao, name='lista_exercicio_sessao'),

]
