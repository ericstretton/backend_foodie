import json
from app import app
from flask import jsonify, request, Response
from helpers.data_functions import allowed_data_keys, check_length, client_dictionary_query, check_email
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
    email = data.get('email')
    username = data.get('username')
    password = data.get(str('password'))
    
    
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode(), salt)
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    picture_url = data.get('picture_url')
    if not email:
        return jsonify('Missing required argument: email'), 422
    if not username:
        return jsonify('Missing required argument: username'), 422
    if not password:
        return jsonify('Missing required argument: password'), 422
    if not firstName:
        return jsonify('Missing required argument: firstName'), 422
    
    run_query("INSERT INTO client (email, username, password, firstName, lastName, picture_url) VALUE(?,?,?,?,?,?)", [email, username, password, firstName, lastName, picture_url])
    token = str(uuid4())
    resp = []
    client_info = run_query('SELECT id FROM client WHERE username=? and password=?', [username, password])
    for info in client_info:
        clientId = {}
        clientId = info[0]
        resp.append(clientId)
    run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, clientId])
    
    return jsonify('Client created', 'client_id: ', clientId, 'token: ', token), 201
    
@app.patch('/api/client')
def client_patch():
                    # TODO: get token from client_session table for authentication
    data = request.json
    token = data.get('token')
    if token != None:
        # token_valid = run_query('SELECT EXISTS(SELECT token FROM client_session WHERE token=?)', [token])
        # token_valid_response = token_valid[0]
        # if str(token_valid_response[0]) == 1:
            # allowed_keys= {"email", "username", "token", "firstName", "lastName", "picture_url"}
            # allowed_data_keys(data, allowed_keys)
            update_client =  client_dictionary_query(data)
            if 'email' in update_client:
                if not check_length(update_client['email'], 1, 75):
                    return jsonify('Invalid length, email must be between 1 and 75 characters')
                if not check_email(update_client['email']):
                    return jsonify("Error, Not a valid email"), 400
                
                email_exists = run_query('SELECT EXISTS(SELECT email FROM client WHERE email=?)', [update_client['email']])
                if email_exists == 1:
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
            client_updated = run_query('SELECT c.id, email, username, fistName, lastName, picture_url, created_at FROM client c INNER JOIN client_session s ON c.id=s.client_id WHERE client_session.token=?', [token])
            resp = client_dictionary_query(client_updated)
            return Response(json.dumps(resp, mimetype="application/json", status=200))
        # else:
        #     return Response('Invalid session token', status=400)
    else:
        return Response('A valid session token is needed')
    
    
@app.delete('/api/client')
def client_delete():
                        # TODO: get token from client_session table for authentication
    data = request.json
    token = data.get('token')
    password = data.get('password')
    
    if token != None:
        token_valid = run_query('SELECT EXISTS(SELECT token FROM client_session WHERE token=?)', [token])
        if token_valid ==1:
            
            comparison = run_query('SELECT client_session.token, client.password, client.id FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
            
            if password == comparison[1]:
                run_query('DELETE * FROM client WHERE id=?', [comparison[2]])
                return jsonify('Delete Processed'), 204
            else:
                return jsonify('Required Credentials do not match, delete not processed'), 400
        else:
            return jsonify("Invalid Token was passed", token)
    else:
        return jsonify('Error, no token present')
    