from flask import Blueprint, render_template, redirect, url_for, session, request
from cash_or_trade import db_client

items = Blueprint('items', __name__, url_prefix='/items')

@items.route('/<username>')
def user_items(username):
    user_items = db_client.user_items_get(username)
    return render_template('items/user_items.html', user_items=user_items)

@items.route('/<username>/add', methods=["GET", "POST"])
def add_item(username):
    if request.method == "POST":
        db_client.add_item_post(username, request.form)
        return render_template('items/user_items.html')
    return render_template('items/add_item.html')
