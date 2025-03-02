from flask import Blueprint, render_template, redirect, url_for

listings = Blueprint('listings', __name__, url_prefix='/listings')
