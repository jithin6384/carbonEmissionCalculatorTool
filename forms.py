from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField,IntegerField;
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    company_name = StringField('Companyname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
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