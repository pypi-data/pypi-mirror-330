from django.test import TestCase, override_settings

from dit_activity_stream.client import get_activity_stream_client


class TestGetActivityStreamClient(TestCase):
    @override_settings(DIT_ACTIVITY_STREAM_CLIENT_CLASS=None)
    def test_setting_not_set(self):
        with self.assertRaises(ValueError):
            get_activity_stream_client()

    @override_settings(
        DIT_ACTIVITY_STREAM_CLIENT_CLASS=(
            "dit_activity_stream.test_app.client.TestBadActivityStreamClient"
        )
    )
    def test_setting_incorrect(self):
        with self.assertRaises(ValueError):
            get_activity_stream_client()
