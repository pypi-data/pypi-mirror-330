from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = "dit_activity_stream.test_app"
    label = "dit_activity_stream_test_app"
    verbose_name = "DIT Activity Stream Test App"
    default_auto_field = "django.db.models.AutoField"
