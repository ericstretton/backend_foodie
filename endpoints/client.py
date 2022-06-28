
from app import app
from flask import jsonify, request, Response
from helpers.data_functions import allowed_data_keys, check_length, client_dictionary_query, check_email, new_dictionary_request, client_dictionary_query_min,  client_dictionary_query_pictureURL
from helpers.db_helpers import run_query
import bcrypt
from uuid import uuid4


@app.get('/api/client')
def client_get():
    # Only applicable to single user id with an equivalent accessible token
    
    
    params = request.args
    token = params.get('token')
    if not token:
        return jsonify('Missing required argument: token', 'You must be logged in to access client information' ),422
    check_token = run_query('SELECT client_session.token FROM client_session INNER JOIN client ON client.id=client_session.client_id WHERE client_session.token=?', [token])
    check = check_token[0]
    
    #Check submitted token with stored user_information to qualify login
    if check[0] == token:
        user_info = run_query('SELECT client_session.client_id, client.email, client.username, client.created_at, client.firstName, client.lastName, client.picture_url  FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
        resp = client_dictionary_query(user_info[0])
        resp_list = []
        resp_list.append(resp)
        return jsonify(resp)
    else:
        return jsonify('Error token does not exist'), 400
    
@app.post('/api/client')
def client_post():
                        
    data = request.json
    # Keys Required, email, username, password, firstName
    if len(data.keys()) >= 4 and len(data.keys()) <= 6:
        if {'email', 'username', 'password', 'firstName'} == data.keys():
            new_client = new_dictionary_request(data)

            if 'email' in new_client:
                
                    #Apply checks on email to qualify if able to post
                    if not check_email(new_client['email']):
                        return jsonify("Error invalid email address submitted"), 400
                    if not check_length(new_client['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400
                
                    check_email_validity = run_query('SELECT email FROM client WHERE email=?', [new_client['email']])
                    
                    
                    if check_email_validity != []:
                        
                        email_validity = check_email_validity[0]
                        if email_validity[0] == new_client['email']:
                            return jsonify('ERROR, email already exists'), 400
                        
            #Apply checks on username to qualify if able to post    
            if 'username' in new_client:
                
                if not check_length(new_client['username'], 1, 50):
                    return jsonify('ERROR, username must be between 1 and 50 characters'), 400
                
                check_username_validity = run_query('SELECT username FROM client WHERE username=?', [new_client['username']])
                
                if check_username_validity != []:
                    username_validity = check_username_validity[0]
                    response = username_validity[0]
                    if response == new_client['username']:
                        return jsonify('username already exists', 400)
                
            if 'password' in new_client:
                #Apply checks on password to qualify if able to post
                if not check_length(new_client['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_client['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
        
            if 'firstName' in new_client:
                    if not new_client['firstName']:
                        return jsonify('Missing required argument: firstName'), 422
                    if not check_length(new_client['firstName'], 1, 50):
                        return jsonify('ERROR, lastName must be between 1 and 50 characters')
                    
                    
            run_query("INSERT INTO client (email, username, password, firstName) VALUES(?,?,?,?)", [new_client['email'], new_client['username'], hashed_password, new_client['firstName']])
            
                
                
            client_id = run_query('SELECT id FROM client WHERE email=?', [new_client['email']])
            response = client_id[0]
            check_response = response[0]
            token = str(uuid4())
                
            run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, check_response])    
            
            client = run_query('SELECT id, created_at, email, username, firstName FROM client WHERE id=?', [check_response])
            client_response = client[0]
            
            resp = client_dictionary_query_min(client_response)
            resp['token'] = token
            
            return jsonify('Client Created,', resp), 201
        
        # Keys Required, email, username, password, firstName, lastName
        elif {'email', 'username', 'password', 'firstName', 'lastName'} == data.keys(): 
            new_client = new_dictionary_request(data)
            
            if 'email' in new_client:
                
                    #Apply checks on email to qualify if able to post
                    if not check_email(new_client['email']):
                        return jsonify("Error invalid email address submitted"), 400
                    if not check_length(new_client['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400
                
                    check_email_validity = run_query('SELECT email FROM client WHERE email=?', [new_client['email']])
                    
                    
                    if check_email_validity != []:
                        
                        email_validity = check_email_validity[0]
                        if email_validity[0] == new_client['email']:
                            return jsonify('ERROR, email already exists'), 400
        
        
            if 'username' in new_client:
                #Apply checks on username to qualify if able to post
                if not check_length(new_client['username'], 1, 50):
                    return jsonify('ERROR, username must be between 1 and 50 characters'), 400
                
                check_username_validity = run_query('SELECT username FROM client WHERE username=?', [new_client['username']])
                
                if check_username_validity != []:
                    username_validity = check_username_validity[0]
                    response = username_validity[0]
                    if response == new_client['username']:
                        return jsonify('username already exists', 400)
                    
                    
            if 'password' in new_client:
                
                if not check_length(new_client['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_client['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
                
                    
            if 'firstName' in new_client:
                if not new_client['firstName']:
                    return jsonify('Missing required argument: firstName'), 422
                if not check_length(new_client['lastName'], 1, 50):
                    return jsonify('ERROR, lastName must be between 1 and 50 characters')
                
                
            if 'lastName' in new_client:
                if not check_length(new_client['lastName'], 1, 50):
                    return jsonify('ERROR, lastName must be between 1 and 50 characters')
                
            
            run_query("INSERT INTO client (email, username, password, firstName, lastName) VALUES(?,?,?,?,?)", [new_client['email'], new_client['username'], hashed_password, new_client['firstName'], new_client['lastName']])
            
            client_id = run_query('SELECT id FROM client WHERE email=?', [new_client['email']])
            response = client_id[0]
            check_response = response[0]
            token = str(uuid4())
                
            run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, check_response])    
            resp['token'] = token
            return jsonify('Client Created,', resp), 201
        
        
        # Keys Required, email, username, password, firstName, picture_url
        elif {'email', 'username', 'password', 'firstName', 'picture_url'} == data.keys():
            new_client = new_dictionary_request(data)
            
            if 'email' in new_client:
                
                
                    if not check_email(new_client['email']):
                        return jsonify("Error invalid email address submitted"), 400
                    if not check_length(new_client['email'], 5, 75):
                        return jsonify('ERROR, email must be between 5 and 75 characters'), 400
                
                    check_email_validity = run_query('SELECT email FROM client WHERE email=?', [new_client['email']])
                    
                    
                    if check_email_validity != []:
                        
                        email_validity = check_email_validity[0]
                        if email_validity[0] == new_client['email']:
                            return jsonify('ERROR, email already exists'), 400
        
            if 'username' in new_client:
                
                if not check_length(new_client['username'], 1, 50):
                    return jsonify('ERROR, username must be between 1 and 50 characters'), 400
                
                check_username_validity = run_query('SELECT username FROM client WHERE username=?', [new_client['username']])
                
                if check_username_validity != []:
                    username_validity = check_username_validity[0]
                    response = username_validity[0]
                    if response == new_client['username']:
                        return jsonify('username already exists', 400)
            
            if 'password' in new_client:
                
                if not check_length(new_client['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_client['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
                
                
            if 'firstName' in new_client:
                if not new_client['firstName']:
                    return jsonify('Missing required argument: firstName'), 422
                if not check_length(new_client['firstName'], 1, 50):
                    return jsonify('ERROR, firstName must be between 1 and 50 characters')
                    
                    
            if 'picture_url' in new_client:
                if not check_length(new_client['picture_url'], 1, 300):
                    return jsonify('ERROR, picture_url must be between 1 and 300 characters')
                
            run_query("INSERT INTO client (email, username, password, firstName, picture_url) VALUE(?,?,?,?,?)", [new_client['email'], new_client['username'], hashed_password, new_client['firstName'], new_client['picture_url']])
            
                
                
            client_id = run_query('SELECT id FROM client WHERE email=?', [new_client['email']])
            response = client_id[0]
            check_response = response[0]
            
            token = str(uuid4())
                
            run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, check_response])    
            
            client = run_query('SELECT id, created_at, email, username, firstName, picture_url FROM client WHERE id=?', [check_response])
            client_response = client[0]
            
            resp = client_dictionary_query_pictureURL(client_response)
            resp['token'] = token
            
            return jsonify('Client Created,', resp), 201
            
            
        # Keys Required, email, username, password, firstName, lastName, picture_url
        elif {'email', 'username', 'password', 'firstName', 'lastName', 'picture_url'} == data.keys():
            new_client = new_dictionary_request(data)
            
        
    
            if 'email' in new_client:
            
            
                if not check_email(new_client['email']):
                    return jsonify("Error invalid email address submitted"), 400
                if not check_length(new_client['email'], 5, 75):
                    return jsonify('ERROR, email must be between 5 and 75 characters'), 400
            
                check_email_validity = run_query('SELECT email FROM client WHERE email=?', [new_client['email']])
                
                
                if check_email_validity != []:
                    
                    email_validity = check_email_validity[0]
                    if email_validity[0] == new_client['email']:
                        return jsonify('ERROR, email already exists'), 400
            

            
            if 'username' in new_client:
                
                if not check_length(new_client['username'], 1, 50):
                    return jsonify('ERROR, username must be between 1 and 50 characters'), 400
                
                check_username_validity = run_query('SELECT username FROM client WHERE username=?', [new_client['username']])
                
                if check_username_validity != []:
                    username_validity = check_username_validity[0]
                    response = username_validity[0]
                    if response == new_client['username']:
                        return jsonify('username already exists', 400)
                    
                    
            if 'password' in new_client:
                
                if not check_length(new_client['password'], 6, 200):
                    return jsonify('')
                
                password = str(new_client['password'])
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)
                    
                    
                    
            if 'firstName' in new_client:
                if not new_client['firstName']:
                    return jsonify('Missing required argument: firstName'), 422
                if not check_length(new_client['lastName'], 1, 50):
                    return jsonify('ERROR, lastName must be between 1 and 50 characters')
            
            if 'lastName' in new_client:
                if not check_length(new_client['lastName'], 1, 50):
                    return jsonify('ERROR, lastName must be between 1 and 50 characters')
                
            if 'picture_url' in new_client:
                if not check_length(new_client['picture_url'], 1, 300):
                    return jsonify('ERROR, picture_url must be between 1 and 300 characters')
            
            run_query("INSERT INTO client (email, username, password, firstName, lastName, picture_url) VALUE(?,?,?,?,?,?)", [new_client['email'], new_client['username'], hashed_password, new_client['firstName'], new_client['lastName'], new_client['picture_url']])
            
                
                
            client_id = run_query('SELECT id FROM client WHERE email=?', [new_client['email']])
            
            response = client_id[0]
            check_response = response[0]
            
            token = str(uuid4())
                
            run_query("INSERT INTO client_session (token, client_id) VALUES (?,?)", [token, check_response])    
            
            client = run_query('SELECT id, created_at, email, username, firstName, lastName, picture_url FROM client WHERE id=?', [check_response])
            client_response = client[0]
            
            resp = client_dictionary_query(client_response)
            resp['token'] = token
            
            return jsonify('Client Created,', resp), 201
        
        else:
            return jsonify('Incorrect keys submitted'), 400
    else:
        return jsonify('Error, invalid amount of data submitted')
    
    
    
@app.patch('/api/client')
def client_patch():
    
                    # TODO: comment code
                    # TODO: error handling
    params = request.args
    data = request.json
    token = params.get('token')
    
    if token != None:
        token_valid = run_query('SELECT token FROM client_session WHERE token=?', [token])
        token_valid_response = token_valid[0]
        response = token_valid_response[0]
        
        
        if response == token:
            allowed_keys= {"token", "email", "username", "password", "firstName", "lastName", "picture_url"}
            
            if allowed_data_keys(data, allowed_keys):
            
                update_client =  new_dictionary_request(data)
            
        
            
                if 'email' in update_client:
                    if not check_length(update_client['email'], 1, 75):
                        return jsonify('Invalid length, email must be between 1 and 75 characters')
                    if not check_email(update_client['email']):
                        return jsonify("Error, Not a valid email"), 400
                    
                    email_exists = run_query('SELECT email FROM client WHERE email=?', [update_client['email']])
                    if email_exists != []:
                        return jsonify('Email already exists'), 400
                    run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.email=? WHERE client_session.token=?', [update_client['email'], token])
                    
                if 'username' in update_client:
                    if not check_length(update_client['username'], 1, 50):
                        return Response('Invalid length, username must be between 1 and 50 characters')
                    
                    username_exists = run_query('SELECT username FROM client WHERE username=?', [update_client['username']])
                    if username_exists != []:
                        return jsonify('Username already Exists')
                    run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id  SET client.username=? WHERE client_session.token=?', [update_client['username'], token])
                    
                if 'firstName' in update_client:
                    if not check_length(update_client['firstName'], 1, 50):
                        return Response('Invalid length, firstName must be between 1 and 50 characters')
                    run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.firstName=? WHERE client_session.token=?', [update_client['firstName'], token])
                    
                if 'lastName' in update_client:
                    if not check_length(update_client['lastName'], 1, 50):
                        return Response('Invalid length, lastName must be between 1 and 50 characters')
                    run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.lastName=? WHERE client_session.token=?', [update_client['lastName'], token])
                    
                if 'picture_url' in update_client:
                    if not check_length(update_client['picture_url'], 1, 300):
                        return Response('Invalid length, picture_url must be between 1 and 300 characters')
                    run_query('UPDATE client INNER JOIN client_session ON client.id=client_session.client_id SET client.picture_url=? WHERE client_session.token=?', [update_client['picture_url'], token])
                
                
                return jsonify("Client information updated"), 200
            
            else:
                return jsonify('ERROR incorrect key values submitted'), 400
        else:
            return jsonify('Invalid session token'), 400
    else:
        return jsonify('A valid session token is needed'), 400
    
    
@app.delete('/api/client')
def client_delete():
                    
                    # TODO: Refine error handling and comment code
    params = request.args
    token = params.get('token')
    
    if token != "":
        token_valid = run_query('SELECT token FROM client_session WHERE token=?', [token])
        
        if token_valid != []:
            response = token_valid[0]
            if response[0] == token:
                
                comparison = run_query('SELECT client_session.token, client.password, client.id FROM client INNER JOIN client_session ON client.id=client_session.client_id WHERE client_session.token=?', [token])
                comp_response = comparison[0]
                
                run_query('DELETE FROM client_session WHERE token=?', [comp_response[0]])
                
                run_query('DELETE FROM client WHERE id=?', [comp_response[2]])
                return jsonify('Delete Success'), 200
                
            else:
                return jsonify("Invalid Token was passed", token)
        else:
            return jsonify('submitted token is not a valid session token')
    else:
        return jsonify('Error, no token present')
        