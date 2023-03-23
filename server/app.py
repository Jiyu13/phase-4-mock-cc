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
        heroes_dict = [hero.to_dict(rules=("-hero_powers", )) for hero in heroes]
        return make_response(jsonify(heroes_dict), 200)
api.add_resource(Heroes, "/heroes")


class HeroByID(Resource):
    def get(self, id):
        try:
            hero = Hero.query.filter_by(id=id).first()
            hero_dict = hero.to_dict(rules=("-hero_powers",))
            response = make_response(jsonify(hero_dict), 200)
        except ValueError:
            message = {
                "error": "Hero not found"
            }
            response = make_response(message, 404)
        return response
api.add_resource(HeroByID, "/heroes/<int:id>")


class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        powers_dict = [power.to_dict(rules=("-hero_powers",)) for power in powers]
        return make_response(powers_dict, 200)
api.add_resource(Powers, "/powers")


class PowerByID(Resource):
    def get(self, id):
        try:
            power = Power.query.filter_by(id=id).first()
            power_dict = power.to_dict(rules=("-hero_powers",))
            response = make_response(jsonify(power_dict), 200)
        except ValueError:
            message = {
                "error": "Hero not found"
            }
            response = make_response(message, 404)
        return response

    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            message = {
                "error": "Power not found"
            }
            return make_response(message, 404)
        else:
            try:
                for attr in request.get_json():
                    setattr(power, attr, request.get_json()[attr])
                db.session.add(power)
                db.session.commit()

                power_dict = power.to_dict(rules=("-hero_powers",))
                response = make_response(jsonify(power_dict), 200)
            except ValueError:
                message = {
                    "error": "Invalid input"
                }
                response = make_response(message, 422)
            return response
api.add_resource(PowerByID, "/powers/<int:id>")


class HeroPowers(Resource):
    def get(self):
        hero_powers = HeroPower.query.all()
        hero_powers_dict = [h_p.to_dict() for h_p in hero_powers]
        return make_response(jsonify(hero_powers_dict), 200)
    
    def post(self):
        try:
            new_hero_powers = HeroPower(
                strength=request.get_json()["strength"],
                hero_id=request.get_json()["hero_id"],
                power_id=request.get_json()["power_id"]
            )
            db.session.add(new_hero_powers)
            db.session.commit()
            
            # send back a response with the data related to the Hero
            hero = Hero.query.filter_by(id=new_hero_powers.hero_id).first()
            response = make_response(hero.to_dict(), 201)
        except ValueError:
            message = {"error": "Invalid input"}
            response = make_response(message, 422)
        return response
        
api.add_resource(HeroPowers, "/hero_powers")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
