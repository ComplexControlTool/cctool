from django.apps import AppConfig


class GraphsAppConfig(AppConfig):

    name = "cctool.graphs"
    verbose_name = "Graphs"

    def ready(self):
        try:
            import graphs.signals  # noqa F401
        except ImportError:
            pass
