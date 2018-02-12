import os
from datetime import datetime
from functools import wraps
import json
import apiclient as google
import flask
import httplib2
from flask import request, redirect, url_for, \
    render_template, flash, Blueprint, session
from oauth2client import client

from DatabaseConnection.DataBaseSchema import db, \
    Master, Participants, Trips, Account
from Forms.POAForms import CreateAccountForm, ModifyAccountForm
from Pitzer_Outdoor_Adventure.Main.controllerHelperMethods import calculateProgress_carRatio, \
    calculateProgress_participantRatio

main = Blueprint('main', __name__, template_folder='templates')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'credentials' not in flask.session or 'Googledata' not in flask.session:
            return redirect(url_for('main.login'))
        elif None == Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first():
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods=['GET', 'POST'])
def mainPage():
    """
    The main page of the website.
    :return: 
    """
    masters = Master.query.checkTrip()
    formatMaster = [masters[x:x+3] for x in range(0, len(masters), 3)]
    print(formatMaster)
    return render_template("HomePage.html", entries=formatMaster)


@main.route("/trips/<int:TripKey>")
def tripPage(TripKey):
    """
    Finds a specific trip and displays it on screen.
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    # FINISHED: MAKE YOUR METERBARS AND JOIN TRIP BUTTON IN A SIDEBAR TOGETHER! This would look really cool.
    meta = Master.query.filter_by(id=TripKey).first()  # Returns a 1 element list lets get the object from that
    tripDetails = Trips.query.filter_by(Master_Key=TripKey).first()
    participantInfo = Participants.query.filter_by(Master_Key=TripKey).all()
    coordinator = Participants.query.filter_by(Master_Key=TripKey, Leader=True).first()
    costs = json.loads(tripDetails.Costs)#  converts string to dict
    costs.pop("POAGasCost", None)#  removes POAGasCost from dict
    print(costs)
    if 'credentials' in flask.session and 'Googledata' in flask.session:
        userID = flask.session['Googledata']['id'][:]
    else:
        userID = ''
    onTrip = False
    for those in participantInfo:
        if those.accountID == userID:
            onTrip = True
    # Check whether the current user, if they're logged in, is a coordinator.
    if coordinator is not None and coordinator.accountID == userID:
        youAreCoordinator = True
    else:
        youAreCoordinator = False

    # Below calculates how much of progress bar should be rendered for car and participant bars respectively
    participantRatio = calculateProgress_participantRatio(meta)
    carRatio = calculateProgress_carRatio(meta)
    return render_template("TripPage.html", Tripinfo=tripDetails, TripMeta=meta, Coordinator=coordinator,
                           ParticipantInfo=participantInfo, participantRatio=participantRatio, carRatio=carRatio,
                           userID=userID, onTrip=onTrip, youAreCoordinator=youAreCoordinator,costs=costs)


@main.route('/login', methods=['POST', 'GET'])
def login():
    """
    Retrieves the user's data from Google through gCallback, then has the user either make an account or go to the main page.
    :return: 
    """
    if 'credentials' not in flask.session:  # Are they already authenticated? If not, then go to authentication.
        return flask.redirect(flask.url_for('main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:  # If the access token is expired, ask them to re-authenticate.
        return flask.redirect(flask.url_for('main.gCallback'))
    else:  # If authenticated, get user info.
        http_auth = credentials.authorize(httplib2.Http())
        service = google.discovery.build('oauth2', 'v2', http_auth)  # We ask for their profile information.
        userinfo = service.userinfo().get().execute()  # Execute request.
        # print(userinfo)

        # populate form with google data
        flask.session['Googledata'] = userinfo
        # print(flask.session)
        # return rendertemplate(create acoubt.html, form=form)
        # Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
        # if flask.session['Googledata']['id']==Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum:
        if None == Account.query.filter_by(id=flask.session['Googledata']['id']).first():
            return redirect(url_for('main.makeAccount'))
        else:
            return redirect(url_for('main.mainPage'))


@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """
    Dumps the user's Googledata and credentials.
    :return: 
    """
    flask.session.pop('Googledata', None)
    flask.session.pop('credentials', None)
    return redirect(url_for('main.mainPage'))


@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    """
    Directs the user to their profile page, where their account information is displayed.
    :return: 
    """
    # print(Account.query.filter_by(id=flask.session['Googledata']['id']).first().accessData()['picture'])
    tempTime = datetime.today()
    # print(tempTime.strftime('%B'))
    # https://docs.python.org/2/library/datetime.html#module-datetime
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    return render_template("ProfilePage.html", user=Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first(), time=tempTime)


@main.route('/createAccount', methods=['POST', 'GET'])
def makeAccount():
    """
    This constructs a new account from the user's information.
    :return: 
    """
    if 'credentials' not in flask.session or 'Googledata' not in flask.session:
        return redirect(url_for('main.mainPage'))
    if None != Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first():
        return redirect(url_for('main.mainPage'))
    else:
        form = CreateAccountForm(FirstName_Box=flask.session['Googledata']["given_name"][:], LastName_Box=flask.session['Googledata']["family_name"][:])
        # TODO: Remove Googledata from session if you can, but doing this isn't that important.
        if request.method == 'POST':
            if form.validate_on_submit() == False:
                return render_template("NewAccount.html", form=form)
            else:
                Account.query.createAccount(formData=form.data, session=session)
                return redirect(url_for('main.mainPage'))
        elif request.method == 'GET':
            return render_template("NewAccount.html", form=form)


@main.route('/gCallback')
def gCallback():
    """
    This handles authentication. Granted, we're not quite sure how... but it does.
    :return:
    """
    secret = os.path.join(main.root_path[:-29], 'secret/client_secret.json')  # access the secret file
    # the -29 changes path to POA Website rather than the path to mainPage
    flow = client.flow_from_clientsecrets(secret, scope='https://www.googleapis.com/auth/userinfo.profile',
                                          redirect_uri=flask.url_for('main.gCallback', _external=True))
    # ,include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()  # sends request to google which redirects user to sign in
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')  # we have received a token form a user
        credentials = flow.step2_exchange(auth_code)  # authenticate that token with google
        flask.session['credentials'] = credentials.to_json()  # we have authenticated the user
        return flask.redirect(flask.url_for('main.login'))  # once authenticated return to main page
