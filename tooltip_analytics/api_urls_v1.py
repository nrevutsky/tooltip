from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('events.api_urls', namespace='api-urls'))
]
