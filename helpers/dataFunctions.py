def client_dictionary_query(data):
    client = {
        "client_id" : data[0],
        "email" : data[1],
        "username" : data[2],
        "firstName" : data[3],
        "lastName" : data[4],
        "profile_url" : data[5],
        "created_at" : data[6]
    }
    return client

def restaurant_dictionary_query(data):
    restaurant = {
        "restaurant_id" : data[0],
        "name" : data[1],
        "city" : data[2],
        "address" : data[3],
        "email" : data[4],
        "phoneNum" : data[5],
        "bio" : data[6],
        "profile_url" : data[7]
    }
    return restaurant