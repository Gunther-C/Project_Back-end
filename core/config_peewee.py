from peewee import SqliteDatabase

"""
import os
DATABASE = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE, 'db.sqlite3')

DATABASE = {
    "sql": "db.sqlite3",
    "engine": "SqliteDatabase"
}
db = SqliteDatabase(DATABASE['sql'])
"""

db = SqliteDatabase('db.sqlite3')
