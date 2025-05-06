import pandas as pd
from django.core.management.base import BaseCommand
from materiais.models import Unidade

class Command(BaseCommand):
    help = 'Importa unidades de um arquivo Excel para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', type=str, help='Caminho completo para o arquivo Excel de Unidades.')

    def handle(self, *args, **options):
        arquivo = options['arquivo']
        try:
            df = pd.read_excel(arquivo)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao ler o arquivo: {e}'))
            return

        # Considerando que o Excel possui as colunas "Unidade" e "Descricao"
        for index, row in df.iterrows():
            nome_unidade = row.get('Unidade')
            if not nome_unidade:
                continue  # Ignora linhas sem valor na coluna "Unidade"

            descricao = row.get('Descricao', '')
            ativo = row.get('ativo', True)
            unidade_obj, created = Unidade.objects.get_or_create(
                unidade=nome_unidade,
                defaults={
                    'descricao': descricao,
                    'ativo': ativo
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Unidade "{unidade_obj}" criada com sucesso.'))
            else:
                self.stdout.write(f'Unidade "{unidade_obj}" já existe.')


#/home/dbsistem/sgmtestes/manage.py import_unidades /home/dbsistem/sgmtestes/Arquivos/Unidades.xlsx