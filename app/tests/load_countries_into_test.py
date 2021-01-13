# app/tests/load_countries_into_test.py

###############################################################################
### helper script to load country data into test db                        ####
###############################################################################

from .fixtures import addAllCountries # pragma: no cover
from flask import jsonify # pragma: no cover

from app import create_app, db # pragma: no cover
from app.models import Country # pragma: no cover
from app.config import TestConfig # pragma: no cover

from flask import current_app # pragma: no cover
from flask_testing import TestCase as FlaskTestCase # pragma: no cover


###############################################################################
####                      flask test case instance                         ####
###############################################################################

class MyTest(FlaskTestCase): # pragma: no cover

    ############################
    #### setup and teardown ####
    ############################

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

###############################################################################
####                               tests                                   ####
###############################################################################

    def test_load_testdb(self): # pragma: no cover
        result = addAllCountries()
        self.assertTrue(result, True)
        self.assertTrue('poptape_address_test' in
                       self.app.config['SQLALCHEMY_DATABASE_URI'])

        total_records = db.session.query(Country).count()
        self.assertTrue(total_records, 249)

# -----------------------------------------------------------------------------
