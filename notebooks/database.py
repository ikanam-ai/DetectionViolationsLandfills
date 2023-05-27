import os

import deta
from deta import Deta 

DETA_KEY = 'c0dahqob3d5_3pz1eEuAyAQwE4P1waUJwr4cr2anHzp8'

deta = Deta(DETA_KEY)

db = deta.Base('users')

def insert_user(username, name, password):
    return db.put({"key": username, "name": name, "password": password})

def fetch_all_users():
    res = db.fetch()
    return res.items

def get_user(username):
    return db.get(username)

def update_user(username, updates):
    return db.update(updates, username)

def delete_user(username):
    return  db.delete(username)
