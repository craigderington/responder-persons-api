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

    def __str__(self):
        if self.group_name:
            return f'{self.group_name}'
        return self.id

    class Meta:
        table = 'group'


class Person(Model):
    """
    A small class for our database
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
