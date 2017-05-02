# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from .managers import DayEventQuerySet, PeriodEventQuerySet


class DayEvent(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, null=True)
    hour = models.IntegerField()
    project_id = models.IntegerField()
    message_id = models.IntegerField()
    visit = models.IntegerField(default=0)
    trigger = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)

    objects = models.Manager()
    daily_events = DayEventQuerySet.as_manager()


class PeriodEvent(models.Model):
    month = models.IntegerField(default=0)
    day = models.DateField(auto_now=False, auto_now_add=False)
    project_id = models.IntegerField()
    message_id = models.IntegerField()
    visit = models.IntegerField(default=0)
    trigger = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)

    objects = models.Manager()
    periodicals_events = PeriodEventQuerySet.as_manager()


class GeneralEvent(models.Model):
    project_id = models.IntegerField()
    message_id = models.IntegerField()
    visit = models.IntegerField(default=0)
    trigger = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)
