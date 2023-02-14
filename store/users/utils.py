import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from store import mail
from datetime import datetime, timedelta
import jwt


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    crop_rectangle = (50, 50, 100, 20)
    
    i = Image.open(form_picture)
    img_width, img_height = i.size
    if img_height > img_width:
        crop_width = img_width
        crop_height = img_width
    else:
        crop_width = img_height
        crop_height = img_height
    new_img = i.crop(((img_width - crop_width) // 2,
                      (img_height - crop_height) // 2,
                      (img_width + crop_width) // 2,
                      (img_height + crop_height) // 2))
    img = new_img.resize((200,200))
    img.save(picture_path, quality=95)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='notifications@moviezyng.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def email_register_token(email, expires_sec=1800):
    token = jwt.encode(
        {
            'email': email,
            'error': False,
            'exp': datetime.now()+timedelta(seconds=expires_sec)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    msg = Message('STORE Registration Invite',
                    sender='notifications@moviezyng.com',
                    recipients=[email])
    msg.body = f'''You have been invited to sign up for the STORE. Visit the following link: 
    {url_for('users.register', token=token, _external=True)}
    
    If you do not expect this, simply ignore this email and nothing will happen.
    '''
    mail.send(msg)

def verify_register_token(token):
    try:
        signature = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            leeway=timedelta(seconds=10),
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        signature = {'error': True}
    return signature

def email_on_register(emails, user):
    msg = Message(f'AVEntertainment User {user} Registered',
                  sender='notifications@moviezyng.com',
                  recipients=emails)
    msg.body = f'''A new user has finshed their registration.
            
            {user} can now be managed and tools can be added to their account
            '''
    mail.send(msg)
