from flask import Flask

app = Flask(__name__)

from endpoints import client, menu_item, restaurant, client_session, restaurant_session, orders