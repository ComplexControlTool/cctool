from django.apps import AppConfig


class AnalysersAppConfig(AppConfig):

    name = "cctool.analysers"
    verbose_name = "Analysers"

    def ready(self):
        try:
            import analysers.signals  # noqa F401
        except ImportError:
            pass
