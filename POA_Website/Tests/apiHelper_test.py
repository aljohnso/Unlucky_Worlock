import unittest, os, datetime, json
from copy import deepcopy
from flask_testing import TestCase
from POA_Website.Pitzer_Outdoor_Adventure import app
from POA_Website.DatabaseConnection.DatabaseQuery import Master_db_query
from POA_Website.Forms.POAForms import CreateAccountForm, ModifyAccountForm
from POA_Website.DatabaseConnection.DataBaseSchema import db, Master, Participants, TripModel, Trips, Account
from POA_Website.Tests.testGlobals import apiHelperInput, apiHelperExpected
from POA_Website.Pitzer_Outdoor_Adventure.api.ApiHelpers import build_POST_return
from flask import jsonify
class User_Accounts_Tests(TestCase):

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
        response = build_POST_return(apiHelperInput["user_AJ"])

        self.assertEqual(response, jsonify(status=200, action="account"))
        self.assertDictEqual(apiHelperExpected['expected_AJ'], Account.query.filter_by(id=apiHelperInput["user_AJ"]["payload"]['googleNum']).first().serailze)