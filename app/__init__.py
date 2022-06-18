from flask import Flask

app = Flask(__name__)

from endpoints import client, restaurant, client_session, restaurant_session, menu_items, orders