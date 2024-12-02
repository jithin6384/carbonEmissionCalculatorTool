from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField,IntegerField;
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Log In', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()], render_kw={"class": "form-control"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    company_name = StringField('Companyname', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')], render_kw={"class": "form-control"})
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Register!', render_kw={"class": "btn btn-primary"})

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
    electricity_bill = FloatField("monthly electricity bill in euros", validators=[DataRequired()], render_kw={"class": "form-control"} )
    natural_gas_bill = FloatField("monthly natural gas bill in euros", validators=[DataRequired()], render_kw={"class": "form-control"} )
    fuel_bill = FloatField("monthly fuel bill in euros", validators=[DataRequired()], render_kw={"class": "form-control"} );

    # Waste Selection

    waste_generated = FloatField("monthly waste generated in kg", validators=[DataRequired()], render_kw={"class": "form-control"})
    recycling_percentage = FloatField("percentage of waste recycled in month", validators=[DataRequired()], render_kw={"class": "form-control"})

    # Business Travel
    kilometers_traveled = IntegerField("how many kilometers are travlled annually for business purpose", validators=[DataRequired()], render_kw={"class": "form-control"});
    fuel_efficiency = IntegerField("Fuel efficiency of vehicles liters per 100 km", validators=[DataRequired()], render_kw={"class": "form-control"});
    
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"});