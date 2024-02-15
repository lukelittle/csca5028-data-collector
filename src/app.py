#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.sqlite3'

db = SQLAlchemy(app)

class PersonInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

def get_person_info_api():
    response = requests.get("https://fakerapi.it/api/v1/persons?_quantity=1&_gender=male&_birthday_start=2005-01-01")
    person_data = response.json()["data"][0] 
    return {
        "firstname": person_data["firstname"],
        "lastname": person_data["lastname"],
        "email": person_data["email"]
    }

if __name__ == "__main__":    
    with app.app_context():
        db.create_all()

        person_info = get_person_info_api()

        new_entry = PersonInfo(
            firstname=person_info["firstname"],
            lastname=person_info["lastname"],
            email=person_info["email"]
        )
        db.session.add(new_entry) 
        db.session.commit()
        print("Data added to the database")