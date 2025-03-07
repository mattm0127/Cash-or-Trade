from flask import Blueprint, render_template, redirect, url_for, request
from cash_or_trade import db_client

listings = Blueprint('listings', __name__, url_prefix='/listings')

@listings.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        type_filter = request.form.get('filter')
        all_listings = db_client.all_listings_get(type_filter)
        return render_template('listings/all_listings.html', 
                               all_listings=all_listings,
                               type_filter=type_filter)
    all_listings = db_client.all_listings_get('all')
    return render_template('listings/all_listings.html', 
                           all_listings=all_listings,
                           type_filter='all')

@listings.route('/view/<listing_id>')
def show_listing(listing_id):
    listing = db_client.show_listing_get(listing_id)
    return render_template('/listings/show_listing.html', listing=listing)