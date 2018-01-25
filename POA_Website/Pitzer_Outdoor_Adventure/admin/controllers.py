# from Tests.protyping.UserAccounts import db, Account, databaseName, currentPath, createAccount
# from Tests.TestForms.SecondForms import CreateAccountForm
from functools import wraps
import flask, datetime, re, copy
from flask import request, redirect, url_for, \
    render_template, flash, Blueprint, jsonify

from DatabaseConnection.DataBaseSchema import db, \
    Master, Participants, TripModel, Account
from Forms.POAForms import MakeTripFormPOA, AddToTripPOA, EditTripMemberPOA
from Pitzer_Outdoor_Adventure.Main.controllers import login_required
from flask_mail import Message, Mail

admin = Blueprint('admin', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
        if tempUser.admin == 0:
            return "Invalid Access AAAAAAAAAĀ"
            # return redirect(url_for('admin.invalidAccess'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route("/commandCenter")
@login_required
@admin_required
def commandCenter():
    """
    Shows the options available to an admin.
    :return:
    """
    #listOfUsers = Account.query.all()
    #listOfTrips = Master.query.all()
    return render_template("CommandCenter.html")