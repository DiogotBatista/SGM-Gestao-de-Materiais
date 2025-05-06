import pandas as pd
from django.core.management.base import BaseCommand
from materiais.models import GrupoMaterial

class Command(BaseCommand):
    help = 'Importa grupos de materiais de um arquivo Excel para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', type=str, help='Caminho completo para o arquivo Excel de grupos de materiais.')

    def handle(self, *args, **options):
        arquivo = options['arquivo']
        try:
            df = pd.read_excel(arquivo)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao ler o arquivo: {e}'))
            return

        # Itera pelas linhas do DataFrame, considerando a coluna "Grupo_materiais"
        for index, row in df.iterrows():
            nome_grupo = row.get('Grupo_materiais')
            if not nome_grupo:
                continue  # ignora linhas sem valor na coluna

            # Por padrão, definimos 'ativo' como True
            grupo, created = GrupoMaterial.objects.get_or_create(
                nome=nome_grupo,
                defaults={'ativo': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo}" criado com sucesso.'))
            else:
                self.stdout.write(f'Grupo "{grupo}" já existe.')


#/home/dbsistem/sgmtestes/manage.py import_grupos /home/dbsistem/sgmtestes/Arquivos/Grupos_material.xlsx