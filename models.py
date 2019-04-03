# coding: utf-8

from tortoise.models import Model
from tortoise import fields


class User(Model):
    """
    User class instance
    """
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        table = 'user'

    def __str__(self):
        return f'{self.name}'


class Group(Model):
    """
    Group class instance
    """

    id = fields.IntField(pk=True)
    group_name = fields.TextField()
    active = fields.BooleanField(default=True)

    class Meta:
        table = 'group'

    def __str__(self):
        if self.group_name:
            return f'{self.group_name}'
        return self.id


class Person(Model):
    """
    Person class instance
    """
    id = fields.IntField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()
    age = fields.IntField()
    phone = fields.TextField()

    class Meta:
        table = 'person'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MeetUp(Model):
    """
    Meetup class instance
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'meetup'

    def __str__(self):
        if self.name:
            return f"{self.name} MeetUp"
        return self.id


class Event(Model):
    """
    Event class instance
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    event_date = fields.DatetimeField()
    event_last_updated = fields.DatetimeField(auto_now=True)
    meetup = fields.ForeignKeyField('models.MeetUp', related_name='events')
    participants = fields.ManyToManyField('models.Group', related_name='events', through='event_group')

    class Meta:
        table = 'event'

    def __str__(self):
        if self.name and self.event_date:
            return f"{self.event_name} {self.event_date}"
        return self.id
