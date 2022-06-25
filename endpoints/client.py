
from app import app
from flask import jsonify, request, Response
from helpers.data_functions import allowed_data_keys, check_length, client_dictionary_query, check_email, new_dictionary_request, update_client_dictionary
from helpers.db_helpers import run_query
import bcrypt
from uuid import uuid4


@app.get('/api/client')
def client_get():
    # Only applicable to single user id with an equivalent accessible token
    params = request.args
    token = params.get('token')
    if not token:
        return jsonify('Missing required argument: token', 'You must be logged in to access client information' ),422
    check_token = run_query('SELECT client_session.token FROM client_session INNER JOIN client ON client.id=client_session.client_id WHERE client_session.token=?', [token])
    check = check_token[0]
    if check[0] == token:
        user_info = run_query('SELECT client_session.client_id, client.email, client.username, client.created_at, client.firstName, client.lastName, client.picture_url  FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
        resp = client_dictionary_query(user_info[0])
        resp_list = []
        resp_list.append(resp)
        return jsonify(resp)
    else:
        return Response('Error token does not exist', status=400)
    
@app.post('/api/client')
def client_post():
                        # TODO STRETTON, update pw protection w salt, hash
    data = request.json
    
    if len(data.keys()) >= 4 and len(data.keys()) <= 6:
        if {'email', 'username', 'password', 'firstName'} or \
            {'email', 'username', 'password', 'firstName', 'lastName'} or \
                {'email', 'username', 'password', 'firstName', 'picture_url'} or \
                    {'email', 'username', 'password', 'firstName', 'lastName', 'picture_url'}:
            new_client = new_dictionary_request(data)
        else:
            return jsonify('Incorrect keys submitted'), 400
    else:
        return jsonify('Error, invalid amount of data submitted')
    
    if not check_email(new_client['email']):
        return jsonify("Error invalid email address submitted"), 400
    if not check_length(new_client['email'], 5, 75):
        return jsonify('ERROR, email must be between 5 and 75 characters'), 400
    
    check_email_validity = run_query('SELECT email FROM client WHERE email=?', [new_client['email']])
    
    if check_email_validity == []:
        if not check_length(new_client['username'], 1, 50):
            return jsonify('ERROR, username must be between 1 and 50 characters'), 400
        check_username_validity = run_query('SELECT username FROM client WHERE username=?', [new_client['username']])
        
        if check_username_validity == []:
            
            if not check_length(new_client['password'], 6, 100):
                return jsonify('ERROR, password must be between 6 and 200 characters'), 400
            password = str(new_client['password'])
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)

            if not new_client['firstName']:
                return jsonify('Missing required argument: firstName'), 422
            else:
                run_query("INSERT INTO client (email, username, password, firstName, lastName, picture_url) VALUE(?,?,?,?,?,?)", [new_client['email'], new_client['username'], hashed_password, new_client['firstName'], new_client['lastName'], new_client['picture_url']])
        else:
            username_validity = check_username_validity[0]
            if username_validity[0] == new_client['username']:
                return jsonify('ERROR, username already exists'), 400
    else:
        email_validity = check_email_validity[0]

        if email_validity[0] == new_client['email']:
            return jsonify('ERROR, email already exists'), 400
    
    client_id = run_query('SELECT id FROM client WHERE email=?', [new_client['email']])
    response = client_id[0]
    check_response = response[0]
    
    token = str(uuid4())
        # TODO, add checks on lastName and picture_url
    run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, check_response])    
    
    client = run_query('SELECT id, email, username, firstName, lastName, picture_url, created_at FROM client WHERE id=?', [check_response])
    client_response = client[0]
    
    resp = client_dictionary_query(client_response)
    resp['token'] = token
    
    return jsonify('Client Created,', resp), 201
    
    
    
@app.patch('/api/client')
def client_patch():
                    # TODO: get token from client_session table for authentication
    data = request.json
    token = data.get('token')
    
    if token != None:
        token_valid = run_query('SELECT token FROM client_session WHERE token=?', [token])
        token_valid_response = token_valid[0]
        response = token_valid_response[0]
        
        
        if response == token:
            allowed_keys= {"token", "email", "username", "firstName", "lastName", "picture_url"}
            
            allowed_data_keys(data, allowed_keys)
            
            update_client =  new_dictionary_request(data)
            
            if 'email' in update_client:
                if not check_length(update_client['email'], 1, 75):
                    return jsonify('Invalid length, email must be between 1 and 75 characters')
                if not check_email(update_client['email']):
                    return jsonify("Error, Not a valid email"), 400
                
                email_exists = run_query('SELECT email FROM client WHERE email=?', [update_client['email']])
                if email_exists != []:
                    return jsonify('Email already exists'), 400
                run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.email=? WHERE client_session.token=?', [update_client['email'], token])
                
            if 'username' in update_client:
                if not check_length(update_client['username'], 1, 50):
                    return Response('Invalid length, username must be between 1 and 50 characters')
                
                username_exists = run_query('SELECT EXISTS(SELECT username FROM client WHERE username=?', [update_client['username']])
                if username_exists == 1:
                    return jsonify('Username already Exists')
                run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [update_client['username'], token])
                
            if 'firstName' in update_client:
                if not check_length(update_client['firstName'], 1, 50):
                    return Response('Invalid length, firstName must be between 1 and 50 characters')
                run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.firstName=? WHERE client_session.token=?', [update_client['firstName'], token])
                
            if 'lastName' in update_client:
                if not check_length(update_client['lastName'], 1, 50):
                     return Response('Invalid length, lastName must be between 1 and 50 characters')
                run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.lastName=? WHERE client_session.token=?', [update_client['lastName'], token])
                
            if 'picture_url' in update_client:
                if not check_length(update_client['picture_url'], 1, 300):
                     return Response('Invalid length, picture_url must be between 1 and 300 characters')
                run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.picture_url=? WHERE client_session.token=?', [update_client['picture_url'], token])
            
            # GET THE UPDATED client information
            client_updated = run_query('SELECT c.id, email, username, fistName, lastName, picture_url, created_at FROM client AS c INNER JOIN client_session AS s ON c.id=s.client_id WHERE client_session.token=?', [token])
            
            resp = update_client_dictionary(client_updated)
            
            return jsonify(resp)
        else:
            return Response('Invalid session token', status=400)
    else:
        return Response('A valid session token is needed')
    
    
@app.delete('/api/client')
def client_delete():
                        # TODO: get token from client_session table for authentication
    data = request.json
    
    
    if len(data.keys()) == 2:
        if {"token", "password"} <= data.keys():
            token = data.get('token')
            password = data.get('password')
        
            if token != None:
                token_valid = run_query('SELECT token FROM client_session WHERE token=?', [token])
                response = token_valid[0]
                if response[0] == token:
                    
                    comparison = run_query('SELECT client_session.token, client.password, client.id FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
                    comp_response = comparison[0]
                    
                    if password == comp_response[1]:
                        run_query('DELETE FROM client_session WHERE token=?', [comp_response[0]])
                        
                        run_query('DELETE FROM client WHERE id=?', [comp_response[2]])
                        return jsonify('Delete Processed' ), 204
                    else:
                        return jsonify('Required Credentials do not match, delete not processed'), 400
                else:
                    return jsonify("Invalid Token was passed", token)
            else:
                return jsonify('Error, no token present')
        else:
            return jsonify('ERROR, Invalid JSON data, check required keys'), 400
    else:
        return jsonify('ERROR, invalid amount of keys, check required keys'), 400