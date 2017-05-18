from django.db import models
import datetime as dt


class DayEventQuerySet(models.QuerySet):
    def get_project_data_by_whole_day(self, project_id):
        last_day = dt.date.today() - dt.timedelta(days=1)
        data = self.filter(models.Q(project_id=project_id),
                           models.Q(day=dt.date.today(), hour__lte=dt.datetime.now().hour) |
                           models.Q(day=last_day, hour__gt=dt.datetime.now().hour)).order_by('day', 'hour')
        return data

    def get_message_data_by_whole_day(self, message_id):
        last_day = dt.date.today() - dt.timedelta(days=1)
        data = self.filter(models.Q(message_id=message_id),
                           models.Q(day=dt.date.today(), hour__lte=dt.datetime.now().hour) |
                           models.Q(day=last_day, hour__gt=dt.datetime.now().hour)).order_by('day', 'hour')
        return data


class PeriodEventQuerySet(models.QuerySet):
    def get_project_data_by_period(self, project_id, day):
        data = self.filter((models.Q(project_id=project_id, day__gte=day, day__lte=dt.date.today())))
        return data

    def get_message_data_by_period(self, message_id, day):
        data = self.filter((models.Q(message_id=message_id, day__gte=day, day__lte=dt.date.today())))
        return data
