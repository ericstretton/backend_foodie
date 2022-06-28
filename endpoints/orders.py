
from app import app
from flask import jsonify, request
from helpers.data_functions import  order_dictionary_query
from helpers.db_helpers import  run_query, order_query

@app.get('/api/orders')
def orders_get():
    
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If order id is given show only that order
    
    params = request.args
    
    if len(params.keys()) >= 1 and len(params.keys()) <= 2:
    
        if len(params.keys()) == 1:
            token = params.get('token')
            
            client_validity = run_query('SELECT token, client_id FROM client_session WHERE token=?', [token])
            
            restaurant_validity = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
            
            if client_validity != []:
                client_validity_response = client_validity[0]
                if client_validity_response[0] == token:
                    client_id = client_validity_response[1]
                    
                    all_user_orders = run_query('SELECT * FROM orders WHERE client_id=?', [client_id])
                    
                    all_orders = []
                    for item in all_user_orders:
                        order = order_dictionary_query(item)
                        all_orders.append(order)
                    return jsonify(all_orders)
            
            if restaurant_validity != []:
                restaurant_validity_response = restaurant_validity[0]
                if restaurant_validity_response[0] == token:
                    restaurant_id = restaurant_validity_response[1]
                    
                    all_rest_orders = run_query('SELECT * FROM orders WHERE restaurant_id=?', [restaurant_id])
                    
                    all_orders = []
                    for item in all_rest_orders:
                        order = order_dictionary_query(item)
                        all_orders.append(order)
                    return jsonify(all_orders)
                
        if len(params.keys()) == 2:
            
            token = params.get('token')
            order_id = params.get('order_id')
            
            client_validity = run_query('SELECT token, client_id FROM client_session WHERE token=?', [token])
            
            restaurant_validity = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
            
            if client_validity != []:
                client_validity_response = client_validity[0]
                if client_validity_response[0] == token:
                    client_id = client_validity_response[1]

                    specific_order = run_query('SELECT * FROM orders WHERE client_id=? AND id=?', [client_id, order_id])
                    
                    order_info = []
                    for item in specific_order:
                        order = order_dictionary_query(item)
                        order_info.append(order)
                    return jsonify(order_info)
                    
                    
            if restaurant_validity != []:
                restaurant_validity_response = restaurant_validity[0]
                if restaurant_validity_response[0] == token:
                    
                    restaurant_id = restaurant_validity_response[1]
                    specific_order = run_query('SELECT * FROM orders WHERE restaurant_id=? AND id=?', [restaurant_id, order_id])
                    
                    order_info = []
                    for item in specific_order:
                        order = order_dictionary_query(item)
                        order_info.append(order)
                    return jsonify(order_info)
                
        else:
            return jsonify('Incorrect keys submitted'), 400
    else:
        return jsonify('Error, invalid amount of data submitted'), 400
    
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
                return jsonify('ERROR, submitted token is not a valid client_session token'), 401
        else:
            return jsonify('ERROR, a client_session token is required to request an order'), 401
        
    else:
        return jsonify('Incorrect keys submitted'), 422
    
@app.patch('/api/orders')
def orders_patch():
    # WHAT is needed for request - has to be seen for either restaurant or client
    # parameter for token -- get the restaurant or client id from the token
    # If client is using, options are cancelOrder
    # If restaurant is using, options are confirmOrder or completeOrder
    
    params = request.args
    data = request.json
    if len(params.keys()) == 2:
        token = params.get('token')
            
        client_validity = run_query('SELECT token, client_id FROM client_session WHERE token=?', [token])
        
        restaurant_validity = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
        
        if client_validity != []:
            client_validity_response = client_validity[0]
            if client_validity_response[0] == token:
                client_id = client_validity_response[1]
                order_id = params.get('order_id')
                order_id_int = int(order_id)
                
                order_verification = run_query('SELECT id FROM orders WHERE client_id=? AND id=?', [client_id, order_id_int])
                
                order_verification_response = order_verification[0]
                
                if order_verification_response[0] == order_id_int:
                    is_cancelled = data.get('is_cancelled')
                    if is_cancelled == "True":
                        cancel_order = 1
                        run_query('UPDATE orders SET is_cancelled=? WHERE order_id=?', [cancel_order, order_id])
                        return jsonify('Order Cancelled')
                    
        if restaurant_validity != []:
            restaurant_validity_response = restaurant_validity[0]
            if restaurant_validity_response[0] == token:
                rest_id = restaurant_validity_response[1]
                order_id = params.get('order_id')
                order_id_int = int(order_id)
                
                order_verification = run_query('SELECT id FROM orders WHERE restaurant_id=? AND id=?', [rest_id, order_id_int])
                order_verification_response = order_verification[0]
                if order_verification_response[0] == order_id_int:
                    is_confirmed = data.get('is_confirmed')
                    
                    if is_confirmed != None:
                        if is_confirmed == "True":
                            confirm_order = 1
                            
                            run_query('UPDATE orders SET is_confirmed=? WHERE id=?', [confirm_order, order_id_int])
                            return jsonify('Order Confirmed')
                    
                    is_complete = data.get('is_complete')
                    
                    if is_complete != None:
                        if is_complete == "True":
                            is_confirmed = 0
                            complete_order = 1
                            run_query('UPDATE orders SET is_confirmed=? WHERE id=?', [is_confirmed, order_id_int])
                            run_query('UPDATE orders SET is_complete=? WHERE id=?', [complete_order, order_id_int])
                            return jsonify('Order has been completed')
                    
    else:
        return jsonify('ERROR')
    