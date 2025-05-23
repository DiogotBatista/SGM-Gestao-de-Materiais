# 📦 SGM - Sistema de Gestão de Materiais

O **SGM** é uma aplicação web desenvolvida em Django para gerenciar de forma eficiente as movimentações de entrada e saída de materiais em contratos e obras. O sistema foi projetado para uso interno em empresas da construção civil, com foco em rastreabilidade, controle e organização de estoque descentralizado.

## 🚀 Funcionalidades Principais

- **Controle de movimentações** de entrada e saída de materiais
- **Associação de materiais a contratos e obras**
- **Relatórios customizáveis** (PDF e Excel) usando `pandas`, `openpyxl` e `reportlab`
- **Filtros avançados** por tipo de movimentação, datas, contratos e obras
- **Cadastro de itens por formulário dinâmico**
- **Acesso por nível de cargo**, com permissões personalizadas
- **Interface responsiva e amigável** com Bootstrap 5
- **Exibição condicional de colunas** nos relatórios
- **Dashboard inicial** com resumo geral das movimentações

## 🧩 Tecnologias Utilizadas

- Python 3.11
- Django 4.2
- Bootstrap 5
- Pandas
- OpenPyXL
- ReportLab
- SortableJS (reordenação de itens)
- HTMX (interatividade sem recarregar a página)

## 🗂 Estrutura do Projeto

```bash
sgm/
├── contratos/         # App para contratos e obras
├── movimentacoes/     # App principal para entrada e saída de materiais
├── reunioes/          # App para atas de reunião (quando aplicável)
├── usuarios/          # Gestão de usuários, perfis e permissões
├── static/            # Arquivos estáticos (JS, CSS, ícones)
├── templates/         # Templates HTML estruturados por app
├── media/             # Uploads e arquivos gerados
├── manage.py
└── requirements.txt
