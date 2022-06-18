from app import app
from flask import jsonify
from helpers.db_helpers import run_query

@app.get('/api/orders')
def orders_get():
    return
    
@app.post('/api/orders')
def orders_post():
    return 
    
@app.patch('/api/orders')
def orders_patch():
    return
    