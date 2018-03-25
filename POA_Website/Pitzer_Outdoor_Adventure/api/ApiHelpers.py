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
        abort(404, message="Record doesn't exist of type: "+ recordName)
    else:
        try:
            return jsonify(status=200, body=object.serialize, recordName=recordName)
        except:
            return jsonify(status=500, body=recordName + "failed to be serialized it most" +
                                                         " likley is lacking a seralization methdd"
                                                         , recordName=recordName)

