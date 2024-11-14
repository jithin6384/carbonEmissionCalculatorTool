from __init__ import db, login_manager;
from werkzeug.security import generate_password_hash, check_password_hash;
from flask_login import UserMixin;

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    company_name = db.Column(db.Text, unique=True, index=True);
    is_Admin = db.Column(db.Boolean, default = False);
    
    # creating relationships
    energy_usage = db.relationship('EnergyUsage', backref = 'user', useList = False);
    waste = db.relationship('Waste', backref = 'user', useList = False);
    buisness_travel = db.relationship('BuisnessTravel', backref = 'user', useList = False);
    def __init__(self, email, username, password, company_name, is_Admin = False):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.company_name = company_name;
        self.is_Admin = is_Admin;


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
    