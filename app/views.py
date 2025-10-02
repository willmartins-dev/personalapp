from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from .models import Cliente, CategoriaTreino, Exercicios, Receber, Treino, treinoSemana, exercicioDia
from .forms import FormUpload
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from datetime import date, timedelta

def home(request):

    alunos = Cliente.objects.count()
    soma_total = Cliente.objects.aggregate(tabela=Sum('valor'))

    context = {
        'alunos':alunos,
        'total': soma_total['tabela'],
    }

    return render(request, 'inicio/home.html', context)

def clientes(request):
    if request.method == 'GET':

        cliente = Cliente.objects.all()
        soma_total = Cliente.objects.aggregate(tabela=Sum('valor'))


        context = {
            'cliente':cliente,
            'total':soma_total['tabela'],
        }

        return render(request, 'clientes/home.html', context)
    
    elif request.method == 'POST':

        cliente = Cliente(
            nome = request.POST.get('nome'),
            celular = request.POST.get('celular'),
            plano = request.POST.get('plano'),
            valor = request.POST.get('valor'),
        )

        cliente.save()

        return redirect('clientes')
    
def treino_cliente(request,id):
    cliente = Cliente.objects.get(id=id)
    treinos = Treino.objects.filter(cliente_id=id)

    if request.method == 'GET':

        context={
            'cliente':cliente,
            'treinos':treinos,
        }

        return render(request, 'clientes/treino.html', context)
    
    if request.method == 'POST':

        treino = Treino(
        
            cliente_id = id,
            titulo = request.POST.get('titulo'),
            data_inicio = request.POST.get('inicio'),
            data_final = request.POST.get('final'),
        )

        treino.save()
        return redirect('treino_cliente', id)
    
def view_treino_cliente(request, id):
    
    if request.method == 'GET':
        treino = Treino.objects.get(id=id)
        sessao = treinoSemana.objects.filter(treino_id=id)
        id_sessao = list(sessao.values_list('id', flat=True))
        exercicio = exercicioDia.objects.filter(dia_semana__in=id_sessao)

        context = {
            'treino':treino,
            'sessao':sessao,
            'exercicios':exercicio,
        }
    return render(request, 'clientes/view_treino.html', context)
    
def add_treino_cliente(request,id):
     
    if request.method == 'GET':
        treino = Treino.objects.get(id=id)
       
        sessao_treino = treinoSemana.objects.filter(treino_id=id)
        context = {
            'treino':treino,
            'sessao_treino':sessao_treino,   
            
        }
        
        return render(request, 'clientes/add_treino.html', context)
    
    elif request.method == 'POST':
        add_dia = treinoSemana(
        titulo = request.POST.get('titulo'),
        treino_id = id,
        )
        add_dia.save()

        return redirect('add_treino_cliente', id)
    

def add_semana(request, id):
    treino = Treino.objects.filter(cliente_id=id)
    
    if request.method == 'POST':
        pass
        
    
    
def add_exercicio_sessao(request,id):
    if request.method == 'GET':

        exercicios = Exercicios.objects.all()[:10]

        treino_semana = treinoSemana.objects.get(id=id)
    
        context={
            'exercicios':exercicios,
            'treino_semana': treino_semana,
        }
        
        return render(request, 'clientes/add_exercicio.html', context)
def lista_exercicio_sessao(request,id):
    lista_exercicio = exercicioDia.objects.filter(dia_semana = id)

    if request.method == 'GET':
        context={
            'lista_exercicio':lista_exercicio
        }

    return render(request, 'clientes/lista_exercicio_ajax.html', context)

def update_treino(request, id):
    update_treino = exercicioDia.objects.get(id=id)
    if request.method == 'POST':
        update_treino.exercicio = request.POST.get('exercicio')
        update_treino.series = request.POST.get('series')
        update_treino.repeticoes = request.POST.get('repeticoes')
        update_treino.observacao = request.POST.get('observacoes')
        update_treino.save()

    return HttpResponse('ok')

@csrf_exempt
def inserir_exercicio(request):

    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        add_exercicio_sessao = exercicioDia(
            dia_semana_id = data.get('id'),
            exercicio = data.get('exercicio'),
            imagem = data.get('imagem'),
        )
        add_exercicio_sessao.save()
    return JsonResponse({'mensagem':data.get('id')})
    

@csrf_exempt
def delete_exercicio_sessao(request, id):

    if request.method == 'POST':

        delete_exercicio = exercicioDia(
            id = id
        )
        delete_exercicio.delete()

        return render(request, 'clientes/lista_exercicio_ajax.html')
    
def delete_sessao(request, id):
    sessao = treinoSemana.objects.get(id=id)
    sessao.delete()

    return redirect('add_treino_cliente', id=sessao.treino_id)

def delete_treino_cliente(request,id):
    
    treino = Treino.objects.get(id=id)
    treino_semana = treinoSemana.objects.filter(treino_id = id)
    exercicios = exercicioDia.objects.filter(dia_semana_id=id)

    treino.delete()
    treino_semana.delete()
    exercicios.delete()

    return redirect('treino_cliente', id=treino.cliente_id)

def view_clientes(request,id):
    
    cliente = Cliente.objects.get(id=id)
    receber = Receber.objects.filter(id_cliente=id)

    if request.method == 'GET':

        agora = date.today().year
        nascimento = cliente.data_nascimento
        if not nascimento:
            idade = ''
        elif nascimento:
            idade=f'({agora-nascimento.year} anos)'

        if not receber.exists():
            receber_dados=''
            data_vencimento = ''
        else:
            receber_dados = Receber.objects.get(id_cliente=id)
            
            if not receber_dados.vencimento:
                data_vencimento = ''
            else:
                data_vencimento = receber_dados.pagamento

        

        context={
            'cliente':cliente,
            'idade':idade,
            'receber_dados':receber_dados,
            'data_vencimento':data_vencimento,
        }

        return render(request, 'clientes/clientes.html', context)
    elif request.method == 'POST':

        valor = request.POST.get('valor').replace(',', '.')
        cliente.nome = request.POST.get('nome')
        cliente.celular = request.POST.get('celular')
        cliente.plano=request.POST.get('plano')
        cliente.valor=float(valor)
        cliente.data_nascimento=request.POST.get('data_nascimento')
        
        cliente.save()

        return redirect('view_clientes')
    
def pagar_clientes(request, id):
    
    agora = date.today()
    mes_ano = agora.strftime('%Y-%m')
    dias = timedelta(days=30)
    proximo_pagamento = agora+dias

    if request.method == 'POST':
        pagamento = Receber(
            id_cliente = id,
            vencimento = f'{mes_ano}-{request.POST.get('vencimento')}',
            pagamento = str(date.strftime(proximo_pagamento, '%Y-%m-%d'))
        )
        pagamento.save()

    return redirect('view_clientes', id)

def atualizar_pagamento(request, id):

    pagar = Receber.objects.get(id_cliente=id)
    agora = date.today()
    dias = timedelta(days=30)
    proximo_pagamento = agora+dias
    
    mes_ano = agora.strftime('%Y-%m')

    if request.method == 'POST':
        pagar.vencimento = str(f'{mes_ano}-{request.POST.get('vencimento')}')
        pagar.pagamento = str(date.strftime(proximo_pagamento, '%Y-%m-%d'))
        pagar.save()
    return HttpResponse()
    #return redirect('view_clientes', id)
    
def delete_cliente(request, id):

    if request.method == 'GET':

        cliente = Cliente.objects.get(id=id)

        cliente.delete()

        return redirect('clientes')
    
def treinos(request):
    form = FormUpload(request.POST, request.FILES)

    if request.method == 'GET':
        form = FormUpload()
        categoria_treino = CategoriaTreino.objects.all().order_by('titulo')

        context = {
            'categoria_treino':categoria_treino,
            'form':form,
        }

        return render(request, 'treino/home.html', context)
    
    elif request.method == 'POST':

        categoria_treino = CategoriaTreino(
            titulo = request.POST.get('titulo'),
            grupo = request.POST.get('grupo'),
            imagem = request.FILES.get('imagem'),
            tipo = request.POST.get('tipo'),
        )
        categoria_treino.save()
        #upload

        return redirect('treinos')
    
def view_treino(request, id):

    dados = CategoriaTreino.objects.get(id=id)

    context = {
        'dados':dados
    }

    return render(request, 'treino/view.html', context)

def atualiza_treinos(request, id):

    categoria_treino = CategoriaTreino.objects.get(id=id)

    if request.method == 'POST':
        categoria_treino.titulo = request.POST.get('titulo')
        categoria_treino.tipo = request.POST.get('tipo')
        categoria_treino.grupo = request.POST.get('grupo')
        categoria_treino.save()
        return redirect('treino')
    
def deleta_treino(request, id):
    categoria_treino = CategoriaTreino.objects.get(id=id)



    
def exercicios(request):
    if request.method == 'POST':
        
        categoria_id = request.POST.get('categoria')
        titulo = request.POST.get('exercicio')
        imagem = request.FILES.get('imagem')
        exercicio = Exercicios(nome = titulo, categoria_id = categoria_id, imagem = imagem)
        
        exercicio.save()

        
        return redirect('treinos')
    
def view_exercicio(request, id):
    if request.method == 'POST':
        
        categoria_id = request.POST.get('categoria')
        titulo = request.POST.get('exercicio')
        imagem = request.FILES.get('imagem')
        exercicio = Exercicios(nome = titulo, categoria_id = categoria_id, imagem = imagem)
        
        exercicio.save()
        return redirect('view_exercicio', id)
    else:
        exercicios = Exercicios.objects.filter(categoria_id = id)
        categoria = CategoriaTreino.objects.filter(id=id)
        context={
            'exercicio':exercicios,
            'categoria':categoria,
        }

        return render(request, 'treino/view_exercicio.html', context)

def delete_exercicio(request, id):

    del_exercicio = Exercicios.objects.get(id=id)
    categoria_id = del_exercicio.categoria_id
    del_exercicio.delete()
    
    return redirect('view_exercicio', categoria_id)

def upload(request,id):

    categoria_treino = CategoriaTreino.objects.get(id=id)
    
    if request.method == 'POST':
       
        file = request.FILES.get('upload')
        categoria_treino.imagem = file
        categoria_treino.save()
        return redirect('treinos')



def buscar_exercicio(request):
    
    termo = request.GET.get('termo')
    resultados = list(CategoriaTreino.objects.filter(titulo__icontains=termo).values('titulo')) 
    return JsonResponse(resultados, safe=False)

def buscar_exercicio_sessao(request):

    termo = request.GET.get('termo')
    id_sessao = request.GET.get('id_sessao')
    if termo:
        
        exercicios = list(Exercicios.objects.filter(nome__icontains=termo).values('id','nome', 'categoria', 'imagem'))
        context = {
            'exercicios':exercicios,
            'id_sessao':id_sessao,
        }
        return render(request, 'clientes/buscar_exercicio_sessao.html', context)
    else:
        return JsonResponse({'mensagem':'Nenhum resultado encontrado!'})


def delete_categoria_exercicio(request, id):

    categoria_exercicio = CategoriaTreino.objects.get(id=id)
    categoria_exercicio.delete()
    
    return redirect('treinos')