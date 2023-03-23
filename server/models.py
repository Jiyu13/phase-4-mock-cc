from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship("HeroPower", backref="hero")
    powers = association_proxy("hero_powers", "power")

    serialize_rules = ("-hero_powers.hero", "-hero_powers.power", "-powers.heroes", "-created_at", "-updated_at")

    def __repr__(self):
        return f'''<Hero>'''


# add any models you may need. 
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship("HeroPower", backref="power")
    heroes = association_proxy("hero_prowers", "hero")

    serialize_rules = ("-hero_powers.power", "-hero_powers.hero", "-heroes.powers", "-created_at", "-updated_at")

    @validates("description")
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("description must be present and at least 20 characters long")
        return description

    def __repr__(self):
        return f'''<Power>'''


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))

    serialize_rules = ("-hero.hero_powers", "-power.hero_powers", 
                       "-heroes.powers", "-powers.heroes",
                       "-created_at", "-updated_at")

    @validates("strength")
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("strength must be one of the following values: 'Strong', 'Weak', 'Average'")
        return strength

    def __repr__(self):
        return f'''<HeroPower>'''