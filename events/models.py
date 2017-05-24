# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from .managers import DayEventQuerySet, PeriodEventQuerySet


class DayEvent(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, null=True)
    hour = models.IntegerField()
    project_id = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100)
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
    project_id = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100)
    visit = models.IntegerField(default=0)
    trigger = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)

    objects = models.Manager()
    periodicals_events = PeriodEventQuerySet.as_manager()


class GeneralEvent(models.Model):
    project_id = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100)
    visit = models.IntegerField(default=0)
    trigger = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)


class RawRequest(models.Model):
    project_id = models.CharField(max_length=100, null=True, blank=True)
    message_id = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    event_type = models.CharField(max_length=20, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
