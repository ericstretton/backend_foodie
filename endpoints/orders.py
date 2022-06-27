from app import app
from flask import jsonify
from helpers.db_helpers import run_query

@app.get('/api/orders')
def orders_get():
    
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If order id is given show only that order
    return
    
@app.post('/api/orders')
def orders_post():
    # parameter for token -- get the client id from the token
    return 
    
@app.patch('/api/orders')
def orders_patch():
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If client is using, options are cancelOrder
    # If restaurant is using, options are confirmOrder or completeOrder
    return
    