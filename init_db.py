# coding: utf-8

from tortoise import Tortoise, run_async


async def init():
    await Tortoise.init(
        db_url='sqlite://persons.db', modules={'models': ['models']}
    )

    await Tortoise.generate_schemas()

run_async(init())
