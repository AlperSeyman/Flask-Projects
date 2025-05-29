from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',  methods=["POST","GET"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":

        # Purchase Item Logic
        purchased_item = request.form.get("purchased_item")
        p_items_obj = Item.query.filter_by(name=purchased_item).first()
        if p_items_obj:
            if current_user.can_purchase(p_items_obj):
                p_items_obj.buy_item(user=current_user)
                flash(f"You purchased {p_items_obj.name} for {p_items_obj.price}$", category="success")
            else:
                flash(f"Unfourtunately, you do not have enough to purchase { p_items_obj.name}", category="danger")
        
        # Sell Item Logic
        selling_item = request.form.get("selling_item")
        s_items_obj = Item.query.filter_by(name=selling_item).first()
        if s_items_obj:
            if current_user.can_sell(s_items_obj):
                s_items_obj.sell_item(user=current_user)
                flash(f"You sold {s_items_obj.name} back to market.", category="success")
            else:
                flash(f"Something went wront with selling {selling_item.name}", category="danger")
        


        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner_id=None) 
        owned_items = Item.query.filter_by(owner_id=current_user.id)
        return render_template('market.html', items = items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items)


@app.route('/register', methods=["POST","GET"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email_address = form.email_address.data,
            password =  form.password1.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Account created successfully! You are logged in as : {user.username}", category="success")
        return redirect(url_for('market_page'))
    
    if form.errors != {}:  # If there are not errors from the validotions
        for field, error_mesg in form.errors.items():
            flash(f"There was an error with {field}: {error_mesg}", category='danger')
    return render_template('register.html', form=form)




@app.route('/login', methods=["POST","GET"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(user_password=form.password.data):
            login_user(user)
            flash(f"Success! You are logged in as : {user.username}", category="success")
            return redirect(url_for('market_page'))
        else:
            flash(f"Username and password are incorrect! Please try again.", category="danger")
    return render_template('login.html', form=form)


@app.route('/logout', methods=["POST","GET"])
def logout_page():
    logout_user()
    flash(f"You logged out!", category="info")
    return redirect(url_for("home_page"))
