from app import app
from flask import jsonify, request
from helpers.db_helpers import run_query

@app.get('/api/client_session')
def client_login_post():
    return 
    
@app.delete('/api/client_session')
def client_login_delete():
    return
    