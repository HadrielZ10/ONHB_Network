import csv
from django.core.management.base import BaseCommand
from SKYNET.models import EDICAO, FASE, TIPO_QUESTAO, QUESTAO

class Command(BaseCommand):
    help = 'Esteira automatizada para importar os 4 arquivos CSV tratando as imperfeições de texto.'

    def handle(self, *args, **options):
        
        # -------------------------------------------------------------------------
        # PASSO 1: IMPORTAR EDIÇÕES
        # -------------------------------------------------------------------------
        csv_edicao = 'DADOS_EDICAO.csv'
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 1/4: Importando Edições..."))
        try:
            with open(csv_edicao, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criadas, atualizadas = 0, 0
                for linha in leitor:
                    if not linha.get('id_edicao'): continue
                    
                    obj, criado = EDICAO.objects.update_or_create(
                        id_edicao=int(linha['id_edicao']),
                        defaults={
                            'num_edicao': int(linha['num_edicao']),
                            'ano_edicao': int(linha['ano_edicao'])
                        }
                    )
                    if criado: criadas += 1
                    else: atualizadas += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Edições -> Criadas: {criadas} | Atualizadas: {atualizadas}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"✘ Arquivo não encontrado: {csv_edicao}"))

        # -------------------------------------------------------------------------
        # PASSO 2: IMPORTAR TIPOS DE QUESTÃO
        # -------------------------------------------------------------------------
        csv_tipo = 'DADOS_TIPO_QUESTAO.csv'
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 2/4: Importando Tipos de Questão..."))
        try:
            with open(csv_tipo, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criadas, atualizadas = 0, 0
                for linha in leitor:
                    if not linha.get('id_tipo_questao'): continue
                    
                    obj, criado = TIPO_QUESTAO.objects.update_or_create(
                        id_tipo_questao=int(linha['id_tipo_questao']),
                        defaults={'tipo_nome': linha['tipo_nome'].strip()}
                    )
                    if criado: criadas += 1
                    else: atualizadas += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Tipos -> Criados: {criadas} | Atualizados: {atualizadas}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"✘ Arquivo não encontrado: {csv_tipo}"))

        # -------------------------------------------------------------------------
        # PASSO 3: IMPORTAR FASES
        # -------------------------------------------------------------------------
        csv_fase = 'DADOS_FASE.csv'
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 3/4: Importando Fases..."))
        try:
            with open(csv_fase, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criadas, atualizadas = 0, 0
                for linha in leitor:
                    if not linha.get('id_fase'): continue
                    
                    edicao_obj = EDICAO.objects.get(id_edicao=int(linha['id_edicao']))
                    
                    obj, criado = FASE.objects.update_or_create(
                        id_fase=int(linha['id_fase']),
                        defaults={
                            'num_fase': int(linha['num_fase']),
                            'tipo_fase': linha['tipo_fase'].strip(),
                            'id_edicao': edicao_obj
                        }
                    )
                    if criado: criadas += 1
                    else: atualizadas += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Fases -> Criadas: {criadas} | Atualizadas: {atualizadas}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"✘ Arquivo não encontrado: {csv_fase}"))

        # -------------------------------------------------------------------------
        # PASSO 4: IMPORTAR QUESTÕES (Com Limpeza de Caracteres)
        # -------------------------------------------------------------------------
        csv_questao = 'DADOS_QUESTAO.csv'
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 4/4: Importando Questões..."))
        try:
            with open(csv_questao, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criadas, atualizadas = 0, 0
                for linha in leitor:
                    if not linha.get('id_questao'): continue
                    
                    fase_obj = FASE.objects.get(id_fase=int(linha['id_fase']))
                    tipo_obj = TIPO_QUESTAO.objects.get(id_tipo_questao=int(linha['id_tipo_questao']))
                    
                    # --- ALGORITMO DE LIMPEZA DO ENUNCIADO ---
                    enunciado_bruto = linha['enunciado']
                    
                    # Remove quebras de linha e espaços bobos nas pontas extremas
                    enunciado_limpo = enunciado_bruto.strip()
                    
                    # Remove sequências de aspas externas (seja 1, 2 ou 3 aspas seguidas nas pontas)
                    while enunciado_limpo.startswith('"') and enunciado_limpo.endswith('"'):
                        enunciado_limpo = enunciado_limpo[1:-1].strip()
                    
                    # Substitui quebras de linha internas por espaços para não quebrar o layout do HTML
                    enunciado_limpo = enunciado_limpo.replace('\n', ' ').replace('\r', '')

                    obj, criado = QUESTAO.objects.update_or_create(
                        id_questao=int(linha['id_questao']),
                        defaults={
                            'num_questao': int(linha['num_questao']),
                            'enunciado': enunciado_limpo,
                            'id_fase': fase_obj,
                            'id_tipo_questao': tipo_obj
                        }
                    )
                    
                    if criado: 
                        criadas += 1
                    else: 
                        atualizadas += 1
                        
                self.stdout.write(self.style.SUCCESS(f"✔ Questões -> Criadas: {criadas} | Atualizadas: {atualizadas}\n"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"✘ Arquivo não encontrado: {csv_questao}"))