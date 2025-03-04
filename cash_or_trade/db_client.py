import bcrypt
from cash_or_trade.extensions import database as db
from cash_or_trade.models import Users, Items, Descriptions, Purchases

def _validate_new_user_form(form):
    # Check for empty fields
    for value in form.values():
        if not value:
            return (False, 'Please fill in all fields.')
    # Check if username already taken
    username = form.get('username')
    username_check = Users.query.filter(Users.username==username).first()
    if username_check:
        return (False, "Username already exists")
    # Check if email already in use
    email = form.get('email')
    email_check = Users.query.filter(Users.email==email).first()
    if email_check:
        return (False, "Email already in use.")
    # Check if passwords match
    if form.get('password') != form.get('check_password'):
        return (False, 'Passwords do not match')
    return (True, form)

def register_new_user(form):
    valid, response = _validate_new_user_form(form)
    if not valid:
        return (False, response)
    try:
        salt = bcrypt.gensalt()
        username = response.get('username')
        password = bcrypt.hashpw(response.get('password').encode('utf-8'), salt)
        email = response.get('email')
        new_user = Users(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return (True, username)
    except Exception:
        return (False, "Error Creating Account, Try Again.")

def validate_user(form):
    try:
        username = form.get('username')
        user = Users.query.filter(Users.username==username).first()
        if bcrypt.checkpw(form.get('password').encode("utf-8"),
                        user.password):
            return (True, username)
        return (False, "Incorrect Password.")
    except Exception:
        return (False, "Incorrect Username")

def user_items_get(username):
    try:
        user = Users.query.filter(Users.username==username).first()
        user_items = Items.query.filter(Items.user_id==user.id).all()
        return user_items
    except Exception:
        return "An Error Occured Try Again"
    
def add_item_post(username, form):
    try:
        user = Users.query.filter(Users.username==username).first()
        new_item = Items(
                user_id = user.id,
                type = form.get('type'),
                name = form.get('name'),
                price = form.get('price'),
                tradeable = form.get('tradeable'),
                status = form.get('status'),
            )
        db.session.add(new_item)
        db.session.commit()
    except Exception:
        print(Exception)