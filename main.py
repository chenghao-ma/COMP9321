from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask import request
import pymongo
from bson.objectid import ObjectId
from localTest import *
import time
import pandas as pd
import preprossing
from preprossing import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
database = myclient["mydatabase"]
profile_collection = database["user_profile"]


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
                      }
        database.profile_collection.insert_one(insertData)
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

predict = api.namespace('predict', description='predict Section')
@predict.route('/predict')
class predict(Resource):

    @predict.response(200, 'Success')
    @predict.response(403, 'Error')
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

show = api.namespace('show', description='dataset presentation')
def avgUserRating():
    return
    
@show.route('/averageUserrating')
class getMeans(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        return "<div>%s</div>".format(avgUserRating(csv_data))
    
@show.route('/dataSize')
class getImages(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        return "<div>%s</div>".format(dateVsAppSize(csv_data))


@show.route('/category')
class getCategory(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        return "<div>%s</div>".format(computeUniq(csv_data))

@show.route('/Genres')
class getCount(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        return "<div>%s</div>".format(categoryChart(csv_data))


@show.route('/GetTopTen')
class getTopTen(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        return jsonify({"result" :getTopTen(csv_data)})



if __name__ == '__main__':
    app.run(debug=True)
