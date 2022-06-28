import bcrypt
from app import app
from flask import jsonify, request, Response
from helpers.db_helpers import run_query
from uuid import uuid4
from helpers.data_functions import *

@app.get('/api/restaurant')
def restaurant_get():
    
    params = request.args
    rest_id = params.get('id')
    
    if len(params.keys()) == 0:
        all_restaurants = run_query('SELECT restaurant.id, restaurant.address, restaurant.banner_url, restaurant.name,  city.name, restaurant.email, restaurant.phoneNum, restaurant.bio, restaurant.profile_url FROM restaurant INNER JOIN city ON city.id=restaurant.city')
        all_restaurants_list = []
        for rest in all_restaurants:
            restaurant = restaurant_get_dict(rest)
            all_restaurants_list.append(restaurant)
        return jsonify('get_all request success', all_restaurants_list)
    
    elif len(params.keys()) >= 1:
        if rest_id.isdigit() <= False:
            return Response('Error, invalid rest_id', status=400)
        check_id_validity = run_query('SELECT EXISTS(SELECT id FROM restaurant WHERE id=?)', [rest_id])
        response = check_id_validity[0]
        
        if response[0] == 1:
            
            restaurant_info = run_query('SELECT restaurant.id, restaurant.address, restaurant.banner_url, restaurant.name,  city.name, restaurant.email, restaurant.phoneNum, restaurant.bio, restaurant.profile_url FROM restaurant INNER JOIN city ON city.id=restaurant.city WHERE restaurant.id=?', [rest_id])
            resp = restaurant_get_dict(restaurant_info[0])
            resp_list = []
            resp_list.append(resp)
            
            return jsonify(resp_list[0]), 201
        else:
            return jsonify('Error, invalid rest_id'), 400
    else:
        return jsonify('Error paramaters exceeded limit, 0 / 1')
    
@app.post('/api/restaurant')
def restaurant_post():

    data = request.json
    
    if len(data.keys()) >= 6 and len(data.keys()) <= 9:
        
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            if 'email' in new_rest:
                
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city) VALUES (?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
            
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            if 'email' in new_rest:
                
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
            
            if 'bio' in new_rest:
                if not check_length(new_rest['bio'], 1, 200):
                    return jsonify('ERROR, bio must be between 1 and 200 characters'), 400
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, bio) VALUES (?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['bio']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
            
            
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'profile_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            if 'email' in new_rest:
                
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
                
            if 'bio' in new_rest:
                if not check_length(new_rest['bio'], 1, 200):
                    return jsonify('ERROR, bio must be between 1 and 200 characters'), 400
            
            if 'profile_url' in new_rest:
                if not check_length(new_rest['profile_url'], 1, 300):
                    return jsonify('ERROR, profile_url must be between 1 and 300 characters'), 400
            
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, bio, profile_url) VALUES (?,?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['bio'], new_rest['profile_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
                
                
                
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'profile_url', 'banner_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            
                
            if 'email' in new_rest:
            
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
                
            if 'bio' in new_rest:
                if not check_length(new_rest['bio'], 1, 200):
                    return jsonify('ERROR, bio must be between 1 and 200 characters'), 400
            
            if 'profile_url' in new_rest:
                if not check_length(new_rest['profile_url'], 1, 300):
                    return jsonify('ERROR, profile_url must be between 1 and 300 characters'), 400
            
            if 'banner_url' in new_rest:
                if not check_length(new_rest['banner_url'], 1, 300):
                    return jsonify('ERROR, banner_url must be between 1 and 300 characters'), 400
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, bio, profile_url, banner_url) VALUES (?,?,?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['bio'], new_rest['profile_url'], new_rest['banner_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
                
                
                        
                                    
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'bio', 'banner_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            if 'email' in new_rest:
            
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
                
            if 'bio' in new_rest:
                if not check_length(new_rest['bio'], 1, 200):
                    return jsonify('ERROR, bio must be between 1 and 200 characters'), 400
            
            if 'banner_url' in new_rest:
                if not check_length(new_rest['banner_url'], 1, 300):
                    return jsonify('ERROR, banner_url must be between 1 and 300 characters'), 400
            
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, bio, banner_url) VALUES (?,?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['bio'], new_rest['banner_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201                
                
                
                
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'profile_url', 'banner_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            if 'email' in new_rest:
            
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
            
            if 'profile_url' in new_rest:
                if not check_length(new_rest['profile_url'], 1, 300):
                    return jsonify('ERROR, profile_url must be between 1 and 300 characters'), 400
            
            if 'banner_url' in new_rest:
                if not check_length(new_rest['banner_url'], 1, 300):
                    return jsonify('ERROR, banner_url must be between 1 and 300 characters'), 400
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, profile_url, banner_url) VALUES (?,?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['profile_url'], new_rest['banner_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
            
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city', 'profile_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            
            if 'email' in new_rest:
            
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
            
            if 'profile_url' in new_rest:
                if not check_length(new_rest['profile_url'], 1, 300):
                    return jsonify('ERROR, profile_url must be between 1 and 300 characters'), 400
                
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, profile_url) VALUES (?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['profile_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201    
            
            
            
        if {'email', 'password', 'name', 'address', 'phoneNum', 'city','banner_url'} == data.keys():
            new_rest = new_dictionary_request(data)
            
            if 'email' in new_rest:
                
                if not new_rest['email']:
                    return jsonify('Missing required key: email'), 422
                if not check_email(new_rest['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_rest['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400

                check_email_validity = run_query('SELECT email FROM restaurant WHERE email=?', [new_rest['email']])
                    
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_rest['email']:
                        return jsonify('ERROR, email already exists'), 400

            if 'password' in new_rest:
            
                if not new_rest['password']:
                    return jsonify('Missing required key: password'), 422
                if not check_length(new_rest['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_rest['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            if 'name' in new_rest:
                    if not new_rest['name']:
                        return jsonify('Missing required key: name'), 422
                    if not check_length(new_rest['name'], 1, 50):
                        return jsonify('ERROR, name must be between 1 and 50 characters')
                    
                    
            if 'address' in new_rest:
                if not new_rest['address']:
                    return jsonify('Missing required argument: address'), 422
                if not check_length(new_rest['address'], 6, 75):
                    return jsonify('ERROR, address must be between 1 and 75 characters'), 
                
                
            if 'phoneNum' in new_rest:
                if not new_rest['phoneNum']:
                    return jsonify('Missing required argument: phoneNum'), 422
                if not check_length(new_rest['phoneNum'], 10, 25):
                    return jsonify('ERROR, phone number must be between 10 and 25 characters'), 400
                
                
            if 'city' in new_rest:
                if not new_rest['city']:
                    return jsonify('Missing required argument: phoneNum'), 422
                city_check = run_query('SELECT name, id FROM city WHERE name=?', [new_rest["city"]])
                city_name_check = city_check[0]
                city_name_response = city_name_check[0]
                city_id = city_name_check[1]
                
                if new_rest['city'] != city_name_response:
                    
                    return jsonify('Error valid city has not been selected.'), 422
            
            if 'banner_url' in new_rest:
                if not check_length(new_rest['banner_url'], 1, 300):
                    return jsonify('ERROR, banner_url must be between 1 and 300 characters'), 400
            
            run_query('INSERT INTO restaurant (email, password, name, address, phoneNum, city, banner_url) VALUES (?,?,?,?,?,?,?)', [new_rest['email'], hashed_password, new_rest['name'], new_rest['address'], new_rest['phoneNum'], city_id, new_rest['banner_url']])
            
            restaurant_id = run_query('SELECT id FROM restaurant WHERE email=?', [new_rest['email']])
            response = restaurant_id[0]
            check_response = response[0]
            token = str(uuid4())
            
            run_query('INSERT INTO restaurant_session (token, restaurant_id) VALUES (?,?)', [token, check_response])

            return jsonify('Restaurant Created: restaurant_id',check_response, "token", token), 201
            
    
        else:
            return jsonify('Incorrect keys submitted'), 400
    else:
        return jsonify('Error, invalid amount of data submitted')



@app.patch('/api/restaurant')
def restaurant_patch():
            
            # TODO: allow for only select updates to the information AND check for accepted keys
            # TODO: error handling
            
    params = request.args
    data = request.json
    token = params.get('token')
    
    
    if token != None:
        token_valid = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
        token_valid_response = token_valid[0]
        response = token_valid_response[0]
        rest_id = token_valid_response[1]
        
        if response == token:
            
            allowed_keys = {"token", "address", "banner_url", "bio", "city", "email", "phoneNum", "profile_url"}
            
            if allowed_data_keys(data, allowed_keys):
                update_restaurant = new_dictionary_request(data)
            
                if 'email' in update_restaurant:
                    if not check_length(update_restaurant['email'], 1, 75):
                        return jsonify('Invalid length, email must be between 1 and 75 characters')
                    if not check_email(update_restaurant['email']):
                        return jsonify("Error, Not a valid email"), 400
                    
                    email_exists = run_query('SELECT email FROM restaurant WHERE email=?', [update_restaurant['email']])
                    if email_exists != []:
                        return jsonify('Email already exists'), 400
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.email=? WHERE restaurant_session.token=?', [update_restaurant['email'], token])
                    
                if 'address' in update_restaurant:
                    if not check_length(update_restaurant['address'], 1, 75):
                        return jsonify('Invalid length, address must be between 1 and 75 characters')
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.address=? WHERE restaurant_session.token=?', [update_restaurant['address'], token])
                
                
                if 'banner_url' in update_restaurant:
                    if not check_length(update_restaurant['banner_url'], 1, 300):
                        return jsonify('Invalid length, banner_url must be between 1 and 300 characters')
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.banner_url=? WHERE restaurant_session.token=?', [update_restaurant['banner_url'], token])
                    
                if 'bio' in update_restaurant:
                    if not check_length(update_restaurant['bio'], 1, 200):
                        return jsonify('Invalid length, phoneNum must be between 1 and 200 characters')
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.bio=? WHERE restaurant_session.token=?', [update_restaurant['bio'], token])
                        
                if 'city' in update_restaurant:
                    city_check = run_query('SELECT name, id FROM city WHERE name=?', [update_restaurant["city"]])
                    
                    
                    city_name_check = city_check[0]
                    city_name_response = city_name_check[0]
                    city_id = city_name_check[1]
                    if update_restaurant['city'] != city_name_response:
                        
                        return jsonify('Error valid city has not been selected.'), 422
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.city=? WHERE restaurant_session.token=?', [city_id, token])
                    
                    
                if 'phoneNum' in update_restaurant:
                    if not check_length(update_restaurant['phoneNum'], 1, 25):
                        return jsonify('Invalid length, phoneNum must be between 1 and 25 characters')
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.phoneNum=? WHERE restaurant_session.token=?', [update_restaurant['phoneNum'], token])
                    
                    
                if 'profile_url' in update_restaurant:
                    if not check_length(update_restaurant['profile_url'], 1, 300):
                        return jsonify('Invalid length, phoneNum must be between 1 and 300 characters')
                    run_query('UPDATE restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id SET restaurant.profile_url=? WHERE restaurant_session.token=?', [update_restaurant['profile_url'], token])
                    
                return jsonify("Restaurant information updated"), 200
            
            else:
                return jsonify("ERROR, incorrect key values submitted"), 400
        else:
            return jsonify('Invalid session token'), 400
    else:
        return jsonify("ERROR, a valid session token is needed"), 400
    
            