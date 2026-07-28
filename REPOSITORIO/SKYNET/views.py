from django.shortcuts import get_object_or_404, render
from .models import EDICAO, FASE, QUESTAO, ITEM, TAG, PERIODO, DOCUMENTO, ANO_HISTORICO,TIPO_QUESTAO



def escolher_edicao(request):
    # Busca todas as edições do banco de dados ordenadas pelo ano mais recente
    edicoes = EDICAO.objects.all().order_by('-ano_edicao')
    
    # Envia as edições para dentro do arquivo HTML através do dicionário de contexto
    return render(request, 'SKYNET/escolher_edicao.html', {'edicoes': edicoes})

def escolher_fase(request, edicao_id):
    # 1. Busca a edição clicada ou dá erro 404 se o ID não existir
    edicao = get_object_or_404(EDICAO, id_edicao=edicao_id)
    
    # 2. Busca apenas as fases que estão vinculadas a essa edição
    fases = FASE.objects.filter(id_edicao=edicao).order_by('num_fase')
    
    # 3. Envia a edição e as fases para o novo arquivo HTML
    return render(request, 'SKYNET/escolher_fase.html', {
        'edicao': edicao, 
        'fases': fases
    })

def listar_questoes(request, fase_id):

    # 1. Busca a fase clicada ou dá erro 404 se não existir
    fase = get_object_or_404(FASE, id_fase=fase_id)
    
    # 2. Busca todas as questões que pertencem a essa fase, ordenadas pelo número da questão
    questoes = QUESTAO.objects.filter(id_fase=fase).order_by('num_questao')

    busca_tipo = request.GET.get('tipos')
    busca_periodo = request.GET.get('periodos')
    busca_documento = request.GET.get('documento')
    busca_tag = request.GET.get('tags')
    busca_ano = request.GET.get('anos')
            
    # 3. Aplica os filtros na lista de QUESTÕES encadeando no QuerySet 'questoes'
    if busca_documento:
        # Filtra questões associadas a documentos com o nome buscado
        questoes = questoes.filter(documentos__nome_documento__icontains=busca_documento)
            
    if busca_tipo:
        # Filtra pelo tipo da questão (ex: chave estrangeira id_tipo_questao)
        questoes = questoes.filter(id_tipo_questao__tipo_nome__iexact=busca_tipo)
            
    if busca_periodo:
        # Filtra questões associadas a um período específico
        questoes = questoes.filter(periodos__periodo_nome__iexact=busca_periodo)

    if busca_tag:
        questoes = questoes.filter(tags__tag_nome__icontains=busca_tag)

    if busca_ano:
        questoes = questoes.filter(anos__ano__icontains=busca_ano)

    questoes = questoes.distinct()
            
    # 3. Envia os dados para o novo HTML
    return render(request, 'SKYNET/listar_questoes.html', {
        'fase': fase,
        'questoes': questoes
    })

def detalhes_questao(request, questao_id):
            
    # 1. Busca a questão clicada ou dá erro 404 se não existir
    questao = get_object_or_404(QUESTAO, id_questao=questao_id)
    
    # 2. Busca todas as alternativas (itens) conectadas a essa questão específica
    alternativas = ITEM.objects.filter(id_questao=questao).order_by('identificador')
    
    
    # 3. Envia a questão e as alternativas para o HTML de detalhes
    return render(request, 'SKYNET/detalhes_questao.html', {
        'questao': questao,
        'alternativas': alternativas
    })