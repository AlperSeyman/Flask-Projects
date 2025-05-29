from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User



class RegistrationForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username aldready exists! Please try a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already exists! Please try a different email address')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')




class UpdateAccountForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    picture = FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField(label="Update")


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username aldready exists! Please try a different username')
        
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already exists! Please try a different email address')
            


class RequestResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label="Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no accoount with that email. You must register first.')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Reset Password")