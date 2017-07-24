from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField, SelectField, validators, DecimalField
from wtforms.fields.html5 import DateField

# https://stackoverflow.com/questions/21815067/how-do-i-validate-wtforms-fields-against-one-another
# ^^^ This could be useful later.

# class SampleValid(object):
#     def __init__(self, min=3, max=3, message=None):
#         self.min = min
#         self.max = max
#         if not message:
#             message = u'Field must be between %i and %i characters long.' % (min, max)
#         self.message = message
#
#     def __call__(self, form, field):
#         l = field.data and len(field.data) or 0
#         if l < self.min or self.max != -1 and l > self.max:
#             raise validators.ValidationError(self.message)

class CheckDigit(object):
    def __init__(self, message=None):
        if not message:
            message = "Please enter a non-negative integer."
        self.message = message

    def __call__(self, form, field):
        if field.data.isdigit() == False:
            raise validators.ValidationError(self.message)
        if int(field.data) < 0:
            # Don't you dare change this to an elif statement, or combine into a single if statement! It will break if you do!
            raise validators.ValidationError(self.message)

class CheckFloat(object):
    def __init__(self, message=None):
        if not message:
            message = "Please enter a non-negative number in decimal form."
        self.message = message

    def __call__(self, form, field):
        cutDots = field.data.replace(".", "")
        if cutDots.isdigit() == False:
            raise validators.ValidationError(self.message)
        if float(field.data) < 0:
            raise validators.ValidationError(self.message)

class CheckPhoneNumber(object):
    def __init__(self, message=None):
        if not message:
            message = "This phone number cannot be processed."
        self.message = message

    def __call__(self, form, field):
        testForNums = field.data[:]
        testForNums = testForNums.replace("(", "")
        testForNums = testForNums.replace(")", "")
        testForNums = testForNums.replace("-", "")
        testForNums = testForNums.replace(" ", "")
        if testForNums.isdigit() == False:
            raise validators.ValidationError(self.message)


class MakeTripFormPOA(FlaskForm):
    # Ideally, you'd be able to display whether dates are valid without refreshing the page.
    # COMMENTED OUT: COORDINATOR NAME, COORDINATOR EMAIL, COORDINATOR PHONE, CAR CAPACITY
    # this info should cover all tables master, Trips
    # Test_Meme = SelectField("Test Select Field", [validators.DataRequired("Didn't work?")], choices=[("hi", "meme")])
    Trip_Name = StringField("Trip Name", [validators.DataRequired("Please name your trip")])
    # vvv REFORMAT THESE TWO THEY'RE REALLY BAD!!!
    Departure_Date = DateField("Departure Date", [validators.DataRequired("Please Enter Departure Date Fromat YYYY-MM-DD")])
    Return_Date = DateField("Return Date", [validators.DataRequired("Please Enter Return Date Fromat YYYY-MM-DD")])
    # Deatails Short this will be an indexed version of trip details
    # Post time will be automatically created with python DateTime Extension
    # Participant Num will be set to 1 when trip is created and then will be added to as the particpants table is updated
    # Particpant cap will be set by the car capacity field and updated as people add to the trip
    Trip_Location = StringField("Trip Location", [validators.DataRequired("Please enter your trips location")])
    Trip_State =StringField("Trip State", [validators.DataRequired("Please enter the state in which your trip will take place")])
    Details = StringField("Trip Details", [validators.DataRequired("Please enter a trip description")])
    #Coordinator_Name = StringField("Coordinator Name", [validators.DataRequired("please enter your name")])
    #Coordinator_Email = StringField("Coordinator Email", [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    #Coordinator_Phone = IntegerField("Coordinator Phone", [validators.DataRequired("Please enter your phone number as 7 Integers no other charecters")])
    GearList = StringField("Gear List", [validators.DataRequired("Please enter gear list if none enter none")])
    Trip_Meeting_Place =StringField("Trip Meeting Place", [validators.DataRequired("Please enter meeting place")])
    Additional_Cost = StringField("Additional Cost Estimate", [validators.DataRequired("Please enter a Number If your cost is 0 enter 0")])
    # Total cost is the amount of money that an individual on this trip will have to pay (like how much they'll likely spend on food, accommodations, etc).
    # Total cost will be computed using additional cost and the cost estiment from the trip location feild hopefully
    Cost_Breakdown = StringField('cost break down', [validators.DataRequired("Please enter What you will be spending money on if cost is zero enter NA")])
    # ^^^ Cost breakdown is an explanation of where each of the costs for the trip (that each individual will have to pay) come from.
    Car_Cap = IntegerField("Max number of cars on trip", [validators.DataRequired("Please enter Max num of Cars on trip")])
    Substance_Free = BooleanField("Substance Free")
    Driver = BooleanField("Driver")
    Car_Capacity = StringField("Number of spaces in your car", [validators.DataRequired("Please enter your car capacity if you dont have a car put 0"), CheckDigit()])
    # Weather Forcast will use weather API to get this assuming google maps passes us a location
    submit = SubmitField("Create Trip")
    #TODO: Obviously the participants fields will not be filled in however make sure that the HTML Reflects this
    # TODO: Add location validator

class AddToTripPOA(FlaskForm):
    # this form will handle all additions to the participants table
    # Participant = StringField("Name", [validators.DataRequired("We need to know who you are please fill in your name brah")])
    # Phone = IntegerField("Phone Number", [validators.DataRequired("So we can find you please fill in your phone number")])
    # Email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    Driver = BooleanField("Driver")
    Car_Capacity = StringField("Car Capacity", [validators.DataRequired("Please put car capacity if you aren't driving for this trip put 0"), CheckDigit()])
    submit = SubmitField("Add to Trip")

class EditTripMemberPOA(FlaskForm):
    Driver_Box = BooleanField("Driver")
    CarCapacity_Box = StringField("Car Capacity", [validators.DataRequired("Please put car capacity if you aren't driving for this trip put 0"), CheckDigit()])
    PotentialLeader_Box = BooleanField("In the event of a change of coordinators, are you willing to coordinate this trip?")
    submit = SubmitField("Confirm Changes")

class CreateAccountForm(FlaskForm):
    #Higher order memes.
    FirstName_Box = StringField("First Name", [validators.DataRequired("First Name Required")])
    LastName_Box = StringField("Last Name", [validators.DataRequired("Last Name Required")])
    Email_Box = StringField("Email", [validators.DataRequired("Email Required")])
    Age_Box = IntegerField("Age", [validators.DataRequired("Age Required")])
    Height_Box = IntegerField("Height (inches)", [validators.DataRequired("Height Required")])
    StudentIDNumber_Box = IntegerField("Student ID #", [validators.DataRequired("Student ID Number Required")])
    PhoneNumber_Box = StringField("Phone Number", [validators.DataRequired("Phone Number Required"), CheckPhoneNumber()])
    CarCapacity_Box = StringField("Car Capacity", [validators.DataRequired("Car Capacity Required"), CheckDigit()])
    submit = SubmitField("Create Account")
    # Is "DecimalField a thing?
    # Bad news! Car capacity cannot be set to zero for some reason!
    # Is this because IntegerField can only accept positive numbers? FIXED

class ModifyAccountForm(FlaskForm):
    FirstName_Box = StringField("First Name", [validators.DataRequired("First Name Required")])
    LastName_Box = StringField("Last Name", [validators.DataRequired("Last Name Required")])
    Email_Box = StringField("Email", [validators.DataRequired("Email Required")])
    Age_Box = IntegerField("Age", [validators.DataRequired("Age Required")])
    Height_Box = IntegerField("Height (inches)", [validators.DataRequired("Height Required")])
    StudentIDNumber_Box = IntegerField("Student ID #", [validators.DataRequired("Student ID Number Required")])
    PhoneNumber_Box = StringField("Phone Number", [validators.DataRequired("Phone Number Required"), CheckPhoneNumber()])
    CarCapacity_Box = StringField("Car Capacity", [validators.DataRequired("Car Capacity Required"), CheckDigit()])
    submit = SubmitField("Submit New Account Information")
    # Things to run over with Alasdair: How does the trip system work, and how can we incorporate user accounts into it?