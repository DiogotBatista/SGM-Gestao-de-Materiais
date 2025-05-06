import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from materiais.models import Material, Unidade, GrupoMaterial

class Command(BaseCommand):
    help = 'Importa materiais de um arquivo Excel para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', type=str, help='Caminho completo para o arquivo Excel de Materiais.')

    def handle(self, *args, **options):
        arquivo = options['arquivo']
        try:
            df = pd.read_excel(arquivo)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao ler o arquivo: {e}'))
            return

        # Obter o usuário "Diogo Batista"
        User = get_user_model()
        try:
            user = User.objects.get(username="Diogo Batista")
        except User.DoesNotExist:
            try:
                user = User.objects.get(first_name="Diogo", last_name="Batista")
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR("Usuário 'Diogo Batista' não encontrado."))
                return

        for index, row in df.iterrows():
            nome_material = row.get('Descricao')
            if not nome_material:
                continue  # ignora linhas sem valor para a descrição

            # Obtém o objeto Unidade baseado na coluna "Unidade"
            unidade_nome = row.get('Unidade')
            unidade_obj = None
            if unidade_nome:
                try:
                    unidade_obj = Unidade.objects.get(unidade=unidade_nome)
                except Unidade.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Unidade '{unidade_nome}' não encontrada."))

            # Obtém o objeto GrupoMaterial baseado na coluna "Grupo_materiais"
            grupo_nome = row.get('Grupo_materiais')
            grupo_obj = None
            if grupo_nome:
                try:
                    grupo_obj = GrupoMaterial.objects.get(nome=grupo_nome)
                except GrupoMaterial.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Grupo '{grupo_nome}' não encontrado."))

            material_obj, created = Material.objects.get_or_create(
                nome=nome_material,
                defaults={
                    'saldo_inicial': 0,
                    'saldo_atual': 0,
                    'unidade': unidade_obj,
                    'grupo': grupo_obj,
                    'ativo': True,
                    'created_by': user,
                    'updated_by': user,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Material '{material_obj}' criado com sucesso."))
            else:
                self.stdout.write(f"Material '{material_obj}' já existe.")


#/home/dbsistem/sgmtestes/manage.py import_materiais /home/dbsistem/sgmtestes/Arquivos/Base_materiais.xlsx