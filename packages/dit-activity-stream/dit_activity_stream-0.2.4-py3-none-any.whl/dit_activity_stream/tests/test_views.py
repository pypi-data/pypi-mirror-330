from django.test import TestCase, override_settings
from freezegun import freeze_time

from dit_activity_stream.test_app.factories import UserFactory
from dit_activity_stream.test_app.utils import get_hawk_kwargs

DIT_ACTIVITY_STREAM_PATH = "/dit-activity-stream/"


class TestAuthenticate(TestCase):
    def test_via_public_internet_then_403(self):
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH, forwarded=True),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {})

    def test_no_header_provided(self):
        response = self.client.get(DIT_ACTIVITY_STREAM_PATH)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {})

    def test_incorrect_secret(self):
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH, hawk_secret="incorrect-secret"),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {})


class TestDitActivityStreamView(TestCase):
    def test_no_users(self):
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH),
        )

        self.assertEqual(response.status_code, 200)

        users = response.json()["orderedItems"]

        self.assertEqual(len(users), 0)
        self.assertEqual(users, [])

    def test_multiple_users(self):
        # create user data
        with freeze_time("2021-01-02 03:04:05", tick=True):
            UserFactory(username="Victor")
            UserFactory(username="Jack")
            UserFactory(username="Winston")

        # Making a request, checking for 200 status code.
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH),
        )

        self.assertEqual(response.status_code, 200)

        # Checking returned values
        users = response.json()["orderedItems"]

        self.assertEqual(len(users), 3)
        self.assertEqual(users[0]["Name"], "Victor")
        self.assertEqual(users[1]["Name"], "Jack")
        self.assertEqual(users[2]["Name"], "Winston")

    @override_settings(
        DIT_ACTIVITY_STREAM_CLIENT_CLASS="dit_activity_stream.test_app.client.CustomRenderClient"
    )
    def test_override_render_object(self):
        # create user data
        with freeze_time("2021-01-02 03:04:05", tick=True):
            UserFactory(username="Victor")

        # Making a request, checking for 200 status code.
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH),
        )

        self.assertEqual(response.status_code, 200)

        # Checking returned values
        users = response.json()["orderedItems"]

        self.assertEqual(users[0]["username"], "Victor")

    @override_settings(
        DIT_ACTIVITY_STREAM_CLIENT_CLASS="dit_activity_stream.test_app.client.CustomQuerysetClient"
    )
    def test_override_get_queryset(self):
        # create user data
        with freeze_time("2021-01-02 03:04:05", tick=True):
            UserFactory(username="Victor")
            UserFactory(username="Jack")
            UserFactory(username="Winston")

        # Making a request, checking for 200 status code.
        response = self.client.get(
            DIT_ACTIVITY_STREAM_PATH,
            **get_hawk_kwargs(DIT_ACTIVITY_STREAM_PATH),
        )

        self.assertEqual(response.status_code, 200)

        # Checking returned values
        users = response.json()["orderedItems"]

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["Name"], "Jack")

    # TODO: Write tests for the pagination/cursor logic.
