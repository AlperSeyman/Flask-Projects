from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


# Register 
@users.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    registration_form = RegistrationForm()
    
    if registration_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        user = User(
            username=registration_form.username.data,
            email = registration_form.email.data,
            password= hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully!  You can log in now", category="success")
        return redirect(url_for('users.login_page'))
    

    return render_template('register.html', title="Register", registration_form=registration_form)


# Log in
@users.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home_page'))
        else:
            flash(f"Email and Password are incorrect! Please try again.", category="danger") 

    return render_template('login.html', title="Login", login_form=login_form)


# Log out
@users.route('/logout')
def logout_page():
    logout_user()
    flash("You logged out!", category="info")
    return redirect(url_for("main.home_page"))


# Update Account Information
@users.route('/account',methods=['GET', 'POST'])
@login_required
def account_page():
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    update_account_form = UpdateAccountForm()
    if update_account_form.validate_on_submit():
        
        #Update Account Info
        
        if update_account_form.picture.data:
            picture_file = save_picture(update_account_form.picture.data)
            current_user.image_file = picture_file

        current_user.username = update_account_form.username.data
        current_user.email = update_account_form.email.data
        db.session.commit()
        flash("Your account has updated!", category="success")
        return redirect(url_for("users.account_page"))
    elif request.method == "GET":
        update_account_form.username.data = current_user.username
        update_account_form.email.data = current_user.email

    return render_template("account.html", title="Account", image_file=image_file, update_account_form=update_account_form)



@users.route('/user/<username>')
def userPosts_page(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)

    return render_template('user_posts.html', posts=posts, user=user)



# Send Reset Password Link
@users.route('/reset_password', methods=["POST","GET"])
def resetRequest_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    
    request_reset_form = RequestResetForm()
    if request_reset_form.validate_on_submit():
        user = User.query.filter_by(email=request_reset_form.email.data).first()

        # Send Mail
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", category='info')
        return redirect(url_for('users.login_page'))
    return render_template('resetRequest_password.html', title='Reset Password', request_reset_form=request_reset_form)

# Reset Password 
@users.route('/reset_password/<token>', methods=["POST","GET"])
def resetToken_page(token):
    if current_user.is_authenticated:   
        return redirect(url_for('main.home_page'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('users.resetRequest_page'))
    
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reset_password_form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has updated', category='success')
        return redirect(url_for('users.login_page'))
    
    return render_template('reset_token_password.html', title='Reset Password', reset_password_form=reset_password_form)
