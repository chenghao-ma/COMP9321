from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask import request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import pandas as pd
import preprossing
from preprossing import *

app = Flask(__name__)
api = Api(app, version='1.0', title='RoundTable API',
          description='A simple API for COMP9321',
          )

auth = api.namespace('auth', description='Auth Section')

# csv_data = pd.read_csv("appstore_games.csv")

@auth.route('/signup')
class Signup(Resource):
    signup_details = api.model('signup_details', {
        'email': fields.String(required=True, example='roundtable@unsw.com'),
        'password': fields.String(required=True, example='123456'),
        'first_name': fields.String(required=True, example='Dahai'),
        'last_name': fields.String(required=True, example='Pang'),
        'wish_list': fields.List(fields.String)

    })
    @auth.expect(signup_details)
    @auth.response(200, 'Success')
    @auth.response(403, 'Username Taken')
    def post(self):
        readData = request.json
        getData = db.user_records.find_one({'email': readData['email']})
        if getData:
            return {'result': 'Username Taken'}, 403
        insertData = {'email': readData['email'],
                      'password': readData['password'],
                      'first_name': readData['first_name'],
                      'last_name': readData['last_name'],
                      'wish_list': []
                      }
        db.user_records.insert_one(insertData)
        return {'result': readData}


@auth.route('/login')
class Login(Resource):
    login_details = api.model('login_details', {
        'email': fields.String(required=True, example='roundtable@unsw.edu.au'),
        'password': fields.String(required=True, example='123456')
    })
    @auth.expect(login_details)
    @auth.response(200, 'Success')
    @auth.response(403, 'Invalid username or password')
    def post(self):
        readData = request.json
        getData = db.user_records.find_one({'email': readData['email']})
        if getData:
            if readData['password'] == getData['password']:
                getData['_id'] = str(getData['_id'])
                return {'result': getData}
            else:
                return {'result': 'Invalid email or password'}
        else:
            return {'result': 'Invalid email or password'}


@auth.route('/login/changePassword/<string:user_id>')
class changePassword(Resource):
    pass_details = api.model('pass_details', {
        'password': fields.String(required=True, example='123456')
    })
    @auth.expect(pass_details)
    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def put(self, user_id):
        readData = request.json
        getData = db.user_records.find_one({'_id': ObjectId(user_id)})
        if getData:
            updateData = {'password': readData['password']}
            db.user_records.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': updateData}
            )
            return {'result': 'Success'}
        else:
            return {'result': 'No such user'}

# @auth.route('/Dashboard')
#class Display(Resource):

def avgUserRating():
    return

@auth.route('/predict')
class predict(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def post(self):
        try:
            price = request.args.get("price")
            ageRating = request.args.get("ageRating")
            size = request.args.get("size")
            genres = request.args.get("genres")
            # return callPredict(price,ageRating,size,genres)
            return ml(price,ageRating,size,genres)
        except Exception as e:
            return e

@auth.route('/getTop')
class top(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        print(csv_data)
    
@auth.route('/averageUserrating')
class getMeans(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        print(csv_data)
    
@auth.route('/dataSize')
class getImages(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        print(csv_data)


@auth.route('/category')
class getCategory(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        print(csv_data)

@auth.route('/Genres')
class getCount(Resource):

    @auth.response(200, 'Success')
    @auth.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        print(csv_data)

    



if __name__ == '__main__':
    app.run(debug=True)
