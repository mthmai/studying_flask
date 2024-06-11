#!/usr/bin/python3

# Base imports
import os

# Third imports
from peewee import AutoField, CharField, ForeignKeyField, FloatField, IntegerField, Model, SqliteDatabase, TextField

db = SqliteDatabase(f'{os.path.dirname(os.path.abspath(__file__))}/cbb.db', pragmas={'journal_mode': 'wal'})

class BaseModel(Model):

    class Meta:
        database = db


class Teams(BaseModel):
    team = TextField(primary_key=True, unique= True)
    conference = CharField(max_length=8)

class Temporada(BaseModel):
    team = ForeignKeyField(Teams, field=Teams.team, on_delete= 'CASCADE')
    conference = ForeignKeyField(Teams, field=Teams.conference, on_delete= 'CASCADE')
    games_played = IntegerField()
    games_win = IntegerField()
    year = IntegerField()

class Staats(BaseModel):
    staats_id = AutoField()
    team = ForeignKeyField(Temporada, field=Temporada.team, on_delete= 'CASCADE')
    conference = ForeignKeyField(Temporada, field=Temporada.conference, on_delete= 'CASCADE')
    games_played = ForeignKeyField(Temporada, field=Temporada.games_played, on_delete='CASCADE')
    games_win = ForeignKeyField(Temporada, field=Temporada.games_win, on_delete='CASCADE')
    year = ForeignKeyField(Temporada, field=Temporada.year, on_delete='CASCADE')
    adjoe = FloatField(null=True)
    adjde = FloatField(null=True)
    barthag = FloatField(null=True)
    efg_o = FloatField(null=True)
    efg_d = FloatField(null=True)
    tor = FloatField(null=True)
    tord = FloatField(null=True)
    orb = FloatField(null=True)
    drb = FloatField(null=True)
    ftr = FloatField(null=True)
    ftrd = FloatField(null=True)
    two_point_o = FloatField(null=True)
    two_poind_d = FloatField(null=True)
    three_point_o = FloatField(null=True)
    three_point_d = FloatField(null=True)
    adj_t = FloatField(null=True)
    wab = FloatField(null=True)
    postseason = TextField(null=True)
    seed = FloatField(null=True)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Teams, Temporada, Staats])