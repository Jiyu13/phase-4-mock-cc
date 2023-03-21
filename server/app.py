#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
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

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_dict = [hero.to_dict() for hero in heroes]
        return make_response(jsonify(heroes_dict), 200)

api.add_resource(Heroes, '/heroes')


class HeroByID(Resource):
    def get(self, id):
        try:
            hero = Hero.query.filter_by(id=id).first()
            print(hero.powers)
            # rules = ("-hero_powers",)
            response = make_response(jsonify(hero.to_dict()), 200)
            # by adding rules = ("-hero_powers",)
            # {
            #     "created_at": "2023-03-21 05:17:47",
            #     "id": 1,
            #     "name": "Kamala Khan",
            #     "super_name": "Ms. Marvel",
            #     "updated_at": null
            # }
        except:
            message = {"error": "Hero Not Found"}
            response = make_response(message, 404)
        return response
api.add_resource(HeroByID, '/heroes/<int:id>')


class GetPowers(Resource):
    def get(self):
        powers = Power.query.all()
        # rules = ('-hero_powers',) will not show hero_powers
        powers_dict = [power.to_dict(rules = ('-hero_powers',)) for power in powers]
        return make_response(jsonify(powers_dict), 200)
api.add_resource(GetPowers, "/powers")


class GetPowerByID(Resource):
    def get(self, id):
        try: 
            power = Power.query.filter_by(id=id).first()
            # rules = ("-hero_powers",))
            return make_response(jsonify(power.to_dict()), 200)
        except:
            response_body = {
                "error": "Power not found"
            }
            return make_response(response_body, 404)

    # ????
    def patch(self, id):
        try:
            power = Power.query.filter_by(id=id).first()
            # data = request.get_json()
            # power.name = data['name']
            # power.description = data['description']
            for attr in request.get_json():
                setattr(power, attr, request.get_json()[attr])
            db.session.add(power)
            db.session.commit()
            response = make_response(power.to_dict(), 200)
        except:
            response_body = {
                "error": "Power not found"
            }
            response = make_response(response_body, 404)
        return response
api.add_resource(GetPowerByID, "/powers/<int:id>")


class HeroPowers(Resource):
    def get(self):
        hero_powers = HeroPower.query.all()
        hero_powers_dict = [hero_power.to_dict() for hero_power in hero_powers]
        return make_response(hero_powers_dict, 200)

    def post(self):
        # try:
        #     new_hero_power = HeroPower(
        #         strength=request.get_json()["strength"],
        #         hero_id=request.get_json()["hero_id"],
        #         power_id=request.get_json()["power_id"]
        #     )
        #     db.session.add(new_hero_power)
        #     db.session.commit()

        # except :
        #     message = {
        #         "error": "Invalid input"
        #     }
        #     return make_response(jsonify(message), 422)
        # # ??? why new_hero_power.hero.
        # return make_response(new_hero_power.hero.to_dict(), 201)

        try:
            new_hero_power = HeroPower(
                strength=request.get_json()["strength"],
                hero_id=request.get_json()["hero_id"],
                power_id=request.get_json()["power_id"]
            )
            db.session.add(new_hero_power)
            db.session.commit()

            hero = Hero.query.filter(Hero.id == new_hero_power.hero_id).first()
            hero_dict = hero.to_dict()
            response = make_response(jsonify(hero_dict), 201)

        except ValueError:
            message = {
                "error": "Invalid input"
            }
            response = make_response(jsonify(message), 400)
        return response
api.add_resource(HeroPowers, '/hero_powers')


class HeroPowerByID(Resource):
    def get(self, id):
        hero_power = HeroPower.query.filter_by(id=id).first()
        # rules=("-hero",)
        return make_response(hero_power.to_dict(), 200)
api.add_resource(HeroPowerByID, '/hero_powers/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
