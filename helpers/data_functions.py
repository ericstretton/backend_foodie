import re
# The first 4 data helper functions are for the variance in accepted keys on a client post request
#Scenario #1
def client_dictionary_query(data):
    client = {
        "client_id" : data[0],
        "created_at" : data[1],
        "email" : data[2],
        "username" : data[3],
        "firstName" : data[4],
        "lastName" : data[5],
        "picture_url" : data[6]
        
    }
    return client
#Scenario #2
def client_dictionary_query_min(data):
    client = {
        "client_id" : data[0],
        "created_at" : data[1],
        "email" : data[2],
        "username" : data[3],
        "firstName" : data[4]
        
    }
    return client
#Scenario #3
def client_dictionary_query_lastName(data):
    client = {
        "client_id" : data[0],
        "created_at" : data[1],
        "email" : data[2],
        "username" : data[3],
        "firstName" : data[4],
        "lastName" : data[5]
        
    }
    return client
#Scenario #4
def client_dictionary_query_pictureURL(data):
    client = {
        "client_id" : data[0],
        "created_at" : data[1],
        "email" : data[2],
        "username" : data[3],
        "firstName" : data[4],
        "picture_url" : data[5]
        
    }
    return client

# helper function to update client information

def update_client_dictionary(data):
    client = {
        
        "email" : data[1],
        "username" : data[2],
        "password" : data[3],
        "firstName" : data[4],
        "lastName" : data[5],
        "picture_url" : data[6]
    }
    return client

#restaurant function for post, where a password is necessary

def restaurant_dictionary_query(data):
    restaurant = {
        "restaurant_id" : data[0],
        "email" : data[1],
        "password" : data[2],
        "name" : data[3],
        "address" : data[4],
        "phoneNum" : data[5],
        "city" : data[6],
        "bio" : data[7],
        "profile_url" : data[8],
        "banner_url" : data[9]
        
    }
    return restaurant

#restaurant function for get requests, no password key value present

def restaurant_get_dict(data):
    restaurant = {
        "restaurant_id" : data[0],
        "address" : data[1],
        "banner_url" : data[2],
        "name" : data[3],
        "city" : data[4],
        "email" : data[5],
        "phoneNum" : data[6],
        "bio" : data[7],
        "profile_url" : data[8]
        
        
    }
    return restaurant

# TODO add functions for orders 
def order_dictionary_query(data):
    order = {
        "order_id" : data[0],
        "created_at" : data[1],
        "is_confirmed" : data[2],
        "is_complete" : data[3],
        "is_cancelled" : data[4],
        "client_id" : data[5],
        "restaurant_id" : data[6]
    }
    return order

#Helper function for creating menu_items
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

#Helper function, regex email - qualifies submitted emails 
def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if(re.search(regex, email)):
        return True
    else:
        return False
    
#Helper function that checks lengths based on various needs of the database
def check_length(input, min_len, max_len):
    if len(input) >= min_len and len(input) <= max_len:
        return True
    else:
        return False

#Helper function to qualify what key values are currently accepted for an endpoint (checks json request)
def allowed_data_keys(data, allowed_keys):
    
    for key in list(data.keys()):
        if key not in allowed_keys:
            del data[key]
    return data

#Helper function that removes leading and trailing whitespaces - created fro json reqest data
def new_dictionary_request(data):
    new_dict = {}
    for k,v in data.items():
        new_dict[k] = str(v).strip()
    return new_dict

def req_menu_items(data):
    menu_items_list ={
        "menu_id" : data
    }
    return menu_items_list