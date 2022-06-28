
from app import app
from flask import jsonify, request
from helpers.data_functions import check_length, menu_item_dictionary, new_dictionary_request
from helpers.db_helpers import run_query

@app.get('/api/menu_item')
def menu_item_get():
                # TODO: apply checks for if menu_id exists within the restaurant
    
    params = request.args
    
    if len(params.keys()) == 0:
        all_items = run_query('SELECT * FROM menu_item')
        all_menu_items = []
        for item in all_items:
            menu_item = menu_item_dictionary(item)
            all_menu_items.append(menu_item)
        return jsonify(all_menu_items)
    
    elif len(params.keys()) == 1:
        rest_id = params.get('restaurant_id')
        all_rest_items = run_query('SELECT * FROM menu_item WHERE restaurant_id=?', [rest_id])
        all_rest_menu_items = []
        for item in all_rest_items:
            menu_item = menu_item_dictionary(item)
            all_rest_menu_items.append(menu_item)
        return jsonify(all_rest_menu_items)
    
    elif len(params.keys()) == 2:
        rest_id = params.get('restaurant_id')
        menu_id = params.get('menu_id')
        rest_menu_item = run_query('SELECT * FROM menu_item WHERE restaurant_id=? and id=?', [rest_id, menu_id])
        menu_object = []
        for item in rest_menu_item:
            menu_item = menu_item_dictionary(item)
            menu_object.append(menu_item)
        return jsonify(menu_object)
    
    else:
        return jsonify('ERROR, invalid number of paramaters entered')
    
@app.post('/api/menu_item')
def menu_item_post():
    
    # TODO: adjust to similar format as client_post
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
            
            item_data = run_query('SELECT menu_item.id, menu_item.restaurant_id, restaurant.id, menu_item.name, menu_item.price FROM menu_item INNER JOIN restaurant ON menu_item.restaurant_id=restaurant.id WHERE menu_item.restaurant_id=?', [id_response])
            
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
    # MUST HAVE a token and a menu_id to reference - check the token with the menu_id that it matches
    params = request.args
    data = request.json
    token = params.get('token')
    menu_id = params.get('menu_id')
    menu_id_int = int(menu_id)
    
    if token != None:
        check_token = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
        token_validity = check_token[0]
        response = token_validity[0]
        rest_id = token_validity[1]
        
        if response == token:
            
            id_check = run_query('SELECT id FROM menu_item WHERE restaurant_id=? AND id=?', [rest_id, menu_id_int])
            id_check_validity = id_check[0]
            response = id_check_validity[0]
            
            if response == menu_id_int:
                
                # TODO: add allowed keys
                update_item = new_dictionary_request(data)
                
                if 'name' in update_item:
                    if not check_length(update_item['name'], 1, 50):
                        return jsonify('Invalid length, name must be between 1 and 50 characters')
                    item_name_exists = run_query('SELECT name FROM menu_item WHERE id=?', [menu_id_int])
                    
                    if item_name_exists != []:
                        item_name_exists_resp = item_name_exists[0]
                        response = item_name_exists_resp[0]
                        if response == update_item['name']:
                            return jsonify('The submitted item name already exists in your menu')
                    run_query('UPDATE menu_item SET name=? WHERE id=?', [update_item['name'], menu_id_int])
                
                if 'description' in update_item:
                    if not check_length(update_item['description'], 1, 150):
                        return jsonify('Invalid length, description must be between 1 and 150 characters')
                    run_query('UPDATE menu_item SET description=? WHERE id=?', [update_item['description'], menu_id_int])
                
                if 'price' in update_item:
                    #TODO check for if the submission is a positive number and a integer
                    run_query('UPDATE menu_item SET price=? WHERE id=?', [update_item['price'], menu_id_int])
                
                if 'image_url' in update_item:
                    #TODO check for if the submission is a url
                    if not check_length(update_item['image_url'], 1, 300):
                        return jsonify('Invalid length, image_url must be between 1 and 300 characters')
                
                # return the response for the updated menu information along with the below success code
                
                return jsonify("menu_item updated"), 200
            else:
                return jsonify("ERROR, menu item needs to be specified, check menu_id")
        else:
            return jsonify('ERROR session token does not match the required restaurant')
    
    else:
        return jsonify('ERROR, restaurant session token is required to update menu items')
    
@app.delete('/api/menu_item')
def menu_item_delete():
    # MUST HAVE a token and a menu_id to reference - check the token with the menu_id that it matches
    params = request.args
    token = params.get('token')
    menu_id = params.get('menu_id')
    menu_id_int = int(menu_id)
    
    
    if token != None:
        check_token = run_query('SELECT token, restaurant_id FROM restaurant_session WHERE token=?', [token])
        token_validity = check_token[0]
        response = token_validity[0]
        
        
        if response == token:
            run_query('DELETE FROM menu_item WHERE id=?', [menu_id_int])
            return jsonify('Success item was deleted ')
        else:
            return jsonify('ERROR session token does not match the required restaurant')    
            
    else:
        return jsonify('ERROR, restaurant session token is required to delete menu items')
    
