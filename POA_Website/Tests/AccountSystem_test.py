import unittest, os, datetime, json
from copy import deepcopy
from flask_testing import TestCase
from Pitzer_Outdoor_Adventure import app
from DatabaseConnection.DatabaseQuery import Master_db_query
from Forms.POAForms import CreateAccountForm, ModifyAccountForm
from DatabaseConnection.DataBaseSchema import db, Master, Participants, TripModel, Trips, Account
from POA_Website.Tests.testGlobals import accountSystemExpected, accountSystemInputs

class User_Accounts_Tests(TestCase):

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/DataBase_Test_Scripts/testing.db'
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Account_Creation(self):
        """
        Asserts that the account creation process creates as many accounts as it is programmed to.
        """
        # Create all three test accounts.
        createAccount(json.dumps(accountSystemInputs['user_AJ']))
        createAccount(json.dumps(accountSystemInputs['user_MV']))
        createAccount(json.dumps(accountSystemInputs['user_MB']))

        # Assertions.
        self.assertTrue(len(Account.query.all())==3)

    def test_Information_Retrieval(self):
        """
        Asserts that the information in the created accounts is as expected.
        """
        # Create all three test accounts.
        createAccount(json.dumps(accountSystemInputs['user_AJ']))
        createAccount(json.dumps(accountSystemInputs['user_MV']))
        createAccount(json.dumps(accountSystemInputs['user_MB']))

        # Assertions.
        self.assertDictEqual(accountSystemExpected['expected_AJ'], Account.query.filter_by(id=accountSystemInputs['user_AJ']['googleNum']).first().accessData())
        self.assertDictEqual(accountSystemExpected['expected_MV'], Account.query.filter_by(id=accountSystemInputs['user_MV']['googleNum']).first().accessData())
        self.assertDictEqual(accountSystemExpected['expected_MB'], Account.query.filter_by(id=accountSystemInputs['user_MB']['googleNum']).first().accessData())

    def test_Form_Usage(self):
        """
        Asserts that accounts created via the CreateAccountForm form exist and can have their data accessed.
        """
        # Create all three forms, and use them to make three accounts.
        form = CreateAccountForm(FirstName_Box=accountSystemInputs['user_AJ']['firstName'][:], LastName_Box=accountSystemInputs['user_AJ']['lastName'][:], Email_Box=accountSystemInputs['user_AJ']['email'][:], Age_Box=accountSystemInputs['user_AJ']['age'][:], Height_Box=accountSystemInputs['user_AJ']['height'][:], StudentIDNumber_Box=accountSystemInputs['user_AJ']['studentIDNumber'][:], PhoneNumber_Box=accountSystemInputs['user_AJ']['phoneNumber'][:], CarCapacity_Box=accountSystemInputs['user_AJ']['carCapacity'][:])
        userinfo = {
            'googleNum': accountSystemInputs['user_AJ']['googleNum'][:],
            'picture': accountSystemInputs['user_AJ']['picture'][:],
            'username': str(form.data['FirstName_Box'][:] + ' ' + form.data['LastName_Box'][:]),
            'email': str(form.data['Email_Box'][:]),
            'firstName': str(form.data['FirstName_Box'][:]),
            'lastName': str(form.data['LastName_Box'][:]),
            'gender': 'TBD',  # form.data['Gender_Box'][:],
            'age': str(form.data['Age_Box'])[:],
            'height': str(form.data['Height_Box'])[:],
            'allergies': 'TBD',
            'dietRestrictions': 'TBD',
            'studentIDNumber': str(form.data['StudentIDNumber_Box'])[:],
            'phoneNumber': str(form.data['PhoneNumber_Box'])[:],
            'carCapacity': str(form.data['CarCapacity_Box'])[:],
            'locale': accountSystemInputs['user_AJ']['locale'][:]
        }
        createAccount(json.dumps(userinfo))
        #
        form = CreateAccountForm(FirstName_Box=accountSystemInputs['user_MV']['firstName'][:], LastName_Box=accountSystemInputs['user_MV']['lastName'][:], Email_Box=accountSystemInputs['user_MV']['email'][:], Age_Box=accountSystemInputs['user_MV']['age'][:], Height_Box=accountSystemInputs['user_MV']['height'][:], StudentIDNumber_Box=accountSystemInputs['user_MV']['studentIDNumber'][:], PhoneNumber_Box=accountSystemInputs['user_MV']['phoneNumber'][:], CarCapacity_Box=accountSystemInputs['user_MV']['carCapacity'][:])
        userinfo = {
            'googleNum': accountSystemInputs['user_MV']['googleNum'][:],
            'picture': accountSystemInputs['user_MV']['picture'][:],
            'username': str(form.data['FirstName_Box'][:] + ' ' + form.data['LastName_Box'][:]),
            'email': str(form.data['Email_Box'][:]),
            'firstName': str(form.data['FirstName_Box'][:]),
            'lastName': str(form.data['LastName_Box'][:]),
            'gender': 'TBD',  # form.data['Gender_Box'][:],
            'age': str(form.data['Age_Box'])[:],
            'height': str(form.data['Height_Box'])[:],
            'allergies': 'TBD',
            'dietRestrictions': 'TBD',
            'studentIDNumber': str(form.data['StudentIDNumber_Box'])[:],
            'phoneNumber': str(form.data['PhoneNumber_Box'])[:],
            'carCapacity': str(form.data['CarCapacity_Box'])[:],
            'locale': accountSystemInputs['user_MV']['locale'][:]
        }
        createAccount(json.dumps(userinfo))
        #
        form = CreateAccountForm(FirstName_Box=accountSystemInputs['user_MB']['firstName'][:], LastName_Box=accountSystemInputs['user_MB']['lastName'][:], Email_Box=accountSystemInputs['user_MB']['email'][:], Age_Box=accountSystemInputs['user_MB']['age'][:], Height_Box=accountSystemInputs['user_MB']['height'][:], StudentIDNumber_Box=accountSystemInputs['user_MB']['studentIDNumber'][:], PhoneNumber_Box=accountSystemInputs['user_MB']['phoneNumber'][:], CarCapacity_Box=accountSystemInputs['user_MB']['carCapacity'][:])
        userinfo = {
            'googleNum': accountSystemInputs['user_MB']['googleNum'][:],
            'picture': accountSystemInputs['user_MB']['picture'][:],
            'username': str(form.data['FirstName_Box'][:] + ' ' + form.data['LastName_Box'][:]),
            'email': str(form.data['Email_Box'][:]),
            'firstName': str(form.data['FirstName_Box'][:]),
            'lastName': str(form.data['LastName_Box'][:]),
            'gender': 'TBD',  # form.data['Gender_Box'][:],
            'age': str(form.data['Age_Box'])[:],
            'height': str(form.data['Height_Box'])[:],
            'allergies': 'TBD',
            'dietRestrictions': 'TBD',
            'studentIDNumber': str(form.data['StudentIDNumber_Box'])[:],
            'phoneNumber': str(form.data['PhoneNumber_Box'])[:],
            'carCapacity': str(form.data['CarCapacity_Box'])[:],
            'locale': accountSystemInputs['user_MB']['locale'][:]
        }
        createAccount(json.dumps(userinfo))

        # Assertions.
        self.assertTrue(len(Account.query.all())==3)
        self.assertDictEqual(accountSystemExpected['expected_AJ'], Account.query.filter_by(id=accountSystemInputs['user_AJ']['googleNum']).first().accessData())
        self.assertDictEqual(accountSystemExpected['expected_MV'], Account.query.filter_by(id=accountSystemInputs['user_MV']['googleNum']).first().accessData())
        self.assertDictEqual(accountSystemExpected['expected_MB'], Account.query.filter_by(id=accountSystemInputs['user_MB']['googleNum']).first().accessData())

    def test_Delete_Account(self):
        """
        TODO: Asserts that deleted accounts no longer exist in the database.
        """
        # Memes here.

if __name__ == '__main__':
    unittest.main()
