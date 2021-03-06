from django.core.cache import cache
import datetime as dt
from celery.task import periodic_task
from .models import DayEvent, PeriodEvent, GeneralEvent
from django.db import transaction


EVENTS = ['visit', 'trigger', 'click', 'close', 'goal']


@periodic_task(run_every=dt.timedelta(seconds=60))
def save_events_count_to_db():
    general_events = cache.get('events_general')
    empty_hours = []
    if general_events:
        for hour in general_events:
            for event_name in EVENTS:
                event = general_events[hour].get(event_name)
                if event:
                    values_to_delete = {}
                    for project_id, project_body in event.iteritems():
                        for message_id, message_count in project_body.iteritems():
                            with transaction.atomic():
                                save_to_event_db(project_id, message_id, message_count, event_name, hour)
                                values_to_delete[message_id] = project_id
                    for msg_id, pr_id in values_to_delete.iteritems():
                        del event.get(pr_id)[msg_id]
                        if not event.get(pr_id):
                            del event[pr_id]
                        if not event:
                            del general_events[hour][event_name]
            if not general_events[hour]:
                empty_hours.append(hour)
        for empty_hour in empty_hours:
            del general_events[empty_hour]
        cache.set('events_general', general_events)


def save_event(msg, event, count):
    if event == 'visit':
        msg.visit += count if count else 0
    elif event == 'trigger':
        msg.trigger += count if count else 0
    elif event == 'click':
        msg.click += count if count else 0
    elif event == 'goal':
        msg.goal += count if count else 0
    elif event == 'close':
        msg.close += count if count else 0


def save_to_event_db(pr_id, msg_id, msg_count, event_name, date_event):
    # day
    if date_event >= (dt.datetime.now().replace(minute=0, second=0) - dt.timedelta(days=1)):
        hours_diff = dt.datetime.now().replace(minute=0, second=0) - date_event
        msg, created = DayEvent.objects.get_or_create(hour=int(hours_diff.total_seconds()/3600),
                                                      project_id=pr_id,
                                                      message_id=msg_id)
        if not created and msg.day != date_event.date():
            msg.day = date_event.date()
            reset_event(msg)
        if created:
            msg.day = date_event.date()
        save_event(msg, event_name, msg_count)
        msg.save()

    # period
    if date_event >= (dt.datetime.now().replace(minute=0, second=0) - dt.timedelta(days=30)):
        msg_day, created_day = PeriodEvent.objects.get_or_create(day=date_event.date(),
                                                                 project_id=pr_id,
                                                                 message_id=msg_id)
        save_event(msg_day, event_name, msg_count)
        msg_day.month = dt.datetime.now().month
        msg_day.save()

    # general
    msg_general, created_general = GeneralEvent.objects.get_or_create(project_id=pr_id,
                                                                      message_id=msg_id)
    save_event(msg_general, event_name, msg_count)
    msg_general.save()


def reset_event(msg):
    for event in EVENTS:
        if event == 'visit':
            msg.visit = 0
        elif event == 'trigger':
            msg.trigger = 0
        elif event == 'click':
            msg.click = 0
        elif event == 'goal':
            msg.goal = 0
        elif event == 'close':
            msg.close = 0
