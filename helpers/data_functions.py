import re

def client_dictionary_query(data):
    client = {
        "client_id" : data[0],
        "email" : data[1],
        "username" : data[2],
        "firstName" : data[4],
        "lastName" : data[5],
        "picture_url" : data[6],
        "created_at" : data[3]
    }
    return client

def update_client_dictionary(data):
    client = {
        
        "email" : data[1],
        "username" : data[2],
        "firstName" : data[3],
        "lastName" : data[4],
        "picture_url" : data[5]
    }
    return client

def restaurant_dictionary_query(data):
    restaurant = {
        "restaurant_id" : data[0],
        "address" : data[1],
        "banner_url" : data[2],
        "bio" : data[3],
        "city" : data[4],
        "email" : data[5],
        "phoneNum" : data[6],
        "profile_url" : data[7]
        
    }
    return restaurant

# TODO add functions for menu items, orders and log in authorization


def menu_item_dictionary(data):
    menu_item = {
        "id" : data[0],
        "name" : data[1],
        "description" : data[2],
        "price" : data[3],
        "image_url" : data[4],
        "restaurant_id" : data[5]
    }
    return menu_item

def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if(re.search(regex, email)):
        return True
    else:
        return False
    
def check_length(input, min_len, max_len):
    if len(input) >= min_len and len(input) <= max_len:
        return True
    else:
        return False
    
def allowed_data_keys(data, allowed_keys):
    
    for key in list(data.keys()):
        if key not in allowed_data_keys:
            del data[key]
    return data

def new_dictionary_request(data):
    new_dict = {}
    for k,v in data.items():
        new_dict[k] = str(v).strip()
    return new_dict