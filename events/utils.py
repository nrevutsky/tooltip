from .models import DayEvent, PeriodEvent, GeneralEvent
import datetime as dt
import collections


PERIOD_DAY = 'day'
PERIOD_WEEK = 'week'
PERIOD_MONTH = 'month'
EVENTS = ['visit', 'trigger', 'click', 'close', 'goal']


def get_project_analytics_by_period(project_id, period):
    result = {}
    if period == PERIOD_DAY:
        data = DayEvent.daily_events.get_project_data_by_whole_day(project_id)
        if data:
            for msg in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = []
                        for i in range(0, 24):
                            result[event].insert(i, 0)
                    result[event][msg.hour] += get_parameter_value(msg, event)
            for event in EVENTS:
                if result.get(event):
                    result[event] = reversed(result[event])
    elif period == PERIOD_WEEK:
        day = dt.date.today() - dt.timedelta(days=6)
        data = PeriodEvent.periodicals_events.get_project_data_by_period(project_id=project_id, day=day)
        if data:
            for day_obj in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = {}
                        for single_date in date_range(day, dt.date.today()):
                            result[event][single_date.strftime("%Y-%m-%d")] = 0
                        result[event][dt.date.today().strftime("%Y-%m-%d")] = 0
                    result[event][day_obj.day.strftime("%Y-%m-%d")] += get_parameter_value(day_obj, event)
            for event in EVENTS:
                result[event] = collections.OrderedDict(sorted(result[event].items())).values()
    if period == PERIOD_MONTH:
        day = dt.date.today() - dt.timedelta(days=29)
        data = PeriodEvent.periodicals_events.get_project_data_by_period(project_id=project_id, day=day)
        if data:
            for day_obj in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = {}
                        for single_date in date_range(day, dt.date.today()):
                            result[event][single_date.strftime("%Y-%m-%d")] = 0
                        result[event][dt.date.today().strftime("%Y-%m-%d")] = 0
                    result[event][day_obj.day.strftime("%Y-%m-%d")] += get_parameter_value(day_obj, event)
            for event in EVENTS:
                result[event] = collections.OrderedDict(sorted(result[event].items())).values()
    return result


def get_parameter_value(data_object, event):
    if event == 'visit':
        return data_object.visit
    elif event == 'goal':
        return data_object.goal
    elif event == 'click':
        return data_object.click
    elif event == 'close':
        return data_object.close
    elif event == 'trigger':
        return data_object.trigger


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


def get_general_data(project_id):
    data = GeneralEvent.objects.filter(project_id=project_id)
    result = {}
    for msg in data:
        for event in EVENTS:
            if not result.get(event):
                result[event] = 0
            result[event] += get_parameter_value(msg, event)
    return result


def get_message_analytics_by_period(msg_id, period):
    result = {}
    if period == PERIOD_DAY:
        data = DayEvent.daily_events.get_message_data_by_whole_day(message_id=msg_id)
        if data:
            for msg in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = []
                        for i in range(0, 24):
                            result[event].insert(i, 0)
                    result[event][msg.hour] = get_parameter_value(msg, event)
            for event in EVENTS:
                if result.get(event):
                    result[event] = reversed(result[event])
    elif period == PERIOD_WEEK:
        day = dt.date.today() - dt.timedelta(days=6)
        data = PeriodEvent.periodicals_events.get_message_data_by_period(message_id=msg_id, day=day)
        if data:
            for day_obj in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = {}
                        for single_date in date_range(day, dt.date.today()):
                            result[event][single_date.strftime("%Y-%m-%d")] = 0
                        result[event][dt.date.today().strftime("%Y-%m-%d")] = 0
                    result[event][day_obj.day.strftime("%Y-%m-%d")] = get_parameter_value(day_obj, event)
            for event in EVENTS:
                result[event] = collections.OrderedDict(sorted(result[event].items())).values()
    elif period == PERIOD_MONTH:
        day = dt.date.today() - dt.timedelta(days=29)
        data = PeriodEvent.periodicals_events.get_message_data_by_period(message_id=msg_id, day=day)
        if data:
            for day_obj in data:
                for event in EVENTS:
                    if not result.get(event):
                        result[event] = {}
                        for single_date in date_range(day, dt.date.today()):
                            result[event][single_date.strftime("%Y-%m-%d")] = 0
                        result[event][dt.date.today().strftime("%Y-%m-%d")] = 0
                    result[event][day_obj.day.strftime("%Y-%m-%d")] = get_parameter_value(day_obj, event)
            for event in EVENTS:
                result[event] = collections.OrderedDict(sorted(result[event].items())).values()
    return result


def create_dict_by_hour():
    result = {}
    hour = dt.timedelta(hours=1)
    now = dt.datetime.now().replace(microsecond=0, second=0, minute=0) - dt.timedelta(hours=24)
    end_time = dt.datetime.now().replace(microsecond=0, second=0, minute=0)
    while now < end_time:
        result[now] = 0
        now += hour
    return result
