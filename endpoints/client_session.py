from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query
from uuid import uuid4



@app.post('/api/client_session')
def client_login_post():
    
    # Gather Required information =>
        # TODO - deal with encrypted password
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify('Missing required argument: username'), 422
    if not password:
        return jsonify('Missing required argument: password'), 422
    
    
    resp = []
    client_info = run_query('SELECT id FROM client WHERE username=? and password=?', [username, password])
    for info in client_info:
        clientId = {}
        clientId = info[0]
        resp.append(clientId)
    if clientId == None:
        return jsonify('Log-in Error, client Id not present', clientId), 422
    else:
        token = str(uuid4())
        #TODO: change to insert
        run_query('INSERT INTO client_session (client_id, token) VALUES (?,?)', [clientId, token])
        if True:
            return jsonify('Log-in Successful', 'clientId: ', clientId, 'token: ', token), 201
        
    
@app.delete('/api/client_session')
def client_login_delete():
    data = request.json
    token = data.get('token')
    return
    