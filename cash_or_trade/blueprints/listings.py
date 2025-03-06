from flask import Blueprint, render_template, redirect, url_for
from cash_or_trade import db_client

listings = Blueprint('listings', __name__, url_prefix='/listings')

@listings.route('/')
def home():
    all_listings = db_client.all_listings_get()
    return render_template('listings/all_listings.html', all_listings=all_listings)

@listings.route('/view/<listing_id>')
def show_listing(listing_id):
    listing = db_client.show_listing_get(listing_id)
    return render_template('/listings/show_listing.html', listing=listing)