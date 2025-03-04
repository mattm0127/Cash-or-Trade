from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from cash_or_trade import db_client


accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

@accounts.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        valid, response = db_client.register_new_user(request.form)
        if valid:
            session['username'] = response
            return redirect(url_for('home'))
        flash(response, category='message')
    return render_template('accounts/register.html')
    
@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Response will be username if valid or error message
        valid, response = db_client.validate_user(request.form)
        if valid:
            session['username'] = response
            return redirect(url_for('home'))
        flash(response, category='message')
    return render_template('accounts/login.html')

@accounts.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))