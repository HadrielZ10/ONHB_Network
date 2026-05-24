from django.contrib import admin
from .models import QUESTAO, ITEM

@admin.register(QUESTAO)
class QUESTAOAdmin(admin.ModelAdmin):
    list_display = ('id_questao', 'enunciado', 'id_fase')
    list_filter = ('id_fase__id_edicao', 'id_fase')
    search_fields = ('enunciado',)

admin.site.register(ITEM)