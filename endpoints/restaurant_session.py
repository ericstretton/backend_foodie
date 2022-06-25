import json
from app import app
from flask import jsonify, request, Response
from helpers.db_helpers import run_query
from uuid import uuid4


@app.post('/api/restaurant_session')
def restaurant_login_post():
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify('Missing required argument: email'), 422
    
    if not password:
        return jsonify('Missing required argument: password'), 422
    
    
    resp = []
    restaurant_info = run_query('SELECT id FROM restaurant WHERE email=? and password=?', [email, password])
    for info in restaurant_info:
        restaurantId = {}
        restaurantId = info[0]
        resp.append(restaurantId)
    if restaurantId == None:
        return jsonify('Log-in Error, restaurant Id not present', restaurantId), 422
    else:
        token = str(uuid4())
        #TODO: change to insert
        run_query('INSERT INTO restaurant_session (restaurant_id, token) VALUES (?,?)', [restaurantId, token])
        if True:
            return jsonify('Log-in Successful', 'restaurantId: ', restaurantId, 'token: ', token), 201 
    
@app.delete('/api/restaurant_session')
def restaurant_login_delete():
    data = request.json
    
    token = data.get('token')
    check_token = run_query('SELECT token from restaurant_session WHERE token=?', [token])
    response = check_token[0]
    if response[0] == token:
        run_query('DELETE FROM restaurant_session WHERE token=?', [token])
    else:
        return jsonify("ERROR, conditions to log out are not met, check token")
    return jsonify("Log-out Successful")