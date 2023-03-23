from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# relationship - one to many
# proxy - cross table

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # 
    hero_powers = db.relationship("HeroPower", backref="hero")

    # A Hero has many Powers through HeroPower: pl first, grab whole table
    # singular: power reference the column
    powers = association_proxy("hero_powers", "power",)
    
    # hero_power reference to one hero and one power
    # -hero_powers.hero -> extract only hero_id instead of the whole hero object
    # '-powers.heroes' does nothing here
    serialize_rules = ('-hero_powers.hero', '-powers.heroes',)

    def __repr__(self):
        return f'''<Hero ID: {self.id}, name: {self.name}, super_name: {self.super_name}>'''

# add any models you may need. 
class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # create a hero_powers.power in HeroPower (Child) class
    hero_powers = db.relationship("HeroPower", backref="power")
    heroes = association_proxy("hero_powers", "hero")

    # serialize_rules = ('-hero_powers', '-heroes.powers', '-created_at', '-updated_at')
    # serialize_rules = ('-hero_powers.hero', '-hero_power.power', '-powers.heroes')

    # '-hero_powers.power', will not show power obj
    serialize_rules = ('-hero_powers.power', '-heroes.powers',)


    @validates("description")
    def validate_description(self, key, description):
        if not description and len(description) < 20:
            raise ValueError("description must be present and at least 20 characters long.")
        return description

    def __repr__(self):
        return f'''<Power ID: {self.id}, name: {self.name}, description: {self.description}>'''


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # one to many=hero->many hero_powers, power->many hero_powers 
    # serialize_rules = ('-hero.hero_powers', '-power.hero_powers', )

    # '-power.hero_powers', -> will not show hero_powers inside power
    # '-hero.hero_powers', "-hero_power.heros", -> don't change anything 
    serialize_rules = ('-power.hero_powers', '-hero.hero_powers',)

    @validates('strength')
    def validate_strength(self, key, strength):
        strength_values = ['Strong', 'Weak', 'Average']
        if strength not in strength_values:
            raise ValueError("strength must be one of the following values: 'Strong', 'Weak', 'Average'.")
        return strength


    def __repr__(self):
        return f'''<HeroPower ID: {self.id}, strength: {self.strength}>'''



# strength_values = ['Strong', 'Weak', 'Average']
# strength = "Weak"
# if len(strength) < 6 or strength not in strength_values:
#     print("strength < 3 and not in strength_values")
# print("meet both condition")