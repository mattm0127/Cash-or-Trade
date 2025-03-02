from flask import Blueprint, render_template, redirect, url_for

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')