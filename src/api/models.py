import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250),unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, **kwargs):
        self.full_name = kwargs['full_name']
        self.email = kwargs['email']
        self.password = kwargs['password']

    @classmethod
    def create(cls, **kwargs):
        new_user = cls(**kwargs)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except Exception as error:
            raise Exception(error.args[0], 400)
        print(new_user.id)
        return new_user

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.gender = kwargs['gender']
        self.hair_color = kwargs['hair_color']
        self.skin_color = kwargs['skin_color']
    
    @classmethod
    def create(cls, **kwargs):
        new_character = cls(**kwargs)
        db.session.add(new_character)
        try:
            db.session.commit()
            return new_character
        except Exception as error:
            raise Exception(error.args[0], 400)
            print(new_character.id)
        return new_character
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.population = kwargs['population']
        self.climate = kwargs['climate']
        self.terrain = kwargs['terrain']

    @classmethod
    def create(cls, **kwargs):
        new_planet = cls(**kwargs)
        db.session.add(new_planet)
        try:
            db.session.commit()
            return new_planet
        except Exception as error:
            raise Exception(error.args[0],400)
            print(new_planet.id)
            return new_planet
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(50))
    manufacturer = db.Column(db.String(250))
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.model = kwargs['model']
        self.manufacturer = kwargs['manufacturer']
        self.crew = kwargs['crew']
        self.passengers = kwargs['passengers']
    
    @classmethod
    def create(cls, **kwargs):
        new_vehicle = cls(**kwargs)
        db.session.add(new_vehicle)
        try:
            db.session.commit()
            return new_vehicle
        except Exception as error:
            raise Exception(error.args[0], 400)
        print(new_vehicle.id)
        return new_vehicle
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "crew": self.crew,
            "passengers": self.passengers
        }

class CharacterFav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    character_id = db.Column(Integer, ForeignKey('character.id'))
    user_id = db.Column(db.Integer,ForeignKey ('user.id') )

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.character_id = kwargs['character_id']
        self.user_id = kwargs['user_id']

    @classmethod
    def create(cls, **kwargs):
        new_characterfav = cls(**kwargs)
        db.session.add(new_characterfav)
        try:
            db.session.commit()
            return new_characterfav
        except Exception as error:
            raise Exception(error.args[0], 400)
        print(new_characterfav.id)
        return new_characterfav

    def serialize(self):
        return {
            "name": self.name,
            "character_id": self.character_id,
            "user_id": self.user_id
        }    

class PlanetFav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey('planet.id'))
    user_id = db.Column(db.Integer,ForeignKey ('user.id') )

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.planet_id = kwargs['planet_id']
        self.user_id = kwargs['user_id']
        
    @classmethod
    def create(cls, **kwargs):
        new_planetfav = cls(**kwargs)
        db.session.add(new_planetfav)
        try:
            db.session.commit()
            return new_planetfav
        except Exception as error:
            raise Exception(error.args[0], 400)
        print(new_planetfav.id)
        return new_planetfav

    def serialize(self):
        return {
            "name": self.name,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }   

class VehicleFav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.id'))
    user_id = db.Column(db.Integer,ForeignKey ('user.id') )

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.vehicle_id = kwargs['vehicle_id']
        self.user_id = kwargs['user_id']

    @classmethod
    def create(cls, **kwargs):
        new_vehiclefav = cls(**kwargs)
        db.session.add(new_vehiclefav)
        try:
            db.session.commit()
            return new_vehiclefav
        except Exception as error:
            raise Exception(error.args[0], 400)
        print(new_vehiclefav.id)
        return new_vehiclefav

    def serialize(self):
        return {
            "name": self.name,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id
        }  