from django.apps import AppConfig


class CommonAppConfig(AppConfig):

    name = "cctool.common"
    verbose_name = "Common"

    def ready(self):
        try:
            import common.signals  # noqa F401
        except ImportError:
            pass
