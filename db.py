# TODO:
# [x] Create a database with tables
# [x] Connect the database to our python code
#     [x] Close connections when done
# [x] Test writing rows to the database
# [x] Test reading rows to the database

import sqlite3
from flask import g

DATABASE = 'flask_db_workshop.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect(DATABASE)
        db = g._database
    return db







# class House():

#     floors = 5
#     rooms = 10

# variable_i_want_to_get = "floors"
# my_house = House()
# getattr(my_house, variable_i_want_to_get)
# new_attribute = "doors"
# setattr(my_house, new_attribute, 5)

# if variable_i_want_to_get == "floors":
#     return iphone.floors
# if variable_i_want_to_get == "rooms":
#     return iphone.rooms
