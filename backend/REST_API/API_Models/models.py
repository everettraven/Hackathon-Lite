import json
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
import requests

db = SQLAlchemy()

#Create the user class and use it to create a user database table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    access_token = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    phone_remind = db.Column(db.Boolean())


    def __init__(self, username, password, access_token, phone="", phone_remind=False):
        self.username = username
        self.password = password
        self.phone = phone
        self.access_token = access_token
        self.phone_remind = phone_remind


class Course():
    def __init__(self, course_id, course_name, course_code):
        self.course_id = course_id
        self.course_name = course_name
        self.course_code = course_code
        self.assignments = []

    def add_assignment(self, Assignment):
        self.assignments.append(Assignment)


    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_code": self.course_code,
            "assignments": [e.serialize() for e in self.assignments]
        }


class Assignment():
    def __init__(self, id, name, description, due_at):
        self.id = id
        self.name = name
        self.description = description
        self.due_at = due_at
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_at": self.due_at
        }