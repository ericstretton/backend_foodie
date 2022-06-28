import enum
from app import app
from flask import jsonify, request, Response
from helpers.data_functions import new_dictionary_request, req_menu_items
from helpers.db_helpers import  run_query, order_query

@app.get('/api/orders')
def orders_get():
    
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If order id is given show only that order
    return
    
    
@app.post('/api/orders')
def orders_post():
    # parameter for token -- get the client id from the token
    params = request.args
    token = params.get('token')
    data = request.json
    rest_id = data.get('rest_id')
    items = data.get('items')
    
    if len(data.keys()) == 2 and {'items', 'rest_id'}:
        
        if token != None:
            token_valid = run_query('SELECT token, client_id FROM client_session WHERE token=?', [token])
            
            
            token_valid_response = token_valid[0]
            client_id = token_valid_response[1]
            response = token_valid_response[0]
            
        if response == token:
            order_length = len(items)
            
            order_id = order_query('INSERT INTO orders (client_id, restaurant_id) VALUES (?,?)',[client_id, rest_id])

            
            
            if len(items) == 1:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                
            elif len(items) == 2:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                
            elif len(items) == 3:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
            elif len(items) == 4:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
            elif len(items) == 5:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
            elif len(items) == 6:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
            elif len(items) == 7:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[6], order_id])
            elif len(items) == 8:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[6], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[7], order_id])
            elif len(items) == 9:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[6], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[7], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[8], order_id])
            elif len(items) == 10:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[6], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[7], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[8], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[9], order_id])
            elif len(items) == 11:
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[0], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[1], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[2], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[3], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[4], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[5], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[6], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[7], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[8], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[9], order_id])
                run_query('INSERT INTO order_menu_item (menu_id, order_id) VALUES (?,?)', [items[10], order_id])
            
            return jsonify("Order Created"), 201
        
    else:
        return jsonify('Incorrect keys submitted'), 400
    
@app.patch('/api/orders')
def orders_patch():
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If client is using, options are cancelOrder
    # If restaurant is using, options are confirmOrder or completeOrder
    return
    