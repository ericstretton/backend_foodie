
from app import app
from flask import jsonify, request, Response
from helpers.db_helpers import run_query
from uuid import uuid4
from helpers.data_functions import *

@app.get('/api/restaurant')
def restaurant_get():
                # TODO: get request applicable to all users
    params = request.args
    rest_id = params.get('id')
    
    
    if len(params.keys()) == 0:
        all_restaurants = run_query('SELECT restaurant.id, restaurant.address, restaurant.banner_url, restaurant.bio, city.name, restaurant.email, restaurant.phoneNum, restaurant.profile_url FROM restaurant INNER JOIN city ON city.id=restaurant.city')
        all_restaurants_list = []
        for rest in all_restaurants:
            restaurant = restaurant_dictionary_query(rest)
            all_restaurants_list.append(restaurant)
        return jsonify('get_all request success', all_restaurants_list)
    
    elif len(params.keys()) >= 1:
        if rest_id.isdigit() <= False:
            return Response('Error, invalid rest_id', status=400)
        check_id_validity = run_query('SELECT EXISTS(SELECT id FROM restaurant WHERE id=?)', [rest_id])
        response = check_id_validity[0]
        
        if response[0] == 1:
            
            restaurant_info = run_query('SELECT restaurant.id, restaurant.address, restaurant.banner_url, restaurant.bio, city.name, restaurant.email, restaurant.phoneNum, restaurant.profile_url FROM restaurant INNER JOIN city ON city.id=restaurant.city WHERE restaurant.id=?', [rest_id])
            resp = restaurant_dictionary_query(restaurant_info[0])
            resp_list = []
            resp_list.append(resp)
            
            return jsonify('Restaurant request successful', resp_list), 201
        else:
            return jsonify('Error, invalid rest_id'), 400
    else:
        return jsonify('Error paramaters exceeded limit, 0 / 1')
    
@app.post('/api/restaurant')
def restaurant_post():
                    # TODO STRETTON, update pw protection w salt, hash
                    
                    # TODO: make a join for city or look up if city exists, if not return response that it is not in the table
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    address = data.get('address')
    phoneNum = data.get('phoneNum')
    bio = data.get('phoneNum')
    profile_url = data.get('profile_url')
    banner_url = data.get('banner_url')
    city = data.get('city')
    if not name:
        return jsonify('Missing required argument: name'), 422
    if not email: 
        return jsonify('Missing required argument: email'), 422
    if not address:
        return jsonify('Missing required argument: address'), 422
    if not phoneNum:
        return jsonify('Missing required argument: phoneNum'), 422
    if not password:
        return jsonify('Missing required argument: password'), 422
    if not city:
        return jsonify('Missing required argument: city'), 422
    elif city == True:
        city_check = run_query('SELECT city.name FROM city INNER JOIN restaurant WHERE restaurant.city=city.id')
        print(city_check)
        if city != city_check:
            return jsonify('Errror valid city has not been selected.'), 422
        
    run_query("INSERT INTO restaurant (email, name, password, phoneNum, address, city, bio, profile_url, banner_url) VALUE(?,?,?,?,?,?,?,?,?)", [email, name, password, phoneNum, address, city, bio, profile_url, banner_url ])
    token = str(uuid4())
    resp = []
    restaurant_info = run_query('SELECT id FROM restaurant WHERE email=? and password=?', [email, password])
    for info in restaurant_info:
        restaurantId = {}
        restaurantId = info[0]
        resp.append(restaurantId)
    run_query("INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)", [token, restaurantId])
     
    return jsonify('Restaurant created', 'restaurant_id: ', restaurantId), 201


@app.patch('/api/restaurant')
def restaurant_patch():
            # TODO: get token from restaurant_session table for authentication for restaurant 
    params = request.args
    rest_token = params.get('rest_token')
    rest_id = params.get('rest_id')
    id = run_query('SELECT EXISTS(SELECT id FROM restaurant WHERE id=?', [rest_id])
    if rest_id != id:
        return Response('ERROR, Restaurant Id not in database', status=400)
    else:
        token = run_query('SELECT EXISTS(SELECT token FROM restaurant_session WHERE token=?)', [rest_token])
        if token != rest_token:
            return Response('ERROR, Token not found in database')
        else:
            update_restaurant_info = run_query('PATCH address, email, phoneNum, bio, profile_url, banner_url FROM restaurant WHERE id=?', [rest_id])
            updated_info = restaurant_dictionary_query(update_restaurant_info)
            