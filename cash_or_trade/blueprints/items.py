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
        db_client.add_item_post(username, request.form, request.files)
        return redirect(url_for('items.user_items', username=username))
    return render_template('items/add_item.html')

@items.route('/<username>/<item_id>')
def show_item(username, item_id):
    item = db_client.show_user_item_get(username, item_id)
    return render_template('items/show_item.html', item=item)


@items.route('/<username>/<item_id>/edit', methods=["GET", "POST"])
def edit_item(username, item_id):
    item = db_client.show_user_item_get(username, item_id)
    if request.method == "POST":
        db_client.edit_user_item_post(username, item_id, request.form, request.files)
        return redirect(url_for('items.show_item', username=username, item_id=item.id))
    return render_template('items/edit_item.html', item=item)

@items.route('/<username>/<item_id>/delete', methods=["GET", "POST"])
def delete_item(username, item_id):
    if request.method == "POST":
        db_client.delete_item_post(username, item_id)
        return redirect(url_for('items.user_items', username=username))
    item = db_client.show_user_item_get(username, item_id)
    return render_template('items/delete_item.html', item=item)

