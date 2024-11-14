from flask_wtf import FlaskForm;
from wtforms import StringField, PasswordField, SubmitField, ValidationError, FloatField, IntegerField;
from wtforms.validators import DataRequired, Email, EqualTo;



# LoginForm 

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email] )
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm')] )
    submit = SubmitField('Log in');
# signup form for company owners

class SignupForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email]);
    username = StringField('Username',validators=[DataRequired()]);
    companyname = StringField('Companyname',validators=[DataRequired()]);
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm')] )
    password_confirm = PasswordField('Confirm Password',validators=[DataRequired()] )
    submit = SubmitField('Sign up');


    def check_email(self, field):
        from models import User;
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
        
    def check_username(self, field):
        from models import User;
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
        


# Questionaire Form

class QuestionaireForm(FlaskForm):
    # EnergyUsage Form
    electricity_bill = FloatField("monthly electricity bill in euros", validators=[DataRequired()] )
    natural_gas_bill = FloatField("monthly natural gas bill in euros", validators=[DataRequired()] )
    fuel_bill = FloatField("monthly fuel bill in euros", validators=[DataRequired()] );

    # Waste Selection

    waste_generated = FloatField("monthly waste generated in kg", validators=[DataRequired()])
    recycling_percentage = FloatField("percentage of waste recycled in month", validators=[DataRequired()])

    # Business Travel
    kilometers_traveled = IntegerField("how many kilometers are travlled annually for business purpose", validators=[DataRequired()]);
    fuel_efficiency = IntegerField("Fuel efficiency of vehicles liters per 100 km", validators=[DataRequired()]);
    
    submit = SubmitField('Submit');
   
    