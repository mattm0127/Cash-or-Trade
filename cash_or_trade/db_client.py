import io
from decimal import Decimal
import bcrypt
from cash_or_trade.extensions import database as db
from cash_or_trade.extensions import s3_client
from cash_or_trade.models import Users, Items, Descriptions, Purchases
from decouple import config
from PIL import Image

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

def _convert_and_upload_s3(files, item):
    db_columns = {1: 'img1', 
                    2: 'img2', 
                    3: 'img3', 
                    4: 'img4', 
                    5: 'img5'}
    file_prefix = f"{item.user.username}/{item.id}/"
    for x in range(1,6):
        if files.get(f'img{x}'):
            file = files.get(f'img{x}')
            key = file_prefix + f'img{x}.png'
            max_width = 1920
            max_height = 1080
            with Image.open(file) as image:
                image.thumbnail((max_width, max_height))
                png_buffer = io.BytesIO()
                image.save(png_buffer, format='PNG')
            png_buffer.seek(0)
            s3_client.upload_fileobj(png_buffer, 
                                        config('BUCKET_NAME'), 
                                        key, 
                                        ExtraArgs={'ContentType': 'image/png'}
                                        )
            s3_url = f"https://{config('BUCKET_NAME')}.s3.{config('BUCKET_REGION')}.amazonaws.com/{key}"
            setattr(item.description, db_columns[x], s3_url)
    return item

def _delete_from_s3(username, item_id):
    keys_to_delete = [f"{username}/{item_id}/img{x}.png" for x in range(1,6)]
    response = s3_client.delete_objects(
        Bucket=config("BUCKET_NAME"),
        Delete = {'Objects': [{'Key': key} for key in keys_to_delete]}
    )
    print(response)

def _add_description(form, files, item):
    new_desc = Descriptions()
    new_desc.item_id = item.id
    new_desc.title = form.get('title')
    new_desc.descr = form.get('descr')
    db.session.add(new_desc)
    db.session.commit()
    new_desc = _convert_and_upload_s3(files=files, item=item)
    item.description_id = new_desc.id
    db.session.commit()

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
        return (False, "Error Creating Account, Try Again")

def validate_user_login(form):
    try:
        username = form.get('username')
        user = Users.query.filter(Users.username==username).first()
        if bcrypt.checkpw(form.get('password').encode("utf-8"),
                        user.password):
            return (True, username)
        return (False, "Incorrect Password")
    except Exception as e:
        print(e)
        return (False, "Incorrect Username")

def get_user_by_username(username):
    user = Users.query.filter(Users.username==username).first()
    return user

def user_items_get(username):
    try:
        user = Users.query.filter(Users.username==username).first()
        user_items = Items.query.filter(Items.user_id==user.id).join(Descriptions, Items.id==Descriptions.item_id).all()
        return user_items
    except Exception:
        return "An Error Occured Try Again"
    
def add_item_post(username, form, files):
    try:
        user = Users.query.filter(Users.username==username).first()
        new_item = Items(
                user_id = user.id,
                type = form.get('type'),
                name = form.get('name'),
                price = Decimal(form.get('price')),
                tradeable = True if form.get('tradeable') else False,
                status = form.get('status'),
            )
        db.session.add(new_item)
        db.session.commit()
        _add_description(form, files, new_item)
        print("Files uploaded")
    except Exception as e:
        print(e)

def show_user_item_get(username, item_id):
    try:
        item = Items.query.get(item_id)
        user = Users.query.get(item.user_id)
        if user.username != username:
            raise IndexError
        return item
    except Exception:
        return "Item Not Found"
    
def edit_user_item_post(username, item_id, form, files):
    try:
        item = Items.query.get(item_id)
        user = Users.query.get(item.user_id)
        if user.username != username:
            raise IndexError('You dont have permission')
        item.type = form.get('type') 
        item.name = form.get('name') if len(form.get('name')) > 0 else item.name
        item.price = Decimal(form.get('price')) if len(form.get('price')) > 0 else item.price
        item.tradeable = True if form.get('tradeable') else False
        item.status = form.get('status')
        item.description.title = form.get('title')
        item.description.descr = form.get('descr')
        item = _convert_and_upload_s3(files, item)
        db.session.commit()
    except Exception as e:
        return e

def delete_item_post(username, item_id):
    try:
        item = Items.query.get(item_id)
        if username != item.user.username:
            raise ValueError("You dont have permission")
        _delete_from_s3(username, item_id)
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        print(e)
        return e
        
def all_listings_get(filter):
    if filter == 'all':
        all_listings = Items.query.filter(Items.status=='public').all()
    else:
        all_listings = Items.query.filter(Items.status=='public', Items.type==filter).all()
    return all_listings

def show_listing_get(listing_id):
    try:
        listing = Items.query.filter(Items.status=='public', 
                                     Items.id==listing_id).first()
        return listing
    except Exception as e:
        return None