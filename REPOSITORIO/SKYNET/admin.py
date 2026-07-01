from django.contrib import admin
from .models import QUESTAO, ITEM, EDICAO, TIPO_QUESTAO, FASE

class ITEMInline(admin.TabularInline):
    """Permite visualizar e editar as alternativas direto dentro da página da Questão!"""
    model = ITEM
    extra = 4 # Já deixa 4 espacinhos prontos para as alternativas (A, B, C, D)

@admin.register(EDICAO)
class EdicaoAdmin(admin.ModelAdmin):
    list_display = ('id_edicao', 'num_edicao', 'ano_edicao')
    list_filter = ('ano_edicao',)
    search_fields = ('num_edicao',)

@admin.register(FASE)
class FaseAdmin(admin.ModelAdmin):
    list_display = ('id_fase', 'num_fase', 'id_edicao', 'tipo_fase')
    list_filter = ('tipo_fase', 'id_edicao')

# Tela de CRUD de Tipo de Questão
admin.site.register(TIPO_QUESTAO)

@admin.register(QUESTAO)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id_questao', 'num_questao', 'id_fase', 'id_tipo_questao', 'resumo_enunciado')
    list_filter = ('id_fase__id_edicao', 'id_fase', 'id_tipo_questao')
    search_fields = ('enunciado',)

    # Junta a Questão e suas Alternativas na mesma tela de cadastro/visualização
    inlines = [ITEMInline]

    def resumo_enunciado(self, obj):
        """Cria um resumo do enunciado para não quebrar o layout da tabela"""
        return obj.enunciado[:80] + '...' if len(obj.enunciado) > 80 else obj.enunciado
    resumo_enunciado.short_description = 'Enunciado (Trecho)'

@admin.register(ITEM)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'identificador', 'pontuacao', 'id_questao')
    list_filter = ('pontuacao', 'identificador') # Filtra por itens de 4 pontos, 2 pontos, ou pela letra (A, B...)
    search_fields = ('texto',) # <-- Corrigido aqui: removido os pontos extras