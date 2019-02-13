from DatabaseConnection.DataBaseSchema import db, \
    Master, Trips, Participants, TripModel, Account
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

def build_GET_return(object, recordName="Unkown"):
    """
    :param object: A sqlalchemy object that has attribute serialize or if no object exsist for
            query then will be none and abort
    :param recordName: the name of the table that the object comes from
    :return: json response
    """
    if object is None:
        abort(404, message="Record doesn't exist of type: " + recordName)
    else:
        try:
            return jsonify(status=200, body=object.serialize, recordName=recordName)
        except:
            return jsonify(status=500, body=recordName + "failed to be serialized it most" +
                                                         " likely is lacking a serialization method"
                                                         , recordName=recordName)

def build_POST_return(object):
    """
    :param object: A json object to be made into a entry in the db
    :return: json object to be send to client
    """
    try:
        if object["meta"] == "account":
        # Check first what record type we are dealing with
            return False
        elif object["meta"] == "trip":
            return False
        elif object["meta"] == "participant":
            return False

    except KeyError:
        abort(404, message="Object is not formated correctly")

def createRecord(recordData, recordType):
    """
    :param recordData: payload from input object
    :param recordType: name of table to insert into
    :return: will create record
    """
    if recordType == "account":
        # Check first what record type we are dealing with
        return False
    elif recordType == "trip":
        return False
    elif recordType == "participant":
        return False

