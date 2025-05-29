import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog import app, mail



# Save Picture to Database
def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    
    image_size = (125, 125)
    image = Image.open(picture)
    image.thumbnail(image_size)
    image.save(picture_path)

    return picture_filename


# Send Mail Function
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",sender='noreply@demo.com', recipients=[user.email])
    msg.body =f""" To reset your password, visit the following link:
{url_for('resetToken_page', token=token, _external=True)}

If you did not make this request, simply ignore this email.
"""
    mail.send(msg)