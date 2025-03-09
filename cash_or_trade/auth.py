from flask import redirect, url_for, session, flash
from functools import wraps

def username_validation(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session_username = session.get('username')
            username = kwargs.get('username')
            if session_username != username:
                  return redirect(url_for('listings.home'))
            return func(*args, **kwargs)
        return wrapper

def require_login(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
            if not session.get('username'):
                  flash('You must be logged in to make an offer', category='message')
                  return redirect(url_for('accounts.login'))
            return func(*args, **kwargs)
      return wrapper
                  