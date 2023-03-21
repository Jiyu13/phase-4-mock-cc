#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods = ['GET'])
def heroes():
    heroes = Hero.query.all()
    heroes_dict = [hero.to_dict(rules = ('-hero_powers',)) for hero in heroes]

    response = make_response(
        jsonify(heroes_dict),
        200
    )

    return response

@app.route('/heroes/<int:id>', methods = ['GET'])
def heroByID(id):
    hero = Hero.query.filter_by(id = id).first()

    if hero:

        hero_dict = hero.to_dict()

        response = make_response(
            jsonify(hero_dict),
            200
        )

    else:

        response = make_response(
            {"error": "Hero not found"},
            404
        )

    return response

@app.route('/powers', methods = ['GET'])
def powers():
    powers = Power.query.all()
    powers_dict = [power.to_dict(rules = ('-hero_powers',)) for power in powers]

    response = make_response(
        jsonify(powers_dict),
        200
    )

    return response

@app.route('/powers/<int:id>', methods = ['GET', 'PATCH'])
def powerByID(id):
    power = Power.query.filter_by(id = id).first()

    if power:

        if request.method == 'GET':

            power_dict = power.to_dict()

            response = make_response(
                jsonify(power_dict),
                200
            )

        elif request.method == 'PATCH':

            try:

                for key in request.get_json():
                    setattr(power, key, request.get_json()[key])

                db.session.add(power)
                db.session.commit()

                power_dict = power.to_dict()

                response = make_response(
                    jsonify(power_dict),
                    200
                )

            except ValueError:

                response = make_response(
                    {"error": "Invalid input"},
                    400
                )

    else:

        response = make_response(
            {"error": "Power not found"},
            404
        )

    return response

@app.route('/hero_powers', methods = ['POST'])
def heroPowers():

    try:

        new_hero_power = HeroPower(
            strength = request.get_json()['strength'],
            hero_id = request.get_json()['hero_id'],
            power_id = request.get_json()['power_id']
        )

        db.session.add(new_hero_power)
        db.session.commit()

        hero = Hero.query.filter(Hero.id == new_hero_power.hero_id).first()
        hero_dict = hero.to_dict()

        response = make_response(
            jsonify(hero_dict),
            201
        )

    except ValueError:

        response = make_response(
            {"error": "Invalid input"},
            400
        )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)