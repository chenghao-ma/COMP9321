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
from flask_cors import CORS, cross_origin

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["mydatabase"]
profile_collection = db["user_profile"]


app = Flask(__name__)
api = Api(app, version='1.0', title='RoundTable API',
          description='A simple API for COMP9321',
          )
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #sovle cors issue
auth = api.namespace('auth', description='Auth Section')
app.config['CORS_HEADERS'] = 'Content-Type'
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
        db.profile_collection.insert_one(insertData)
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
        getData = db.profile_collection.find_one({'email': readData['email']})
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
        getData = db.profile_collection.find_one({'_id': ObjectId(user_id)})
        if getData:
            updateData = {'password': readData['password']}
            db.profile_collection.update_one(
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
@show.route('/avgUserRating')
class avgUserRating(Resource):
    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        aur = csv_data['Average User Rating'].value_counts().sort_index()
        # create bokeh figure for containing bar chart
        p = figure(x_range=list(map(str,aur.index.values)), plot_height=250, title="Average User Rating", toolbar_location=None, tools = "")
        
        # create bar chart with x (rating 4.0 4.5...) and y (numbers)
        p.vbar(x=list(map(str,aur.index.values)),top=aur.values,width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start=0
        p.output_backend = 'svg'
        export_svgs(p, filename = "avgUserRating.svg")
        return {'result': 'success'}
    
# @show.route('/averageUserrating')
# class getMeans(Resource):

#     @show.response(200, 'Success')
#     @show.response(403, 'Error')
#     def get(self):
#         csv_data = pd.read_csv("appstore_games.csv")
#         # global csv_data
#         return "<div>%s</div>".format(avgUserRating(csv_data))
    
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

@show.route('/getGenre')
class getCount(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        csv_data['Original Release Date'] = pd.to_datetime(csv_data['Original Release Date'], format = '%d/%m/%Y')
        # just get column of Original Release Date
        date_size = pd.DataFrame({'size':csv_data['Size']})
        date_size = date_size.set_index(csv_data['Original Release Date'])
        date_size = date_size.sort_values(by=['Original Release Date'])
        date_size.head()
        
        # compute monthly number for each app
        monthly_size = date_size.resample('M').mean()
        tmp = date_size.resample('M')
        monthly_size['min'] = tmp.min()
        monthly_size['max'] = tmp.max()
        monthly_size.head()

        p = figure(x_axis_type='datetime',           
                plot_height=250, plot_width=750,
                title='Date vs App Size (Monthly)')
        p.line(y='size', x='Original Release Date', source=monthly_size, line_width=2, line_color='Green')
        p.output_backend = 'svg'
        export_svgs(p, filename = "dataVsAppSize.svg")
        return {'result': 'success'}


@show.route('/getTopTen')
class getTopTen(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        csv_data['User Rating Count'] = csv_data['User Rating Count'].fillna(0)
        csv_data['User Rating Count'] = csv_data['User Rating Count'].astype('int64')
        # sort by rating
        temp = csv_data.sort_values(['User Rating Count'], ascending=False)
        
        # pick specific columns
        final = temp.loc[:, ['Icon URL','Name', 'Genres', 'Price', 'Size', 'Average User Rating']]
        
        # pick top 10 rows
        final = final[:5]
        print(final)
        json_file = []
        for index,row in final.iterrows():
            print(row[1])
            json_file.append({
            "Icon URL" : row[0],
            "Name" : row[1],
            "Genres" : row["Genres"],
            "Price" : row["Price"],
            "App Size" : row["Size"],
            "Rating" : row["Average User Rating"]
            })
        print(json_file)
        # global csv_data
        return {"result" :json_file}



if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(debug=True)
