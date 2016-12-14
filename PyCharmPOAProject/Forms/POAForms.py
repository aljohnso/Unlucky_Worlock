from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField,validators


class MakeTripFormPOA(FlaskForm):
    # this info should cover all tables master, Trips
    Trip_Name = StringField("Trip Name", [validators.DataRequired("Please name your trip")])
    Departure_Date = DateField("Departure Date", [validators.DataRequired("Please Enter Departure Date")])
    Return_Date = DateField("Return Date", [validators.DataRequired("Please Enter Return Date")])
    # Deatails Short this will be an indexed version of trip details
    # Post time will be automaticly created with python DateTime Extention
    # Participant Num will be set to 1 when trip is created and then will be added to as the particpants table is updated
    # Particpant cap will be set by the car capacity feild and updated as people add to the trip
    Trip_Location = StringField("Trip Location", [validators.DataRequired("Please enter your trips location")])
    Trip_State =StringField("Trip State", [validators.DataRequired("Please enter the state your trip will take place in")])
    Details = StringField("Trip Details", [validators.DataRequired("Please enter a trip discription")])
    Coordinator_Name = StringField("Coordinator Name", [validators.DataRequired("please enter your name")])
    Coordinator_Email = StringField("Coordinator Email", [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    Coordinator_Phone = IntegerField("Coordinator Phone", [validators.DataRequired("Please enter your phone number")])
    GearList = StringField("Gear List", [validators.DataRequired("Please enter gear list if none enter none")])
    Trip_Meeting_Place =StringField("Trip Meeting Place", [validators.DataRequired("Please enter meeting place")])
    Additional_Cost = IntegerField("Additional Cost Estimate")#condsider adding validator
    # Total cost will be computed using additional cost and the cost estiment from the trip location feild hopefully
    Cost_Breakdown = StringField('cost break down')
    Car_Cap = IntegerField("Max number of cars on trip", [validators.DataRequired("Please enter Max num of Cars on trip")])
    Car_Capacity = IntegerField("Number of spaces in your car", [validators.DataRequired("Please enter your car capacity if you dont have a car put 0")])
    Substance_Free = BooleanField("Substance Free")
    # Weather Forcast will use weather API to get this assuming google maps passes us a location
    submit = SubmitField("Create Trip")
    #TODO: Obviously the participants feilds will not be filled in however make sure that the HTML Reflects this
    # TODO: Add location validoator

class AddToTripPOA(FlaskForm):
    # this form will handle all additions to the particpants table
    Participant = StringField("Name", [validators.DataRequired("We need to know who you are please fill in your name brah")])
    Phone = IntegerField("Phone Number", [validators.DataRequired("So we can find you please fill in your phone number")])
    Driver = BooleanField("Driver")
    Car_Capacity = StringField("Car Capacity", [validators.DataRequired("Please put car capacity if you aren't driving for this trip put 0")])
