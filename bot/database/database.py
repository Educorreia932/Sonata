import os

from peewee import AutoField, Model, SqliteDatabase

db_path = os.getenv("SONATA_BOT_DB_PATH", "sonata.db")
db = SqliteDatabase(db_path, pragmas=(("journal_mode", "wal"),))


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db
