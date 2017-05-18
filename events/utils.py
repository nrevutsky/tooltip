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
            result = create_daily_report(data)
    else:
        day_diff = 6 if period == PERIOD_WEEK else 29
        day = dt.date.today() - dt.timedelta(days=day_diff)
        data = PeriodEvent.periodicals_events.get_project_data_by_period(project_id=project_id, day=day)
        if data:
            result = create_period_report(data, day)
    return sort_data(result)


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
    if data:
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
            result = create_daily_report(data)
    else:
        day_diff = 6 if period == PERIOD_WEEK else 29
        day = dt.date.today() - dt.timedelta(days=day_diff)
        data = PeriodEvent.periodicals_events.get_message_data_by_period(message_id=msg_id, day=day)
        if data:
            result = create_period_report(data, day)
    return sort_data(result)


def create_dict_by_hour():
    result = {}
    hour = dt.timedelta(hours=1)
    now = dt.datetime.now().replace(microsecond=0, second=0, minute=0) - dt.timedelta(hours=24)
    end_time = dt.datetime.now().replace(microsecond=0, second=0, minute=0)
    while now < end_time:
        result[now] = 0
        now += hour
    return result


def create_daily_report(data):
    result = {}
    for msg in data:
        for event in EVENTS:
            if not result.get(event):
                result[event] = {}
            date_key = dt.datetime.combine(msg.day, dt.time(hour=msg.hour))
            if not result[event].get(date_key):
                result[event][date_key] = 0
            result[event][dt.datetime.combine(msg.day, dt.time(hour=msg.hour))] += get_parameter_value(msg,
                                                                                                       event)
    return fill_empty_hours(result)


def create_period_report(data, day):
    result = {}
    for day_obj in data:
        for event in EVENTS:
            if not result.get(event):
                result[event] = {}
                for single_date in date_range(day, dt.date.today()):
                    result[event][single_date.strftime("%Y-%m-%d")] = 0
                result[event][dt.date.today().strftime("%Y-%m-%d")] = 0
            result[event][day_obj.day.strftime("%Y-%m-%d")] += get_parameter_value(day_obj, event)
    return result


def sort_data(result):
    if result:
        for event in EVENTS:
            if result[event]:
                result[event] = collections.OrderedDict(sorted(result[event].items())).values()
    return result


def fill_empty_hours(result):
    for event in EVENTS:
        for hour_step in range(0, 24):
            if not result[event].get(
                            dt.datetime.now().replace(
                                minute=0, second=0, microsecond=0) - dt.timedelta(hours=hour_step)):
                result[event][dt.datetime.now() - dt.timedelta(hours=hour_step)] = 0
    return result
