from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query
from uuid import uuid4

@app.get('/api/restaurant')
def restaurant_get():
                # TODO: get request applicable to all users
    return
    
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
    return