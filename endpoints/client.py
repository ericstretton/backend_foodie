from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query



@app.get('/api/client')
def client_get():
    data = request.json
    token = data.get('token')
    #TODO: Join to client_session for token
    user_info = run_query("SELECT * FROM post WHERE username=?", [token])
    resp = []
    for info in user_info:
        obj = {}
        obj[id] = info[0]
        obj[email] = info[1]
        obj[password] = info[2]
        obj[username] = info[8]
        obj[firstName] = info[3]
        obj[lastName] = info[4]
        # an_obj[created_at] = info[5]
        obj[picture_url] = info[6]
        resp.append(obj)
    
    return jsonify('Client get request successful'), 201
    
@app.post('/api/client')
def client_post():
                        # TODO STRETTON, update pw protection w salt, hash
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    # salt = bcrypt.gensalt()
    # hashed = bcrypt.hashpaw(password.encode(), salt)
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
    
    return jsonify('Client created'), 201
    
@app.patch('/api/client')
def client_patch():
    data = request.json
    token = data.get('token')
    return
    
@app.delete('/api/client')
def client_delete():
    return