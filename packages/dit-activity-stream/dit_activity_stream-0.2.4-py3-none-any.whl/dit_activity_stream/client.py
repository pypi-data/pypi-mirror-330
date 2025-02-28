from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from django.conf import settings
from django.db.models import Q, QuerySet
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.utils.module_loading import import_string


# We want this function to return a View
def get_activity_stream_client():
    """
    Get the view from the DIT_ACTIVITY_STREAM_CLIENT_CLASS setting
    """

    # Use default view if RENDER_VIEW setting doesn't exist.
    if not getattr(settings, "DIT_ACTIVITY_STREAM_CLIENT_CLASS", None):
        raise ValueError("DIT_ACTIVITY_STREAM_CLIENT_CLASS must be set")

    dit_activity_stream_client_class = import_string(
        settings.DIT_ACTIVITY_STREAM_CLIENT_CLASS
    )

    # Check if subclass of ActivityStreamClient
    if not issubclass(dit_activity_stream_client_class, ActivityStreamClient):
        raise ValueError(
            "DIT_ACTIVITY_STREAM_CLIENT_CLASS must inherit from ActivityStreamClient"
        )

    return dit_activity_stream_client_class()


class ActivityStreamClient(ABC):
    object_uuid_field: str
    object_last_modified_field: str
    objects_per_page: int = 50

    @abstractmethod
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Get the queryset for the objects to be rendered.

        Note: Filtering the queryset for pagination is handled elsewhere.
        """

        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def render_object(self, object: Any) -> Dict:
        """
        Render the object out into a dict.
        """

        raise NotImplementedError()  # pragma: no cover

    def get_cursor(self, request: HttpRequest) -> Tuple[datetime, UUID]:
        """
        Get the cursor from the request.

        The cursor is built up as a timestamp and UUID, separated by an underscore.
        """

        after_ts_str, after_object_id_str = request.GET.get(
            "cursor", "0.0_00000000-0000-4000-0000-000000000000"
        ).split("_")
        after_ts = datetime.fromtimestamp(float(after_ts_str))
        after_object_id = UUID(after_object_id_str)
        return after_ts, after_object_id

    def next_url(
        self, request: HttpRequest, after_ts: datetime, after_object_id: UUID
    ) -> str:
        """
        Build the URL for the next page of objects.
        """

        return request.build_absolute_uri(
            reverse("dit_activity_stream")
        ) + "?cursor={}_{}".format(str(after_ts.timestamp()), str(after_object_id))

    def paginate_objects_queryset(
        self, objects_queryset: QuerySet, after_ts: datetime, after_object_id: UUID
    ) -> QuerySet:
        """
        Paginate the objects queryset.

        The exclusion Query does the following:
        - Excludes any objects modified before the timestamp
        - Excludes any objects with a matching timestamp, but a lower or equal UUID
          to the after_object_id
        """

        exclusion_query = Q(
            Q(**{self.object_last_modified_field + "__lt": after_ts})
            | Q(
                **{
                    self.object_last_modified_field: after_ts,
                    self.object_uuid_field + "__lte": after_object_id,
                }
            )
        )
        one_second_ago = datetime.now() - timedelta(seconds=1)

        objects_queryset = objects_queryset.exclude(exclusion_query)
        objects_queryset = objects_queryset.filter(
            **{self.object_last_modified_field + "__lt": one_second_ago}
        )
        objects_queryset = objects_queryset.order_by(
            self.object_last_modified_field, self.object_uuid_field
        )

        return objects_queryset[: self.objects_per_page]

    def render_page(self, request: HttpRequest) -> JsonResponse:
        """
        Render out the page of objects.
        """

        after_ts, after_object_id = self.get_cursor(request=request)

        objects_queryset = self.get_queryset(request=request)
        objects_queryset = self.paginate_objects_queryset(
            objects_queryset=objects_queryset,
            after_ts=after_ts,
            after_object_id=after_object_id,
        )
        objects: List[Any] = list(objects_queryset)

        data: Dict[str, Any] = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                {"dit": "https://www.trade.gov.uk/ns/activitystreams/v1"},
            ],
            "type": "Collection",
            "orderedItems": [],
        }

        last_ts: Optional[datetime] = None
        last_object_id: Optional[UUID] = None

        for object in objects:
            data["orderedItems"].append(self.render_object(object=object))
            last_ts = getattr(object, self.object_last_modified_field)
            last_object_id = getattr(object, self.object_uuid_field)

        if data["orderedItems"]:
            assert last_ts
            assert last_object_id

            data["next"] = self.next_url(
                request=request,
                after_ts=last_ts,
                after_object_id=last_object_id,
            )

        return JsonResponse(data)
