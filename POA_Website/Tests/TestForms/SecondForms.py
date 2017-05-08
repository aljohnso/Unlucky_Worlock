from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, validators, DecimalField
from wtforms.fields.html5 import EmailField

class CreateAccountForm(FlaskForm):
    #Higher order memes.
    FirstName_Box = StringField("First Name", [validators.DataRequired("Gimme a name")])
    LastName_Box = StringField("Last Name", [validators.DataRequired("Gimme a name")])
    Email_Box = StringField("Email", [validators.DataRequired("Gimme a name")])
    Age_Box = IntegerField("Age", [validators.DataRequired("Gimme a name")])
    Height_Box = DecimalField("Height (inches(?))", [validators.DataRequired("Gimme a name")])
    StudentIDNumber_Box = IntegerField("Student ID #", [validators.DataRequired("Gimme a name")])
    PhoneNumber_Box = IntegerField("Phone Number", [validators.DataRequired("Gimme a name")])
    CarCapacity_Box = IntegerField("Car Capacity", [validators.DataRequired("Gimme a name")])
    submit = SubmitField("Create Account")