from app import app
from flask import jsonify
from helpers.db_helpers import run_query

@app.get('/api/menu_items')
def menu_items_get():
    return
    
@app.post('/api/menu_items')
def menu_items_post():
    return 
    
@app.patch('/api/menu_items')
def menu_items_patch():
    return
    
@app.delete('/api/menu_items')
def menu_items_delete():
    return
