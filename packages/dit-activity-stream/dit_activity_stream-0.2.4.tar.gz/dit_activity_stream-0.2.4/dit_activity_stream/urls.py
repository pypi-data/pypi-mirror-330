from django.urls import path

from dit_activity_stream import views

urlpatterns = [
    path("", views.DitActivityStreamView.as_view(), name="dit_activity_stream"),
]
