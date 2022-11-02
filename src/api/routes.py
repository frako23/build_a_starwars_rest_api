"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Vehicle, CharacterFav, PlanetFav, VehicleFav
from api.utils import generate_sitemap, APIException
import requests

api = Blueprint('api', __name__)

users = []

@api.route('/users', methods=['GET','POST'])
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        users_dictionaries = []
        for user in users:
            users_dictionaries.append(user.serialize())
        return jsonify(users_dictionaries), 200
    new_user_data = request.json
    try:
        new_user = User.create(**new_user_data)
        return jsonify(new_user.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]

characters = []

@api.route('/people', methods=['GET','POST'])
def get_characters():
    if request.method == 'GET':
        characters = Character.query.all()
        characters_dictionaries = []
        for character in characters:
            characters_dictionaries.append(character.serialize())
        return jsonify(characters_dictionaries), 200
    new_character_data = request.json
    try:
        new_character = Character.create(**new_character_data)
        return jsonify(new_character.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]

planets = []

@api.route('/planets', methods=['GET', 'POST'])
def get_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets_dictionaries = []
        for planet in planets:
            planets_dictionaries.append(planet.serialize())
        return jsonify(planets_dictionaries), 200
    new_planet_data = request.json
    try:
        new_planet = Planet.create(**new_planet_data)
        return jsonify(new_planet.serialize()), 201
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]

vehicles = []

@api.route('/vehicles', methods=['GET', 'POST'])
def get_vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        vehicles_dictionaries = []
        for vehicle in vehicles:
            vehicles_dictionaries.append(vehicle.serialize())
        return jsonify(vehicles_dictionaries), 200
    new_vehicle_data = request.json
    try:
        new_vehicle = Vehicle.create(**new_vehicle_data)
        return jsonify(new_vehicle.serialize()), 201
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]

favorites = []

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    if request.method == 'GET':
        favorites_characters = CharacterFav.query.all()
        favorites_planets = PlanetFav.query.all()
        favorites_vehicles = VehicleFav.query.all()
        favorites_dictionaries = []
        for character in favorites_characters:
            favorites_dictionaries.append(character.serialize())
        for planet in favorites_planets:
            favorites_dictionaries.append(planet.serialize())
        for vehicle in favorites_vehicles:
            favorites_dictionaries.append(vehicle.serialize())
        return jsonify(favorites_dictionaries), 200

@api.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['POST', 'DELETE'])
def add_people_favorites(user_id, people_id):
    if request.method == 'POST':
        new_people_favorite = request.json
        try:
            new_people_favorite = CharacterFav.create(user_id = user_id, character_id = people_id, **new_people_favorite)
            return jsonify(new_people_favorite.serialize()), 201
        except Exception as error:
            return jsonify(error.args[0]), 500
    else:
        variable = CharacterFav.query.filter_by(user_id=user_id, character_id=people_id).delete()
        try:
            if variable == 0:
                raise Exception("no hay favoritos", 404)
            db.session.commit()
            return jsonify({"mensaje": "Se elimino correctamente"})
        except Exception as error:
            return jsonify(error.args[0]), error.args[1]

@api.route('/favorite/planets/<int:user_id>/<int:planet_id>', methods=['POST', 'DELETE'])
def add_planets_favorites(user_id, planet_id):
    if request.method == 'POST':
        new_planet_favorite = request.json
        try:
            new_planet_favorite = PlanetFav.create(user_id = user_id, planet_id = planet_id, **new_planet_favorite)
            return jsonify(new_planet_favorite.serialize()),201
        except Exception as error:
            return jsonify(error.args[0]), 500
    else:
        variable = PlanetFav.query.filter_by(user_id=user_id, planet_id=planet_id).delete()
        try:
            if variable == 0:
                raise Exception("no hay favoritos", 404)
            db.session.commit()
            return jsonify({"mensaje": "Se elimino correctamente"})
        except Exception as error:
                return jsonify(error.args[0]), error.args[1]

@api.route('/favorite/vehicles/<int:user_id>/<int:vehicle_id>', methods=['POST', 'DELETE'])
def add_vehicles_favorites(user_id, vehicle_id):
    if request.method == 'POST':
        new_vehicle_favorite = request.json
        try:
            new_vehicle_favorite = VehicleFav.create(user_id = user_id, vehicle_id = vehicle_id, **new_vehicle_favorite)
            return jsonify(new_vehicle_favorite.serialize()),201
        except Exception as error:
            return jsonify(error.args[0]), 500
    else:
        variable = VehicleFav.query.filter_by(user_id = user_id, vehicle_id = vehicle_id).delete()
        try:
            if variable == 0:
                raise Exception("no hay favoritos", 404)
            db.session.commit()
            return jsonify({"mensaje": "Se elimino correctamente"})
        except Exception as error:
                    return jsonify(error.args[0]), error.args[1]

@api.route('/input_data/planets', methods=['POST'])
def input_data_planets():
    response = requests.get('https://swapi.dev/api/planets')
    data = response.json()
    planets = Planet.query.all()
    if len(planets) == data['count']:
        return jsonify("Los planetas ya existen"), 400
    
    null = False
    def query():
        count = 0
        for number in range(len(data['results'])):
            Planet.create(name = data['results'][number]['name'], population = data['results'][number]['population'], climate = data['results'][number]['climate'], terrain = data['results'][number]['terrain'])
        count = count + 1
        return query()
    
    while not null:
        response = requests.get(data['next'])
        data = response.json()
        query()
        null = data['next'] is None

    return jsonify(f'Se han creado {count} planetas') 