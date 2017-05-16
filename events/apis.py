from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.cache import cache
from .tasks import save_events_count_to_db
from rest_framework import status
from .utils import get_project_analytics_by_period, get_general_data, get_message_analytics_by_period
import datetime as dt


@api_view(['POST'])
def receive_events_data(request):
    if request.data:
        if request.data.get('secret') == settings.SECRET_KEY_API:
            event_date = dt.datetime.fromtimestamp(int(request.data.get('time_stamp'))).replace(minute=0, second=0)
            events_general = cache.get('events_general')
            if not events_general:
                events_general = {}
            events_by_hour = events_general.get(event_date)
            if not events_by_hour:
                events_by_hour = {request.data.get('event_type'): {request.data.get('project_id'): {request.data.get('message_id'): 0}}}
            if not events_by_hour.get(request.data.get('event_type')):
                event_by_project_dict = {request.data.get('project_id'): {request.data.get('message_id'): 0}}
                events_by_hour[request.data.get('event_type')] = event_by_project_dict
            event = events_by_hour[request.data.get('event_type')]
            event_project = event.get(request.data.get('project_id'))
            if event_project:
                event_project_msg = event_project.get(request.data.get('message_id'))
                if event_project_msg:
                    event_project[request.data.get('message_id')] = event_project_msg + 1
                else:
                    event_project[request.data.get('message_id')] = 1
                event[request.data.get('project_id')] = event_project
            else:
                event[request.data.get('project_id')] = {request.data.get('message_id'): 1}
            events_by_hour[request.data.get('event_type')] = event
            events_general[event_date] = events_by_hour
            cache.set('events_general', events_general)
            # save_events_count_to_db()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_periodical_analytics_by_project(request, project_id):
    data = get_project_analytics_by_period(project_id, request.query_params.get('filter'))
    return Response(data=data)


@api_view(['GET'])
def get_general_analytics(request, project_id):
    data = get_general_data(project_id)
    return Response(data=data)


@api_view(['GET'])
def get_periodical_analytics_by_message(request, message_id):
    data = get_message_analytics_by_period(message_id, request.query_params.get('filter'))
    return Response(data=data)
