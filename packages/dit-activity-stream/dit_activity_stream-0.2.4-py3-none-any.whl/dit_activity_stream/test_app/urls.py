from django.urls import include, path

urlpatterns = [
    path("dit-activity-stream/", include("dit_activity_stream.urls")),
]
