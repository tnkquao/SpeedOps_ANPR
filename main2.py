from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import timedelta          # import done set up max time session could last for before automatic usr logout 
from datetime import datetime

from models import *
from forms import *
from fineAmount import Capture

# import line for ANPR
# function call of ANPR returning the license plate details

licenseplate = ""
speed = 0
speeding_instance = Capture(license, speed)

app = Flask(__name__)
app.secret_key='hello'   # secret key used for encrypt and decrypt server data

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/speedops'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.permanent_session_lifetime = timedelta(minutes=5)      # stores permanent session data for 5 minutes


@login_manager.user_loader
def load_user(user_id):
    return admin.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


#real logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = admin.query.filter_by(username=form.username.data).first()
        log = log_track(name=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                db.session.add(log)     # add record of admin login to db
                db.session.commit()     # confirms query
                return redirect(url_for('dashboard'))

#add a part to keep track of admin logins, by adding to a different table for that purpose
        flash("Login Successful!")
    return render_template('login.html', form=form)

# real admin addition
@app.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = admin(username=form.username.data, email=form.email.data, password=hashed_password)
        # possible to consider adding date admin account was created
        db.session.add(new_user)
        db.session.commit()
        flash('New Admin has been added!')
        return redirect('/signup', form=form, values=speeders.query.all())

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', values=speeders.query.all(), user=admin.query.all())


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search = OffenceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('view.html', form=search)

@app.route('/entries', methods=["POST", "GET"])
@login_required
def entries():
    form = OffenceForm()
    
    if form.validate_on_submit():
        speeder = speeders(name=form.name.data, license_plate= form.license_plate.data, 
                speed=form.speed.data, fine=form.fine.data, location=form.location.data)

        db.session.add(speeder)
        db.session.commit()
        return render_template('entries.html', form=form)

    return render_template('entries.html', form=form)

@app.route('/searching', methods=['GET', 'POST'])
@login_required
def pager():
    search = OffenceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('searcher.html', form=search)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def search_results(search):
    results = []
    search = OffenceSearchForm(request.form)

    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Name':
            #user = db.session.query(speeders).filter(
            #    speeders.name.contains(search_string))
            #user = speeders.query.filter_by(name=search_string)

            qry = db_session.query(speeders).filter(
                speeders.name.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'License Plate':
            qry = db_session.query(speeders).filter(
                speeders.license_plate.contains(search_string))
            results = qry.all()
            user = admin.query.filter_by(username=search_string)

        elif search.data['select'] == 'Location':
            qry = db_session.query(speeders).filter(
                speeders.location.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(speeders)
            results = qry.all()
    else:
        qry = db_session.query(speeders)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/searching')

    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table, form=search)
        #return render_template('results.html', results=results)


# displays all culprits who have outstanding fines to pay
@app.route('/paid')
@login_required
def all_paid():
    qry = db_session.query(speeders).filter(speeders.fine_paid==True)
    results = qry.all
    table = Results(results)
    table.border = True
    return render_template('results.html', table=table)


#logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "info")
    #session.pop("user", None)
    # #session.pop("email", None)
    return redirect(url_for("login"))           # take user to login page
    

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)