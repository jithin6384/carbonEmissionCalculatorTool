from flask import Flask, render_template, request, jsonify
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)

login_manager.login_view = "login"

# defining users here 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    company_name = db.Column(db.Text, unique=True, index=True);
    password_hash = db.Column(db.String(128))

    # creating relationships
    energy_usage = db.relationship('EnergyUsage', backref = 'user', uselist = False);
    waste = db.relationship('Waste', backref = 'user', uselist = False);
    buisness_travel = db.relationship('BuisnessTravel', backref = 'user', uselist = False);

    def __init__(self, email, username,company_name, password):
        self.email = email
        self.username = username;
        self.company_name = company_name;
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        
        return check_password_hash(self.password_hash,password)
    

class EnergyUsage(db.Model):

    __tablename__ = 'energy_usage';
    id = db.Column(db.Integer, primary_key=True)
    electricity_bill = db.Column(db.Float, nullable = True);
    natural_gas_bill = db.Column(db.Float, nullable = True);
    fuel_bill = db.Column(db.Float, nullable = True);
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False);

    def __init__(self, electricity_bill,natural_gas_bill, fuel_bill, user_id):
         self.electricity_bill = electricity_bill;
         self.natural_gas_bill = natural_gas_bill;
         self.fuel_bill = fuel_bill;
         self.user_id = user_id;



class Waste(db.Model):
    __tablename__ = 'waste';
    id = db.Column(db.Integer, primary_key=True);
    waste_generated = db.Column(db.Float, nullable = True);
    recycling_percantage = db.Column(db.Float, nullable = True);
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False);

    def __init__(self, waste_generated,recycling_percantage, user_id):
         self.waste_generated = waste_generated;
         self.recycling_percantage = recycling_percantage;
         self.user_id = user_id;
    

class BuisnessTravel(db.Model):
    __tablename__ = 'business_travel';
    id = db.Column(db.Integer, primary_key=True);
    kilometer_traveled = db.Column(db.Float, nullable = True);
    fuel_efficiency = db.Column(db.Float, nullable = True);
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False);
    
    def __init__(self, kilometer_traveled,fuel_efficiency, user_id):
         self.kilometer_traveled = kilometer_traveled;
         self.fuel_efficiency = fuel_efficiency;
         self.user_id = user_id;


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
       

        if user.check_password(form.password.data) and user is not None:
        

            login_user(user)
            flash('Logged in successfully.')

      
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    company_name=form.company_name.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
