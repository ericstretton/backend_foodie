
import bcrypt
from app import app
from flask import jsonify, request
from helpers.data_functions import check_email
from helpers.db_helpers import run_query
from uuid import uuid4



@app.post('/api/client_session')
def client_login_post():
    
    # Gather Required information =>
        # TODO - deal with encrypted password
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    
    if not check_email(email):
        return jsonify('Information provided is not a valid Email'), 422
    valid_email = run_query('SELECT EXISTS(SELECT email FROM client WHERE email=?', [email])
    if valid_email == 1:
        db_password = run_query('SELECT password FROM client WHERE email=?', [email])
        if bcrypt.checkpw(str(password).encode(), str(db_password).encode()):
            client = 123
    if not password:
        return jsonify('Missing required argument: password'), 422
    
    
    resp = []
    client_info = run_query('SELECT id FROM client WHERE username=? and password=?', [email, password])
    for info in client_info:
        clientId = {}
        clientId = info[0]
        resp.append(clientId)
    if clientId == None:
        return jsonify('Log-in Error, client Id not present', clientId), 422
    else:
        token = str(uuid4())
        #TODO: 
        run_query('INSERT INTO client_session (client_id, token) VALUES (?,?)', [clientId, token])
        if True:
            return jsonify('Log-in Successful', 'clientId: ', clientId, 'token: ', token), 201
        
    
@app.delete('/api/client_session')
def client_login_delete():
    data = request.json
    token = data.get('token')
    check_token = run_query('SELECT token from client_session WHERE token =?', [token])
    response = check_token[0]
    if response[0] == token:
        run_query('DELETE FROM client_session WHERE token=?', [token])
    else:
        return jsonify("Error, conditions to log-out are not met, check token")
    return jsonify('Log-out Successful')
    