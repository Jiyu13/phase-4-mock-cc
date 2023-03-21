from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata = metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # set many to many relationships through model HeroPower, reference back to hero
    hero_powers = db.relationship("HeroPower", backref="hero")

    # set a joined table with association proxy,
    # there's a association through the hero_powers table's power column
    powers = association_proxy('hero_powers', 'power')

    # serialize_rules
    serialize_rules = ('-hero_powers.hero')

    def __repr__(self):
        return f'''<Hero {self.id}; Name: {self.name}; Super Name: {self.super_name}>'''



class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # set many to many relationships through model HeroPower, reference back to power
    hero_powers = db.relationship("HeroPower", backref="power")

    # set a joined table with association proxy,
    # there's a association through the hero_powers table's hero column
    heros = association_proxy('hero_powers', 'hero')

    # serialize_rules
    serialize_rules = ('-hero_powers.power')

    @validates("description")
    def validate_description(self, key, description):
        if not description and not len(description) >= 20:
            raise ValueError("description must be present and at least 20 characters long")
        return description


    def __repr__(self):
        return f'''<Power {self.id}; Name: {self.name}; Description: {self.description}>'''



class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # set foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    # serialize_rules
    serialize_rules = ('-hero.hero_powers', "-power.hero_powers")


    @validates("strength")
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("strength must be one of the following values: 'Strong', 'Weak', 'Average'")
        return strength

# add any models you may need. 