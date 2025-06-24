from django.urls import re_path
from system_files.consumer import ChartDataConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chart-data/$', ChartDataConsumer.as_asgi()),
]