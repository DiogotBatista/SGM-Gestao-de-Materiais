from django.apps import AppConfig

class MovimentacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movimentacoes'

    def ready(self):
        import movimentacoes.signals
