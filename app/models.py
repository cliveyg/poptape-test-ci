# app/models.py
from app import db
from sqlalchemy.dialects.postgresql import JSON
import datetime

#-----------------------------------------------------------------------------#
# models match to tables in postgres
#-----------------------------------------------------------------------------#

class Country(db.Model):

    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    iso_code = db.Column(db.String(3), unique=True, nullable=False)

    def __init__(self, name, iso_code):
        self.name = name
        self.iso_code = iso_code

    def __repr__(self): # pragma: no cover 
        return '<id Country {}>'.format(self.id)
    

class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.String(50), unique=True, nullable=False)
    public_id = db.Column(db.String(50), nullable=False)
    house_name = db.Column(db.String(50))
    house_number = db.Column(db.String(50))
    address_line_1 = db.Column(db.String(150))
    address_line_2 = db.Column(db.String(150))
    address_line_3 = db.Column(db.String(150))
    state_region_county = db.Column(db.String(150))
    country_id = db.Column(db.Integer, db.ForeignKey(Country.id))
    post_zip_code = db.Column(db.String(30))
    created = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, address_id, public_id, house_name, house_number,
                 address_line_1, address_line_2, address_line_3,
                 state_region_county, country_id, post_zip_code):
        self.address_id = address_id
        self.public_id = public_id
        self.house_name = house_name
        self.house_number = house_number
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.state_region_county = state_region_county
        self.country_id = country_id
        self.post_zip_code = post_zip_code

    def __repr__(self): # pragma: no cover
        return '<id Address {}>'.format(self.id)

