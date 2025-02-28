# DIT Activity Stream

## Installation

Read the [Django Hawk installation](https://github.com/uktrade/django-hawk/#installation) documentation.

Add the package to your `urls.py` file.

```python
from django.urls import include, path

urlpatterns = [
    ...
    path("dit-activity-stream/", include("dit_activity_stream.urls")),
    ...
]
```

## How to implement?

Write your custom client, here is an example client for returning all users:

```python
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpRequest

from dit_activity_stream.client import ActivityStreamClient

User = get_user_model()


class ActivityStreamUserClient(ActivityStreamClient):
    object_uuid_field: str = "user_id"
    object_last_modified_field: str = "last_modified"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return User.objects.all()

    def render_object(self, object: User) -> Dict:
        return {
            "id": object.id,
            "username": object.username,
            "first_name": object.first_name,
            "last_name": object.last_name,
        }
```

Where the following attributes:
- `object_uuid_field` is a field on the Object that is a Unique Identifier for the object.
  - This will be output in the URL GET parameter so it should be a UUID.
- `object_last_modified_field` us a field on the Object that holds a datetime value of when the object was last modified.
  - This will be output in the URL GET parameter.

Set `DIT_ACTIVITY_STREAM_CLIENT_CLASS` in your django settings file:

```python
DIT_ACTIVITY_STREAM_CLIENT_CLASS = "package.client.ActivityStreamUserClient"
```

## Pushing to PyPI

- [PyPI Package](https://pypi.org/project/dit-activity-stream/)
- [Test PyPI Package](https://test.pypi.org/project/dit-activity-stream/)

Running `make build` will build the package into the `dist/` directory.
Running `make push-pypi-test` will push the built package to Test PyPI.
Running `make push-pypi` will push the built package to PyPI.

### Setting up poetry for pushing to PyPI

First you will need to add the test pypy repository to your poetry config:

```
poetry config repositories.test-pypi https://test.pypi.org/legacy/
```

Then go to https://test.pypi.org/manage/account/token/ and generate a token.

Then add it to your poetry config:

```
poetry config pypi-token.test-pypi XXXXXXXX
```

Then you also need to go to https://pypi.org/manage/account/token/ to generate a token for the real PyPI.

Then add it to your poetry config:

```
poetry config pypi-token.pypi XXXXXXXX
```

Now the make commands should work as expected.
