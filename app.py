# app.py

import os
import responder
from starlette.exceptions import HTTPException
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned
from models import User, Group, Person

api = responder.API(secret_key=os.urandom(64))
debug = True


@api.on_event("shutdown")
async def close_db_connection():
    await Tortoise.close_connections()


@api.on_event("startup")
async def init_db():
    """
    Initialize the database
    :return:
    """
    await Tortoise.init(
        db_url="sqlite://persons.db", modules={"models": ["models"]}
    )


@api.route("/api/v1.0/users")
async def get_users(_, resp):
    """
    Return all Users
    :param _:
    :param resp:
    :return: json
    """

    users = []

    # fetch the users from the database
    try:
        data = await User.all()

        for rec in data:
            _users = {
                "id": rec.id,
                "name": rec.name
            }

            users.append(_users)

        # return the response
        resp.media = users

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=None
        )


@api.route("/api/v1.0/user/{username}")
async def get_user(_, resp, username: str):

    # fetch the new user
    try:
        user = await User.filter(name=username).first()

        # return the response in plain text
        resp.text = f"Hello, {user.name}"

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=None
        )


@api.route("/api/v1.0/groups")
async def get_groups(_, resp):
    """
    Get a list of Groups
    :param _:
    :param resp:
    :return: json
    """
    # create an empty dict
    groups = []

    # query the database for all groups
    try:
        data = await Group.all()

        # add group_name to dict
        # make the queryset obj json serializable
        for rec in data:
            _group = {
                'id': rec.id,
                'name': rec.group_name
            }

            groups.append(_group)

        # return the response
        resp.media = groups

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=None
        )


@api.route("/api/v1.0/persons")
async def get_persons(_, resp):
    """
    Get a list of persons
    :param _:
    :param resp:
    :return: json
    """

    # create a Person object
    # await Person.create(first_name="Marshall", last_name="Madison", age=35, phone="910-555-1212")

    persons = []

    # fetch the new Person object
    try:
        data = await Person.all()

        # make the queryset json serializable
        for rec in data:
            _persons = {
                'first_name': rec.first_name,
                'last_name': rec.last_name,
                'age': rec.age,
                'phone': rec.phone
            }

            persons.append(_persons)

        # return the response as json
        resp.media = persons

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=None
        )


if __name__ == "__main__":
    api.run(
        address="0.0.0.0",
        port=7001,
        debug=debug
    )
