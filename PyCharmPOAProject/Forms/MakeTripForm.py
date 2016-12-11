from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField,validators


class MakeTripForm(FlaskForm):
    # this info should cover all tables master, Trips, particpants
    Trip_Name = StringField("Trip Name", [validators.DataRequired("Please name your trip")])
    Departure_Date = DateField("Departure Data", [validators.DataRequired("Please Enter Departure Date")])
    Return_Date = DateField("Return Data", [validators.DataRequired("Please Enter Departure Date")])
    # Deatails Short this will be an indexed version of trip details
    # Post time will be automaticly created with python DateTime Extention
    # Participant Num will be set to 1 when trip is created and then will be added to as the particpants table is updated
    # Particpant cap will be set by the car capacity feild and updated as people add to the trip
    Trip_Location = StringField("Trip Location", [validators.DataRequired("Please enter your trips location")])
    Details = StringField("Trip Details", [validators.DataRequired("Please enter a trip discription")])
    Coordinator_Name = StringField("Coordinator Name", [validators.DataRequired("please enter your name")])
    Coordinator_Email = StringField("Coordinator Email", [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    Coordinator_Phone = IntegerField("Coordinator Phone", [validators.DataRequired("Please enter your phone number")])
    GearList = StringField("Gear List", [validators.DataRequired("Please enter gear list if none enter none")])
    Trip_Meeting_Place =StringField("Trip Meeting Place", [validators.DataRequired("Please enter meeting place")])
    Additional_Cost = StringField("Additional Cost Estimate")#condsider adding validator
    # Total cost will be computed using additional cost and the cost estiment from the trip location feild hopefully
    Cost_Breakdown = StringField('cost break down')
    Car_Cap = IntegerField("Max number of cars on trip", [validators.DataRequired("Please enter Max num of Cars on trip")])
    Substance_Free = BooleanField("Substance Free", [validators.DataRequired("You gonna do drugs???")])
    # Weather Forcast will use weather API to get this assuming google maps passes us a location
    submit = SubmitField("Create Trip")
    #TODO: Obviously the participants feilds will not be filled in however make sure that the HTML Reflects this