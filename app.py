# app.py

import os
import responder
from starlette.exceptions import HTTPException
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned, OperationalError
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
async def get_users(req, resp):
    """
    Return all Users
    :param _:
    :param resp:
    :return: json
    """

    users = []

    if req.method == 'post':
        resp.text = "Can not create new users from this endpoint."

    # default method
    elif req.method == 'get':

        resp.status_code = api.status_codes.HTTP_200

        # fetch the users from the database
        try:
            data = await User.all().limit(10)

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

    else:

        # respond method not allowed send a 405
        resp.status_code = api.status_codes.HTTP_405
        resp.media = {
            "Error": "Method: " + f"{req.method} is not allowed.  Operation aborted.",
            "Status": resp.status_code
        }


@api.route("/api/v1.0/user/{username}")
async def get_user(_, resp, username: str):

    # fetch the new user
    try:
        user = await User.filter(name=username).first()

        # return the response in plain text
        resp.status_code = api.status_codes.HTTP_200
        resp.text = f"Hello, {user.name}"

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=None
        )


@api.route("/api/v1.0/groups")
async def get_groups(req, resp):
    """
    Get a list of Groups
    :param _:
    :param resp:
    :return: json
    """

    # create a new group on post
    if req.method == 'post':

        # get the params
        data = req.params

        if data:
            _group = req.params.get('group')

            try:
                group = await Group.create(group_name=_group)

                resp.status_code = api.status_codes.HTTP_201
                resp.media = {
                    "Success": f"{group} was successfully added..."
                }

            except OperationalError as db_err:
                raise HTTPException(
                    status_code=500,
                    detail=str(db_err)
                )
        else:
            # return response
            resp.text = "No params found in the request.  Operation aborted."

    # get method
    elif req.method == 'get':

        # create an group dict
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

    else:

        # respond method not allowed and 405
        resp.status_code = api.status_codes.HTTP_405
        resp.media = {
            "Error": "Method: " + f"{req.method} is not allowed.  Operation aborted.",
            "Status": resp.status_code
        }


@api.route("/api/v1.0/persons")
async def get_persons(req, resp):
    """
    Get a list of persons
    :param _:
    :param resp:
    :return: json
    """

    # add a new person
    if req.method == 'post':

        # get the params
        data = req.params

        if data:
            f_name = req.params.get('first_name')
            l_name = req.params.get('last_name')
            age = req.params.get('age')
            phone = req.params.get('phone')

            # insert the record
            try:
                await Person.create(first_name=f_name, last_name=l_name, age=age, phone=phone)

                # return the response
                resp.status_code = api.status_codes.HTTP_201
                resp.media = {
                    "First Name": f_name,
                    "Last Name": l_name,
                    "Age": age,
                    "Phone": phone
                }

            except OperationalError as db_err:
                raise HTTPException(
                    status_code=500,
                    detail=str(db_err)
                )

        else:
            # return error response
            resp.text = "No params found in the request.  Operation aborted."

    # default method
    elif req.method == 'get':

        # create an empty list
        persons = []

        # fetch the new Person object
        try:
            data = await Person.all().limit(25)

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
            resp.status_code = api.status_codes.HTTP_200
            resp.media = persons

        except DoesNotExist:
            raise HTTPException(
                status_code=404,
                detail=None
            )

    else:

        # respond method not allowed and 405
        resp.status_code = api.status_codes.HTTP_405
        resp.media = {
            "Error": "Method: " + f"{req.method} is not allowed.  Operation aborted.",
            "Status": resp.status_code
        }


if __name__ == "__main__":
    api.run(
        address="0.0.0.0",
        port=7001,
        debug=debug
    )
