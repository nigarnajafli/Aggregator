from flask import redirect, request, render_template, url_for, flash
from application import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, SearchForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from .business_layer.collector import Collector


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    product = form.product.data
    minimum = form.minimum.data
    maximum = form.maximum.data
    sorting = None
    currency = None
    choices = [site for site in ['amazon', 'tapaz', 'aliexpress']
               if request.form.getlist(site) == ['on']
               ]
    if request.method == 'POST':
        sorting = request.form['sort_pr']
        currency = request.form['currency']
    if product:
        collector = Collector(choices, product, minimum, maximum, currency, sorting)
        all_records = collector.get_data()
    else:
        all_records = {'amazon': {}, 'tapaz': {}, 'aliexpress': {}}
    return render_template('search.html', title='Search', form=form, all_records=all_records)
