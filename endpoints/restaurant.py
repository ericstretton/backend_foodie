from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query

@app.get('/api/restaurant')
def restaurant_get():
    return
    
@app.post('/api/restaurant')
def restaurant_post():
                    # TODO STRETTON, update pw protection w salt, hash
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    address = data.get('address')
    phoneNum = data.get('phoneNum')
    bio = data.get('phoneNum')
    profile_url = data.get('profile_url')
    banner_url = data.get('banner_url')
    city = data.get('city')
    return 
    
@app.patch('/api/restaurant')
def restaurant_patch():
    return