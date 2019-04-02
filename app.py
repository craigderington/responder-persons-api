# app.py

import responder
from tortoise import Tortoise
from models import User, Group, Person

api = responder.API()


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

    users = dict()

    # fetch the users from the database
    data = await User.all()

    for rec in data:
        users.update({
            "id": rec.id,
            "name": rec.name
        })

    # return the response
    resp.media = users


@api.route("/api/v1.0/user/{username}")
async def get_user(_, resp, username: str):

    # fetch the new user
    user = await User.filter(name=username).first()

    # return the response
    resp.text = f"Hello, {user.name}"


@api.route("/api/v1.0/groups")
async def get_groups(_, resp):
    """
    Get a list of Groups
    :param _:
    :param resp:
    :return: json
    """

    groups = dict()

    # query the database for all groups
    data = await Group.all()

    # make the queryset obj json serializable
    for rec in data:
        groups["id"] = rec.id
        groups["name"] = rec.group_name

    # return the response
    resp.media = groups


@api.route("/api/v1.0/persons")
async def get_persons(_, resp):
    """
    Get a list of persons
    :param _:
    :param resp:
    :return: json
    """

    # create a Person object
    await Person.create(first_name="Marshall", last_name="Madison", age=35, phone="910-555-1212")

    # fetch the new Person object
    data = await Person.all()

    # make the queryset json serializable
    persons = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'age': data.age,
        'phone': data.phone
    }

    # return the response as json
    resp.media = persons


if __name__ == "__main__":
    api.run(
        address="0.0.0.0",
        port=7001
    )
