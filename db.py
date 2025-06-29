from typing import Text
from peewee import ForeignKeyField, IntegerField, Model, SqliteDatabase, TextField

db = SqliteDatabase("game.db")

class BaseModel(Model):
    class Meta:
        database = db

class Info(BaseModel):
    user_id = IntegerField(primary_key=True)

class Nation(BaseModel):
    user_id = IntegerField(primary_key=True)
    nation_name = TextField()
    happiness = IntegerField(default=0) # won't really be accessed, yet. just let the default value be 0
    war_status = TextField(default="Peace")
    pop = IntegerField(default=20_000) # magic value
    balance = IntegerField(default=100_000) # magic value

    # bonuses
    admin_production_bonus = IntegerField(default=1)
    pop_multiplier = IntegerField(default=1)

class Mil(BaseModel):
    user_id = IntegerField(primary_key=True)
    troops = IntegerField(default=5_000)
    tanks = IntegerField(default=0)
    planes = IntegerField(default=0)
    artillery = IntegerField(default=0)
    anti_air = IntegerField(default=0)
    recruiting_time_left = IntegerField(default=0) # this is to ensure that if the bot stops running, the player doesn't have to wait or recruit again.
    in_recruitment = IntegerField(default=0)

    # bonuses
    mil_ground_doctrine = TextField(default="Mobile Warfare")
    mil_air_doctrine = TextField(default="Strategic Destruction")
    admin_mil_tactic_bonus = IntegerField(default=1)

class Infra(BaseModel):
    user_id = IntegerField(primary_key=True)

    # raw materials
    iron_mine = IntegerField(default=2)
    coal_mine = IntegerField(default=2)
    oil_well = IntegerField(default=1)
    lumber_camp = IntegerField(default=2)
    grain_farm = IntegerField(default=2)
    water_plant = IntegerField(default=1)

    # manufactured materials
    steel_mill = IntegerField(default=0)
    sawmill = IntegerField(default=0)
    flour_mill = IntegerField(default=0)
    food_processing = IntegerField(default=0)
    oil_refinery = IntegerField(default=0)
    cement_plant = IntegerField(default=0)
    electronics_factory = IntegerField(default=0)

class Resources(BaseModel):
    user_id = IntegerField(primary_key=True)

    # Raw resources
    iron_ore = IntegerField(default=200)
    coal = IntegerField(default=200)
    oil = IntegerField(default=100)
    wood = IntegerField(default=200)
    grain = IntegerField(default=200)
    water = IntegerField(default=300)

    # Manufactured goods
    steel = IntegerField(default=0)
    planks = IntegerField(default=0)
    flour = IntegerField(default=0)
    processed_food = IntegerField(default=0)
    petrol = IntegerField(default=0)
    concrete = IntegerField(default=0)
    electronics = IntegerField(default=0)


def init_db():
    db.connect()
    db.create_tables([Info, Nation, Mil, Infra, Resources])
    print("[+] DB Initialized.")
