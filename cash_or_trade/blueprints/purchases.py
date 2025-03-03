from flask import Blueprint, render_template, redirect, url_for

purchases = Blueprint('purchases', __name__, url_prefix='/purchases')