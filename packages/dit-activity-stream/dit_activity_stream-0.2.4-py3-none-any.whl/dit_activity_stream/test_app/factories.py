from factory import Sequence
from factory.django import DjangoModelFactory

from dit_activity_stream.test_app.models import CustomUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = Sequence(lambda n: f"user{n}@example.com")
    username = Sequence(lambda n: f"user{n}")
