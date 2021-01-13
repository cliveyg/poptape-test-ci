# app/main/views.py
from app import limiter, db, flask_uuid
from flask import jsonify, request, abort
from flask import current_app as app
from app.main import bp
from app.models import Country, Address
from app.decorators import require_access_level
from app.assertions import assert_valid_schema
from sqlalchemy.exc import SQLAlchemyError
from jsonschema.exceptions import ValidationError as JsonValidationError
import uuid

# reject any non-json requests
@bp.before_request
def only_json():
    if not request.is_json:
        abort(400)

# -----------------------------------------------------------------------------
# helper route - useful for checking status of api in api_server application

@bp.route('/address/status', methods=['GET'])
@limiter.limit("100/hour")
def system_running():
    app.logger.info("Praise the FSM! The sauce is ready")
    return jsonify({ 'message': 'System running...' }), 200

# -----------------------------------------------------------------------------
# returns a list of addresses for the authenticated user

@bp.route('/address', methods=['GET'])
@limiter.limit("20/hour")
@require_access_level(10, request)
def get_all_addresses_for_user(public_id, request):

    addresses = []
    try:
        addresses = db.session.query(Address.address_id,
                                     Address.house_name,
                                     Address.house_number,
                                     Address.address_line_1,
                                     Address.address_line_2,
                                     Address.address_line_3,
                                     Address.state_region_county,
                                     Country.name,
                                     Country.iso_code,
                                     Address.post_zip_code).join(Country)\
                                                           .filter(Address.public_id == public_id)\
                                                           .all()

    except: 
        jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 502

    if len(addresses) == 0:
        return jsonify({ 'message': 'no addresses found for user' }), 404

    adds = []
    for address in addresses:
        address_data = {}
        address_data['address_id'] = address.address_id
        address_data['house_name'] = address.house_name
        address_data['house_number'] = address.house_number
        address_data['address_line_1'] = address.address_line_1
        address_data['address_line_2'] = address.address_line_2
        address_data['address_line_3'] = address.address_line_3
        address_data['state_region_county'] = address.state_region_county
        address_data['country'] = address.name
        address_data['country_code'] = address.iso_code
        address_data['post_zip_code'] = address.post_zip_code
        adds.append(address_data)

    return jsonify({ 'addresses': adds }), 200

# -----------------------------------------------------------------------------
# creates an address for the authenticated user

@bp.route('/address', methods=['POST'])
@limiter.limit("10/hour")
@require_access_level(10, request)
def get_create_address_for_user(public_id, request):

    # check input is valid json
    try:
        data = request.get_json()
    except:
        return jsonify({ 'message': 'Check ya inputs mate. Yer not valid, Jason'}), 400

    # validate input against json schemas
    try:
        country_data = { 'iso_code': data.get('iso_code') }
        assert_valid_schema(country_data, 'country')
        assert_valid_schema(data, 'address')

    except JsonValidationError as err:
        return jsonify({ 'message': 'Check ya inputs mate.', 'error': err.message }), 400

    country = Country.query.filter_by(iso_code = country_data.get('iso_code')).first()
    address = Address(public_id = public_id,
                      address_id = str(uuid.uuid4()),
                      house_name = data.get('house_name'),
                      house_number = data.get('house_number'),
                      address_line_1 = data.get('address_line_1'),
                      address_line_2 = data.get('address_line_2'),
                      address_line_3 = data.get('address_line_3'),
                      state_region_county = data.get('state_region_county'),
                      post_zip_code = data.get('post_zip_code'),
                      country_id = country.id)

    try:
        db.session.add(address)
        db.session.flush()
        db.session.commit()
    except (SQLAlchemyError, DBAPIError) as e:
        db.session.rollback()
        return jsonify({ 'message': 'oopsy, something went wrong at our end' }), 422
   
    message = {}
    message['message'] = 'address created successfully'
    message['address_id'] = address.address_id
    return jsonify( message ), 201

# -----------------------------------------------------------------------------
# returns an individual address - returns 401 if not authorized on that
# address uuid

@bp.route('/address/<uuid:address_id>', methods=['GET'])
@limiter.limit("100/hour")
@require_access_level(10, request)
def get_one_address(public_id, request, address_id):

    # convert to string
    address_id = str(address_id)
    address = None
    try:
        address = db.session.query(Address.house_name,
                                   Address.house_number,
                                   Address.address_line_1,
                                   Address.address_line_2,
                                   Address.address_line_3,
                                   Address.state_region_county,
                                   Country.name,
                                   Country.iso_code,
                                   Address.post_zip_code).join(Country)\
                                                         .filter(Address.address_id == address_id)\
                                                         .first()
    except:
        return jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 502

    if not address:
        message = "no addresses found for supplied id ["+address_id+"]"
        return jsonify({ 'message': message }), 404

    # i prefer to explicitly assign variables returned to ensure no 
    # accidental exposure of private data
    address_data = {}
    address_data['house_name'] = address.house_name
    address_data['house_number'] = address.house_number
    address_data['address_line_1'] = address.address_line_1
    address_data['address_line_2'] = address.address_line_2
    address_data['address_line_3'] = address.address_line_3
    address_data['state_region_county'] = address.state_region_county
    address_data['country'] = address.name
    address_data['country_code'] = address.iso_code
    address_data['post_zip_code'] = address.post_zip_code

    return jsonify(address_data), 200

# -----------------------------------------------------------------------------
# deletes an address for the authenticated user

@bp.route('/address/<uuid:address_id>', methods=['DELETE'])
@limiter.limit("10/hour")
@require_access_level(10, request)
def delete_address_for_user(public_id, request, address_id):

    address_id = str(address_id)
    try:
        result = Address.query.filter(Address.address_id == address_id)\
                              .filter(Address.public_id == public_id)\
                              .delete()
    except SQLAlchemyError as err:
        return jsonify({ 'message': 'naughty, naughty' }), 401

    if result:
        return '', 204

    return jsonify({ 'message': 'nope sorry, that\'s not happening today' }), 401

# -----------------------------------------------------------------------------
# returns a list of all possible countries - names and 3 alpha iso codes

@bp.route('/address/countries', methods=['GET'])
@limiter.limit("100/hour")
def list_countries():

    countries = []
    results = Country.query.all()

    for country in results:
        country_data = {}
        country_data['name'] = country.name
        country_data['iso_code'] = country.iso_code
        countries.append(country_data)

    return jsonify({ 'countries': countries }), 200

# -----------------------------------------------------------------------------
# admin routes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# get all addresses - paginated - limited in config at present
@bp.route('/address/admin/address', methods=['GET'])
@limiter.limit("100/hour")
@require_access_level(5, request)
def get_all_addresses_admin_method(public_id, request):

    # pagination allowed on this url
    page = request.args.get('page', 1, type=int)

    addresses = []
    total_records = 0
    addresses_per_page = int(app.config['ADDRESS_LIMIT_PER_PAGE'])
    try:
        total_records = db.session.query(Address).count() 

        addresses = db.session.query(Address.address_id,
                                     Address.public_id,
                                     Address.house_name,
                                     Address.house_number,
                                     Address.address_line_1,
                                     Address.address_line_2,
                                     Address.address_line_3,
                                     Address.state_region_county,
                                     Country.name,
                                     Country.iso_code,
                                     Address.post_zip_code)\
                                            .join(Country)\
                                            .paginate(page,\
                                                      addresses_per_page, False).items

    except:
        return jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 500

    if len(addresses) == 0:
        return jsonify({ 'message': 'no addresses found for user' }), 404

    adds = []
    for address in addresses:
        address_data = {}
        address_data['address_id'] = address.address_id
        address_data['house_name'] = address.house_name
        address_data['house_number'] = address.house_number
        address_data['address_line_1'] = address.address_line_1
        address_data['address_line_2'] = address.address_line_2
        address_data['address_line_3'] = address.address_line_3
        address_data['state_region_county'] = address.state_region_county
        address_data['country'] = address.name
        address_data['country_code'] = address.iso_code
        address_data['post_zip_code'] = address.post_zip_code
        adds.append(address_data)

    output = { 'addresses': adds }
    output['total_records'] = total_records
    total_so_far = page * addresses_per_page
    
    if total_so_far < total_records:
        npage = page + 1
        output['next_url'] = '/address/admin/address?page='+str(npage)

    if page > 1:
        ppage = page - 1
        output['prev_url'] = '/address/admin/address?page='+str(ppage)

    return jsonify(output), 200

# -----------------------------------------------------------------------------
# route for testing rate limit works - generates 429 if more than two calls
# per minute to this route - restricted to admin users and above
@bp.route('/address/admin/ratelimited', methods=['GET'])
@require_access_level(5, request)
@limiter.limit("0/minute")
def rate_limted(public_id, request):
    return jsonify({ 'message': 'should never see this' }), 200

# -----------------------------------------------------------------------------
# route for anything left over - generates 404

@bp.route('/address/<everything_left>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def not_found(everything_left):
    message = 'resource ['+everything_left+'] not found'
    return jsonify({ 'message': message }), 404
