import os
import pandas as pd
import django

# Configurar ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgm.settings")  # 🔁 Substitua 'seu_projeto' pelo nome do seu projeto
django.setup()

from usuarios.models import ViewDisponivel

# Caminho do arquivo gerado
ARQUIVO_EXCEL = os.path.join(os.path.dirname(__file__), 'Arquivos', 'Nomes_views.xlsx')

if not os.path.exists(ARQUIVO_EXCEL):
    print(f"Arquivo {ARQUIVO_EXCEL} não encontrado.")
    exit()

# Ler o Excel
df = pd.read_excel(ARQUIVO_EXCEL)

# Verificar e adicionar as views
novos = 0
for nome_view in df['view_name'].dropna().unique():
    if not ViewDisponivel.objects.filter(nome=nome_view).exists():
        ViewDisponivel.objects.create(nome=nome_view)
        novos += 1

print(f"{novos} novas view(s) adicionadas com sucesso.")
