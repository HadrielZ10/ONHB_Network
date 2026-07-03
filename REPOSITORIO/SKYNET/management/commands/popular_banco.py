import csv
from django.core.management.base import BaseCommand
from SKYNET.models import EDICAO, FASE, TIPO_QUESTAO, QUESTAO, ITEM, DOCUMENTO, PERIODO, ANO_HISTORICO, TAG

class Command(BaseCommand):
    help = 'Esteira automatizada para importar os 5 arquivos CSV tratando as imperfeições de texto.'

    def handle(self, *args, **options):
        
        # -------------------------------------------------------------------------
        # PASSO 1: IMPORTAR EDIÇÕES
        # -------------------------------------------------------------------------
        csv_edicao = 'DADOS_EDICAO.csv'
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 1/5: Importando Edições..."))
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
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 2/5: Importando Tipos de Questão..."))
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
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 3/5: Importando Fases..."))
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
        self.stdout.write(self.style.WARNING(f"\n➔ Passo 4/5: Importando Questões..."))
        try:
            with open(csv_questao, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criadas, atualizadas = 0, 0
                for linha in leitor:
                    if not linha.get('id_questao'): continue
                    
                    fase_obj = FASE.objects.get(id_fase=int(linha['id_fase']))
                    tipo_obj = TIPO_QUESTAO.objects.get(id_tipo_questao=int(linha['id_tipo_questao']))
                    
                    enunciado_bruto = linha['enunciado']
                    enunciado_limpo = enunciado_bruto.strip()
                    
                    while enunciado_limpo.startswith('"') and enunciado_limpo.endswith('"'):
                        enunciado_limpo = enunciado_limpo[1:-1].strip()
                    
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


        # 🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩 ADICIONADO DAQUI EM DIANTE 🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩
        # -------------------------------------------------------------------------
        # PASSO 5: IMPORTAR ITENS / ALTERNATIVAS (Tratando aspas e quebras)
        # -------------------------------------------------------------------------
        csv_item = 'DADOS_ITEM.csv'
        self.stdout.write(self.style.WARNING(f"➔ Passo 5/5: Importando Itens/Alternativas..."))
        try:
            with open(csv_item, mode='r', encoding='utf-8-sig') as f:
                leitor = csv.DictReader(f, delimiter=';')
                criados, atualizados = 0, 0
                for linha in leitor:
                    # Proteção contra linhas vazias no fim do CSV
                    if not linha.get('id_item'): continue
                    
                    # Relaciona o ITEM com a sua respectiva QUESTAO (Chave Estrangeira)
                    questao_obj = QUESTAO.objects.get(id_questao=int(linha['id_questao']))
                    
                    # Higienização do texto da alternativa (remove aspas e quebras de linha)
                    texto_bruto = linha['texto'].strip()
                    while texto_bruto.startswith('"') and texto_bruto.endswith('"'):
                        texto_bruto = texto_bruto[1:-1].strip()
                    texto_limpo = texto_bruto.replace('\n', ' ').replace('\r', '')

                    # 🚩 ALTERAÇÃO AQUI: Tratamento para evitar o erro de pontuação vazia
                    try:
                        pontuacao_final = int(linha['pontuacao'])
                    except (ValueError, TypeError):
                        # Se estiver vazio ou não for um número válido, define como 0 por padrão
                        pontuacao_final = 0

                    # Cria ou atualiza no banco de dados de forma segura
                    obj, criado = ITEM.objects.update_or_create(
                        id_item=int(linha['id_item']),
                        defaults={
                            'identificador': linha['identificador'].strip(), # Ex: A, B, C, D
                            'texto': texto_limpo,
                            'pontuacao': pontuacao_final, # Usa a pontuação tratada aqui!
                            'id_questao': questao_obj
                        }
                    )
                    if criado: criados += 1
                    else: atualizados += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Itens -> Criados: {criados} | Atualizados: {atualizados}\n"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"✘ Arquivo não encontrado: {csv_item}"))
        # 🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩 FINAL DO BLOCO ADICIONADO 🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩

        