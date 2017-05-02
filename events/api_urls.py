from django.conf.urls import url
from .apis import receive_events_data, get_periodical_analytics_by_project, get_general_analytics,\
    get_periodical_analytics_by_message

urlpatterns = [
    url(r'^collect/$', receive_events_data, name='receive_events_data'),
    url(r'^project-stats/(?P<project_id>[^/]+)/$', get_periodical_analytics_by_project, name='get_project_analytics'),
    url(r'^project-general-stats/(?P<project_id>[^/]+)/$', get_general_analytics, name='get_general_analytics'),
    url(r'^message-stats/(?P<message_id>[^/]+)/$', get_periodical_analytics_by_message, name='get_message_analytics'),
]
