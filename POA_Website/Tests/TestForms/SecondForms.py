from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, validators, DecimalField
from wtforms.fields.html5 import EmailField

class CreateAccountForm(FlaskForm):
    #Higher order memes.
    FirstName_Box = StringField("First Name", [validators.DataRequired("First Name Required")])
    LastName_Box = StringField("Last Name", [validators.DataRequired("Last Name Required")])
    Email_Box = StringField("Email", [validators.DataRequired("Email Required")])
    Age_Box = IntegerField("Age", [validators.DataRequired("Age Required")])
    Height_Box = IntegerField("Height (inches)", [validators.DataRequired("Height Required")])
    StudentIDNumber_Box = IntegerField("Student ID #", [validators.DataRequired("Student ID Number Required")])
    PhoneNumber_Box = IntegerField("Phone Number", [validators.DataRequired("Phone Number Required")])
    CarCapacity_Box = IntegerField("Car Capacity", [validators.DataRequired("Car Capacity Required")])
    submit = SubmitField("Create Account")
    # Is "DecimalField a thing?