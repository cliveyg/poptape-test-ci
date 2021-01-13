# app/tests/fixtures.py

from app import db
from app.models import Country, Address
import uuid
import os.path
import os
import csv
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
load_dotenv()

# countries and addresses for testings

# -----------------------------------------------------------------------------

def getPublicID():
    return "fef0b81e-6b39-417c-ab4f-4be1ac4f2c66"

# -----------------------------------------------------------------------------

def getAdminID():
    return "a3893f8b-63e6-4bb7-8147-713738912bd5"

# -----------------------------------------------------------------------------

def addTestCountries():
    country1 = Country(name = "United Kingdom", iso_code = "GBR")
    country2 = Country(name= "Germany", iso_code = "DEU")
    country3 = Country(name= "Brazil", iso_code = "BRA")
    country4 = Country(name= "France", iso_code = "FRA")
    db.session.add(country1)
    db.session.add(country2)
    db.session.add(country3)
    db.session.add(country4)
    countries = [country1, country2, country3, country4]
    db.session.commit()
    return countries

# -----------------------------------------------------------------------------

def addTestAddresses():

    # check if countries are present and if not then add them
    countries = []
    countries = Country.query.all()
    if len(countries) == 0:
        countries = addTestCountries()

    address1 = Address(address_id = str(uuid.uuid4()),
                       public_id  = getPublicID(),
                       house_name = "The Cottage",
                       house_number = "",
                       address_line_1 = "Mill Lane",
                       address_line_2 = "Brixton",
                       address_line_3 = "",
                       state_region_county = "London",
                       country_id = countries[0].id,
                       post_zip_code = "SW9 4RF")

    address2 = Address(address_id = str(uuid.uuid4()),
                       public_id  = "376a3fcc-5574-4a3e-91f2-066ca80a9900",
                       house_name = "",
                       house_number = "45",
                       address_line_1 = "High Street",
                       address_line_2 = "Belper",
                       address_line_3 = "",
                       state_region_county = "Derbyshire",
                       country_id = countries[0].id,
                       post_zip_code = "DE21 6JH")

    address3 = Address(address_id = str(uuid.uuid4()),
                       public_id  = getPublicID(),
                       house_name = "",
                       house_number = "11A",
                       address_line_1 = "Queens Road",
                       address_line_2 = "Outer Bowden",
                       address_line_3 = "Great Weedon",
                       state_region_county = "Cornwall",
                       country_id = countries[0].id,
                       post_zip_code = "TR4 8DH") 

    address4 = Address(address_id = str(uuid.uuid4()),
                       public_id  = getPublicID(),
                       house_name = "Sitío Trinca Ferro",
                       house_number = "",
                       address_line_1 = "Morro da Praia Brava",
                       address_line_2 = "Paraty",
                       address_line_3 = "",
                       state_region_county = "Rio de Janeiro",
                       country_id = countries[2].id,
                       post_zip_code = "239700-000")

    address5 = Address(address_id = str(uuid.uuid4()),
                       public_id  = getAdminID(),
                       house_name = "A loja",
                       house_number = "54",
                       address_line_1 = "Rua Santa Clara",
                       address_line_2 = "Paraty",
                       address_line_3 = "",
                       state_region_county = "Rio de Janeiro",
                       country_id = countries[2].id,
                       post_zip_code = "239700-000")

    address6 = Address(address_id = str(uuid.uuid4()),
                       public_id  = getAdminID(),
                       house_name = "",
                       house_number = "765",
                       address_line_1 = "Clubstraße",
                       address_line_2 = "Berlin",
                       address_line_3 = "",
                       state_region_county = "",
                       country_id = countries[1].id,
                       post_zip_code = "2 6 1 3 3")    

    db.session.add(address1)
    db.session.add(address2)
    db.session.add(address3)
    db.session.add(address4)
    db.session.add(address5)
    db.session.add(address6)
    addresses = [address1, address2, address3, address4]
    db.session.commit()

    return addresses

# -----------------------------------------------------------------------------

def addAllCountries(): # pragma: no cover
    
    # load csv file
    countries_file = os.getenv('COUNTRIES_CSV')
    filepath = os.path.join(os.path.dirname(__file__), countries_file)
    errors = []

    with open(filepath) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',') 
        for row in csv_reader:

            country = Country(name = row[0], iso_code = row[1])
            try:
                db.session.add(country)
                db.session.flush()
                db.session.commit()
            except (SQLAlchemyError, DBAPIError) as err:
                errors.append(err)
                db.session.rollback() 

    if len(errors) > 0:
        print("Errors generated when loading database!")
        return False
    return True

