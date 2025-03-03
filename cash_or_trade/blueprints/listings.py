from flask import Blueprint, render_template, redirect, url_for

listings = Blueprint('listings', __name__, url_prefix='/listings')

@listings.route('')
def home():
    return render_template('listings/index.html')