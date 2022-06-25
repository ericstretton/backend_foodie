import bcrypt
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
            
            return jsonify(resp_list[0]), 201
        else:
            return jsonify('Error, invalid rest_id'), 400
    else:
        return jsonify('Error paramaters exceeded limit, 0 / 1')
    
@app.post('/api/restaurant')
def restaurant_post():
                    # TODO STRETTON, update pw protection w salt, hash
                    
                    # TODO: make a join for city or look up if city exists, if not return response that it is not in the table
    data = request.json
    if len(data.keys()) >= 6 and len(data.keys()) <= 9 :
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city'} or \
            {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio'} or \
                {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'profile_url'} or \
                    {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'profile_url', 'banner_url'} or \
                        {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'banner_url'} or \
                            {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'profile_url', 'banner_url'} or \
                                {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'profile_url'} or \
                                    {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'banner_url'}:
                                        new_restaurant = new_dictionary_request(data)
        else:
            return jsonify('Incorrect keys submitted'), 400
    else:
        return jsonify('Error, invalid amount of data submitted')
    
    if not new_restaurant['email']:
        return jsonify('Missing required argument: email'), 422
    elif not check_email(new_restaurant['email']):
        return jsonify("Error invalid email address submitted"), 400
    elif not check_length(new_restaurant['email'], 5, 75):
        return jsonify('ERROR, email must be between 5 and 75 characters'), 400
    
    check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_restaurant['email']])
    
    if check_email_validity == []:
        
        if not new_restaurant['name']:
            return jsonify('Missing required argument: name'), 422
        elif not check_length(new_restaurant['name'], 1, 75):
            return jsonify('ERROR, restaurant name must be between 1 and 75 characters'), 400
        
        if not new_restaurant['address']:
            return jsonify('Missing required argument: address'), 422
        elif not check_length(new_restaurant['address'], 6, 75):
            return jsonify('ERROR, address must be between 1 and 75 characters'), 400
        
        if not new_restaurant['phoneNum']:
            return jsonify('Missing required argument: phoneNum'), 422
        elif not check_length(new_restaurant['phoneNum'], 10, 25):
            return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
        
        if not new_restaurant['city']:
            return jsonify('Missing required argument: city'), 422
        elif new_restaurant['city'] == True:
            city_check = run_query('SELECT city.name FROM city INNER JOIN restaurant WHERE restaurant.city=city.id')
            print(city_check)
            if new_restaurant['city'] != city_check:
                return jsonify('Errror valid city has not been selected.'), 422
            
        if not new_restaurant['password']:
            return jsonify('Missing required argument: password'), 422
        elif not check_length(new_restaurant['password'], 6, 100):
                return jsonify('ERROR, password must be between 6 and 200 characters'), 400
        password = str(new_restaurant['password'])
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        
        # TODO : Need to make acceptions for handling no profile_url, banner_url, and bio
        
        
        if not check_length(new_restaurant['bio'], 1, 200):
            return jsonify('ERROR, bio must be between 1 and 200 characters'), 400
        if  new_restaurant['profile_url'] == False:
            pass
        elif not check_length(new_restaurant['profile_url'], 8, 300):
            return jsonify('ERROR, profile_url must be between 8 and 300 characters'), 400

        if not check_length(new_restaurant['banner_url'], 8, 300):
            return jsonify('ERROR, banner_url must be between 8 and 300 characters'), 400
        
        else:run_query("INSERT INTO restaurant (email, name, password, phoneNum, address, city, bio, profile_url, banner_url) VALUE(?,?,?,?,?,?,?,?,?)", [new_restaurant['email'], new_restaurant['name'], hashed_password, new_restaurant['phoneNum'], new_restaurant['address'], new_restaurant['city'], new_restaurant['bio'], new_restaurant['profile_url'], new_restaurant['banner_url'] ])
        
    else:
        email_validity = check_email_validity[0]
        if email_validity[0] == new_restaurant['email']:
            return jsonify('ERROR, email already exists'), 400
        
    restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_restaurant['email']])
    
    response = restaurant_id[0]
    
    check_response = response[0]
    
    token = str(uuid4())
    run_query("INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)", [token, check_response])
    
    return jsonify( 'restaurant_id: ', check_response, 'token: ', token), 201


@app.patch('/api/restaurant')
def restaurant_patch():
            # TODO: get token from restaurant_session table for authentication for restaurant 
    data = request.json
    token = data.get('token')
    
    if token != None:
        token_valid = run_query('SELECT token FROM restaurant_session WHERE token=?', [token])
        token_valid_response = token_valid[0]
        response = token_valid_response[0]
        

        if response == token:
            update_restaurant = new_dictionary_request(data)
            
            if 'email' in update_restaurant:
                if not check_length(update_restaurant['email'], 1, 75):
                    return jsonify('Invalid length, email must be between 1 and 75 characters')
                if not check_email(update_restaurant['email']):
                    return jsonify("Error, Not a valid email"), 400
                
                email_exists = run_query('SELECT email FROM restaurant WHERE email=?', [update_restaurant['email']])
                if email_exists != []:
                    return jsonify('Email already exists'), 400
                run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.email=? WHERE restaurant_session.token=?', [update_restaurant['email'], response])
                return jsonify(email_exists)
    # else:
    #     token = run_query('SELECT token FROM restaurant_session WHERE token=?)', [token])
    #     if token != rest_token:
    #         return Response('ERROR, Token not found in database')
    #     else:
    #         update_restaurant_info = run_query('PATCH address, email, phoneNum, bio, profile_url, banner_url FROM restaurant WHERE id=?', [rest_id])
    #         updated_info = restaurant_dictionary_query(update_restaurant_info)
            