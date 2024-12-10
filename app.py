from flask import Flask, render_template, request, session
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_required, current_user;

from forms import LoginForm, RegistrationForm, QuestionaireForm
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
if(os.getenv('RENDER')):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/data/data.sqlite'
else:
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
    
    def __repr__(self):
        return(f"name is {self.username} company name is {self.company_name}");

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
    def __repr__(self):
        return f"energy usage is {self.electricity_bill} and {self.fuel_bill} and {self.natural_gas_bill}"


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
    def __repr__(self):
        return f"waste is {self.waste_generated} and {self.recycling_percantage}"

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
    def __repr__(self):
        return f"waste is {self.kilometer_traveled} and {self.fuel_efficiency}"

@app.route('/')
def home():
    # print("current user energy usage ==>", current_user.energy_usage)
    # print("current user  waste generated => ", current_user.waste)
    # print("current user  business travel => ", current_user.buisness_travel);
    # f"energy usage is {self.electricity_bill} and {self.fuel_bill} and {self.natural_gas_bill}"
    # calculating energy usage for the current user
    electricity_bill = 0;
    fuel_bill = 0;
    natural_gas_bill = 0;
    energy_footprint = 0;
    carbon_data = {};
    suggestions = [];
    company_name = ''
    print("current user is authenticated =>", current_user.is_authenticated);
    if(current_user.is_authenticated):
        if(current_user.energy_usage):
            electricity_bill =  current_user.energy_usage.electricity_bill
            fuel_bill = current_user.energy_usage.fuel_bill
            natural_gas_bill = current_user.energy_usage.natural_gas_bill
            energy_footprint = (electricity_bill * 12 * 0.0005) + (natural_gas_bill * 12 * 0.0053) + (fuel_bill * 12 * 2.32)
            print("electricity bill",electricity_bill );
            print("energy_footprint", energy_footprint);
        
        # calculating waste generated for current user
        waste_generated = 0;
        recycling_percentage = 0;

        if(current_user.waste):
            waste_generated = current_user.waste.waste_generated;
            recycling_percentage = current_user.waste.recycling_percantage
            waste_footprint = (waste_generated * 12) * (0.57 - (recycling_percentage / 100));
        
        # calculating business travel 
        travel_distance = 0;
        fuel_efficiency = 0;
        if(current_user.buisness_travel):
            travel_distance = current_user.buisness_travel.kilometer_traveled;
            fuel_efficiency = current_user.buisness_travel.fuel_efficiency
            travel_footprint = (travel_distance / 1) * (fuel_efficiency / 100) * 2.31
        suggestions = [{"energy_footprint": [], "waste_footprint": [], "travel_footprint" : []}]
       
            
       

        # Energy Usage Suggestions
        if electricity_bill > 5000:
            suggestions[0]["energy_footprint"].append("Switch to energy-efficient appliances and LED bulbs.")
            
        if natural_gas_bill > 1000:
            suggestions[0]["energy_footprint"].append("Improve insulation or switch to renewable energy sources.")
        
        if fuel_bill > 1000:
            suggestions[0]["energy_footprint"].append("Use public transport, carpool, or switch to electric vehicles.")
        
        # Waste Reduction Suggestions
        if recycling_percentage < 50:
            
            suggestions[0]["waste_footprint"].append("Increase recycling efforts and compost organic waste.")
        if waste_generated > 100:
            suggestions[0]["waste_footprint"].append("Reduce single-use plastics and re-use products.")

        # Business Travel Suggestions
        if travel_distance > 10000:
            suggestions[0]["travel_footprint"].append("Reduce travel through virtual meetings.")
        if fuel_efficiency > 8:
           suggestions[0]["travel_footprint"].append("Switch to fuel-efficient or electric vehicles.")

    
        carbon_data = { 
            "categories": ["energy_footprint", "waste_footprint", "travel_footprint", ],
            "values": [energy_footprint, waste_footprint, travel_footprint]
        }
        if(current_user.company_name is not None):
           company_name = current_user.company_name;

        
    return render_template('home.html', carbon_data = carbon_data, suggestions = suggestions, company_name = company_name )


@app.route('/welcome',methods=['GET', 'POST'] )
@login_required
def welcome_user():
    form = QuestionaireForm();
    if(form.validate_on_submit()):
         # check if energy_usage,waste business travel for present user already exists
        try:
            # checking negative values in energy usage
            if ((form.electricity_bill.data <= 0) or (form.natural_gas_bill.data <= 0) or (form.fuel_bill.data <= 0)):
                if(form.electricity_bill.data <= 0):
                    flash('Electricity bill cannot be negative or zero',  "electricityError");
                if(form.natural_gas_bill.data <= 0):
                    flash('Natural gas bill cannot be negative or zero',  "naturalGasError");
                if(form.fuel_bill.data <= 0):
                    flash('Fuel bill cannot be negative or zero',  "fuelError");
                
                
            # checking negative values in waste generated
            if ((form.waste_generated.data <= 0) or (form.recycling_percentage.data <= 0)):
                if((form.waste_generated.data <= 0)):
                    flash("Waste values cannot be negative or zero.", "wasteDanger");
                if((form.recycling_percentage.data <= 0)):
                    flash("Recycling percentage values cannot be negative or zero.", "recyclingDanger");
                
               
            
            # checking negative values in kilometers travelled and fuel efficiency
            if ((form.kilometers_traveled.data <= 0) or (form.fuel_efficiency.data <= 0)):
                if(form.kilometers_traveled.data <= 0):
                    flash("Distance travelled cannot be negative or zero.", "travelDanger");
                if(form.fuel_efficiency.data <= 0):
                    flash("fuel efficiency cannot be negative or zero.", "fuelEfficiencyError");

            if((form.electricity_bill.data <= 0) or (form.natural_gas_bill.data <= 0) or (form.fuel_bill.data <= 0) or (form.waste_generated.data <= 0) or (form.recycling_percentage.data <= 0) or (form.kilometers_traveled.data <= 0) or (form.fuel_efficiency.data <= 0)):  
                return redirect(url_for('welcome_user'))
            
            energy_usage = EnergyUsage.query.filter_by(user_id=current_user.id).first()
            waste = Waste.query.filter_by(user_id=current_user.id).first()
            business_travel = BuisnessTravel.query.filter_by(user_id=current_user.id).first()
            
            # if users doesn't exist
            if not energy_usage:
                energy_usage = EnergyUsage(
                    electricity_bill=form.electricity_bill.data,
                    natural_gas_bill=form.natural_gas_bill.data,
                    fuel_bill=form.fuel_bill.data,
                    user_id=current_user.id
                )
                db.session.add(energy_usage)
            else:
                energy_usage.electricity_bill = form.electricity_bill.data
                energy_usage.natural_gas_bill = form.natural_gas_bill.data
                energy_usage.fuel_bill = form.fuel_bill.data

            # Handle Waste
            if not waste:
                waste = Waste(
                    waste_generated=form.waste_generated.data,
                    recycling_percantage=form.recycling_percentage.data,
                    user_id=current_user.id
                )
                db.session.add(waste)
            else:
                waste.waste_generated = form.waste_generated.data
                waste.recycling_percantage = form.recycling_percentage.data
            
            # Handle Business Travel
            if not business_travel:
                business_travel = BuisnessTravel(
                    kilometer_traveled=form.kilometers_traveled.data,
                    fuel_efficiency=form.fuel_efficiency.data,
                    user_id=current_user.id
                )
                db.session.add(business_travel)
            else:
                business_travel.kilometer_traveled = form.kilometers_traveled.data
                business_travel.fuel_efficiency = form.fuel_efficiency.data

            # Commit all changes
            db.session.commit()
            flash('Data submitted successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback();
            flash(f'An error occured {str(e)}', 'danger');
    
    return render_template('welcome_user.html', form=form)




  

@app.route('/logout')
@login_required
def logout():
    logout_user()
   
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        

            if user is not None and user.check_password(form.password.data) :
            

                login_user(user)
                flash('Logged in successfully.', 'success')

        
                next = request.args.get('next')
                session.pop('_flashes', None)
                if next == None or not next[0]=='/':
                    if(user.buisness_travel or user.energy_usage or user.waste):
                     next = url_for('home')
                    else:
                     next = url_for('welcome_user')

                return redirect(next)
            else:
              flash("Invalid username or password. Please try again!", 'danger');
        except Exception as e:
              flash(f"An Error occurred: {str(e)} ")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            existing_userEmail = User.query.filter_by(email=form.email.data).first()
            # check for existing email 
            if(existing_userEmail):
                flash('Email is already registered please use a different Email', 'emailDanger');
            
            existing_username = User.query.filter_by(username=form.username.data).first();
            if(existing_username):
                flash('Username is already registered please use a different Username', 'userNamedanger');
               
            existing_company = User.query.filter_by(company_name=form.company_name.data).first();
            if(existing_company):
                flash("Company is already registered please use a different CompanyName", "companyNameDanger")
            
            if(existing_userEmail or existing_company or existing_username):
                return redirect(url_for('register'))
            user = User(email=form.email.data,
                        username=form.username.data,
                        company_name=form.company_name.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback();
            flash(f'An error occured during registration: {str(e)}', 'danger')
    return render_template('register.html', form=form)

@app.route('/summary', methods=['GET'])
@login_required
def summary():
    users = User.query.all();
    company_summaries = [];
    print('users => ', users)
    for user in users:
        print('user company name', user.company_name)
        if user.company_name and (user.energy_usage is not None or user.waste is not None or user.buisness_travel is not None) :
            company_data = {'energy_footprint': 0, 'waste_footprint' : 0, 'travel_footprint' : 0, 'total_footprint': 0, 'company_name' :  user.company_name}
            
            if user.energy_usage:
                electricity_bill =  user.energy_usage.electricity_bill
                fuel_bill = user.energy_usage.fuel_bill
                natural_gas_bill = user.energy_usage.natural_gas_bill
                energy_footprint = (electricity_bill * 12 * 0.0005) + (natural_gas_bill * 12 * 0.0053) + (fuel_bill * 12 * 2.32);
                company_data['energy_footprint'] = int(energy_footprint);
                company_data['total_footprint'] = company_data['total_footprint'] + int(energy_footprint);
            
            if(user.waste):
                waste_generated = user.waste.waste_generated;
                recycling_percentage = user.waste.recycling_percantage
                waste_footprint = (waste_generated * 12) * (0.57 - (recycling_percentage / 100));
                company_data['waste_footprint'] = int(waste_footprint);
                company_data['total_footprint'] = company_data['total_footprint'] + int(waste_footprint);
            if(user.buisness_travel):
                travel_distance = user.buisness_travel.kilometer_traveled;
                fuel_efficiency = user.buisness_travel.fuel_efficiency
                travel_footprint = (travel_distance / 1) * (fuel_efficiency / 100) * 2.31;
                company_data["travel_footprint"] = int(travel_footprint);
                company_data['total_footprint'] = company_data['total_footprint'] + int(travel_footprint);
            company_summaries.append(company_data);
    company_summaries = sorted(company_summaries, key= lambda x: x["total_footprint"])
    return  render_template('summary.html', company_summaries = company_summaries);
if __name__ == '__main__':
    app.run(debug=False)
