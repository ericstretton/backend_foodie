from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query
import bcrypt
from uuid import uuid4


@app.get('/api/client')
def client_get():
    #TODO: Get Token as a variable 
    
    token = str("086741bd-3ccc-4dc4-b79a-cbda9dc077bb")
    user_info = run_query('SELECT client_session.client_id, client.email, client.username, client.created_at, client.firstName, client.lastName, client.picture_url  FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
    resp = []
    for info in user_info:
        obj = {}
        obj['id'] = info[0]
        obj['username'] = info[2]
        obj['email'] = info[1]
        obj['lastName'] = info[4]
        obj['created_at'] = info[3]
        obj['lastName'] = info[5]
        obj['picture_url'] = info[6]
        resp.append(obj)
    
    return jsonify('Client get request successful', resp), 201
    
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
    return
    
@app.delete('/api/client')
def client_delete():
                        # TODO: get token from client_session table for authentication
    return