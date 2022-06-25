import json
from app import app
from flask import jsonify, request
from helpers.data_functions import check_length, menu_item_dictionary, new_dictionary_request
from helpers.db_helpers import run_query

@app.get('/api/menu_item')
def menu_item_get():
                # OPTIONAL arguments are restaurant_id and menuId
    
    params = request.args
    
    if len(params.keys()) == 0:
        all_items = run_query('SELECT * FROM menu_item')
        all_menu_items = []
        for item in all_items:
            menu_item = menu_item_dictionary(item)
            all_menu_items.append(menu_item)
        return jsonify(all_menu_items)
@app.post('/api/menu_item')
def menu_item_post():
    
    # TODO: include description and image_url as optional keys
    data = request.json
    token = data.get('token')
    
    if token != None: 
        
        check_token = run_query('SELECT token FROM restaurant_session WHERE token=?', [token])
        token_validity = check_token[0]
        response = token_validity[0]
        
        if response == token:
            restaurant_id = run_query('SELECT restaurant.id FROM restaurant INNER JOIN restaurant_session ON restaurant.id=restaurant_session.restaurant_id WHERE token=?', [response])
            new_menu_item = new_dictionary_request(data)
            resp_restaurant_id = restaurant_id[0]
            id_response = resp_restaurant_id[0]

            if 'name' in new_menu_item:
                if not check_length(new_menu_item['name'], 1, 50):
                    return jsonify('Invalid length, item name must be between 1 and 50 characters')
            if not new_menu_item['price']:
                return jsonify('ERROR, required field not listed: Price')

            run_query('INSERT INTO menu_item (restaurant_id, name, price) VALUES (?,?,?) ', [id_response, new_menu_item['name'], new_menu_item['price']])
            
            item_data = run_query('SELECT menu_item.id, menu_item.restaurant_id, restaurant.id, menu_item.name, menu_item.price FROM menu_item INNER JOIN restaurant ON menu_item.restaurant_id=restaurant.id WHERE menu_item.restaurant_id=?', [response] )
            item = item_data[0]
            
            
            resp = {
                "item_id" : item[0],
                "restaurant_id" : item[2],
                "name" : item[3],
                "price" : item[4]
            }
            return jsonify("Item Created: ", resp)
        else:
            return jsonify('ERROR token submitted is invalid', token), 422
    else:
        return jsonify('ERROR, valid log in token is required to create menu items')
@app.patch('/api/menu_item')
def menu_item_patch():
    return
    
@app.delete('/api/menu_item')
def menu_item_delete():
    return
