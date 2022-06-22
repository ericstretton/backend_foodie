
from app import app
from flask import jsonify, request
from helpers.dataFunctions import client_dictionary_query, check_email
from helpers.db_helpers import run_query
import bcrypt
from uuid import uuid4



@app.get('/api/client')
def client_get():
    #TODO: Get Token as a variable 
    data = request.data
    token = data.get('token')
    user_info = run_query('SELECT client_session.client_id, client.email, client.username, client.created_at, client.firstName, client.lastName, client.picture_url  FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
    resp = client_dictionary_query(user_info)
    resp_list = []
    resp_list.append(resp)
    
    return jsonify('Client get request successful', resp_list), 201
    
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
        token_valid = run_query('SELECT EXISTS(SELECT token FROM client_session WHERE token=?)', [token])
        if token_valid == 1:
            update_client =  client_dictionary_query(data)
            if "email" in update_client:
                if not check_email(update_client['email']):
                    return jsonify("Error, Not a valid email"), 400
                email_exists = run_query('SELECT EXISTS(SELECT email FROM client WHERE email=?)', [update_client['email']])
                if email_exists == 1:
                    return jsonify('Email already exists'), 400
                
    return
    
@app.delete('/api/client')
def client_delete():
                        # TODO: get token from client_session table for authentication
    data = request.json
    token = data.get('token')
    password = data.get('password')
    
    if token != None:
        token_valid = run_query('SELECT EXISTS(SELECT token FROM cllient_session WHERE token=?', [token])
        if token_valid ==1:
            comparison =  run_query('SELECT client_session.token, client.password, client.id FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
            if password == comparison[1]:
                run_query('DELETE FROM client WHERE id=?', [comparison[2]])
                return jsonify('Delete Processed'), 204
            else:
                return jsonify('Required Credentials do not match, delete not processed'), 400
        
    return