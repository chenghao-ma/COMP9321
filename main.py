from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields, reqparse
from flask import request
from flask_cors import CORS, cross_origin
import pymongo
from bson.objectid import ObjectId
from localTest import *
import datetime
import json
from functools import wraps
import jwt
import pandas as pd
from preprossing import *
import os
import matplotlib.pyplot as matplt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["mydatabase"]
profile_collection = db["user_profile"]

class AuthenticationToken:
    def __init__(self,secret_key,expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in

    def generate_token(self,username):
        info = {
            'username':username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expires_in)
        }
        return jwt.encode(info, self.secret_key, algorithm='HS256')

    def validate_token(self,token):
        info = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        return info['username']

SECRET_KEY = "THIS IS THE SECRET KEY FOR COMP9321 ROUND TABLE."
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)


app = Flask(__name__)
api = Api(app, 
            authorizations={
                    'API-KEY':{
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
            security= 'API-KEY',
            default='COMP9321',
            version='1.0', 
            title='RoundTable API',
            description='A simple API for COMP9321',
          )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')
        try:
            user = auth.validate_token(token)
        except Exception as e:
            abort(401,e)
        return f(*args, **kwargs)
    return decorated


cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #sovle cors issue

app.config['CORS_HEADERS'] = 'Content-Type'

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        if username == 'admin' and password == 'admin':
            return {"token": auth.generate_token(username).decode('utf-8')}

        return {"message": "authorization has been refused for those credentials."}, 401

# csv_data = pd.read_csv("appstore_games.csv")
# auth = api.namespace('auth', description='Auth Section')
# @auth.route('/signup')
# class Signup(Resource):
#     signup_details = api.model('signup_details', {
#         'email': fields.String(required=True, example='roundtable@unsw.com'),
#         'password': fields.String(required=True, example='123456'),
#         'first_name': fields.String(required=True, example='Dahai'),
#         'last_name': fields.String(required=True, example='Pang'),
#     })
#     @auth.expect(signup_details)
#     @auth.response(200, 'Success')
#     @auth.response(403, 'Username Taken')
#     def post(self):
#         readData = request.json
#         getData = db.user_records.find_one({'email': readData['email']})
#         if getData:
#             return {'result': 'Username Taken'}, 403
#         insertData = {'email': readData['email'],
#                       'password': readData['password'],
#                       'first_name': readData['first_name'],
#                       'last_name': readData['last_name'],
#                       }
#         db.profile_collection.insert_one(insertData)
#         return {'result': readData}


# @auth.route('/login')
# class Login(Resource):
#     login_details = api.model('login_details', {
#         'email': fields.String(required=True, example='roundtable@unsw.edu.au'),
#         'password': fields.String(required=True, example='123456')
#     })
#     @auth.expect(login_details)
#     @auth.response(200, 'Success')
#     @auth.response(403, 'Invalid username or password')
#     def post(self):
#         readData = request.json
#         getData = db.profile_collection.find_one({'email': readData['email']})
#         if getData:
#             if readData['password'] == getData['password']:
#                 getData['_id'] = str(getData['_id'])
#                 return {'result': getData}
#             else:
#                 return {'result': 'Invalid email or password'}
#         else:
#             return {'result': 'Invalid email or password'}


# @auth.route('/login/changePassword/<string:user_id>')
# class changePassword(Resource):
#     pass_details = api.model('pass_details', {
#         'password': fields.String(required=True, example='123456')
#     })
#     @auth.expect(pass_details)
#     @auth.response(200, 'Success')
#     @auth.response(403, 'Error')
#     def put(self, user_id):
#         readData = request.json
#         getData = db.profile_collection.find_one({'_id': ObjectId(user_id)})
#         if getData:
#             updateData = {'password': readData['password']}
#             db.profile_collection.update_one(
#                 {'_id': ObjectId(user_id)},
#                 {'$set': updateData}
#             )
#             return {'result': 'Success'}
#         else:
#             return {'result': 'No such user'}

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
        if os.path.exists('frontend/src/views/Dashboard/avgUserRating.svg'):
            return {'result': 'avgUserRating has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/Dashboard/avgUserRating.svg')
            return {'result': 'avgUserRating success'}
@show.route('/countGeners')
class getImages(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        genres = pd.DataFrame({ 'category' : csv_data["Genres"]})
        category = {}
        for row in csv_data["Genres"]:
            cate_list = row.split(',')
            for i in cate_list:
                if i not in category:
                    category[i] = 1
                else:
                    category[i] += 1
        cleaned_category = {}
        for key in category:
            if category[key] > 500 :
                cleaned_category[key] = category[key]
        category = cleaned_category
        cate_list = sorted(category, key=category.get, reverse=True)
        cate_value = []
        cate_color = ["maroon","navy","orange","blue", "grey","purple","yellow","pink","brown","olive","cyan","magenta","limegreen","gold","darkkhaki"]

        for key in cate_list:
            cate_value.append(category[key])

        squarify.plot(sizes=cate_value, label=cate_list, alpha=.7, color=cate_color )
        matplt.axis('off')
        if os.path.exists('frontend/src/views/Dashboard/countGeners.svg'):
            return {'result': 'countGeners has been exported'}
        else:
            matplt.savefig('frontend/src/views/Dashboard/countGeners.svg')
            return {'result': 'countGeners success'}

@show.route('/category')
class getCategory(Resource):

    @show.response(200, 'Success')
    @show.response(403, 'Error')
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
        genres = pd.DataFrame({ 'category' : csv_data["Genres"]})
        category = {}
        for row in csv_data["Genres"]:
            cate_list = row.split(',')
            for i in cate_list:
                if i not in category:
                    category[i] = 1
                else:
                    category[i] += 1
        cleaned_category = {}
        
        # remains category which is larger than 100
        for key in category:
            if category[key] > 100 :
                cleaned_category[key] = category[key]
        category = cleaned_category
        # create dataframe for category
        data = pd.Series(category).reset_index(name='value').rename(columns={'index':'category'})

        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[20] + Category20c[3]
    #    data["value"] = data['value']
        
        # create figure for containing pie chart
        p = figure(plot_height=350, plot_width=750, title="Numbers of Different Genres", toolbar_location=None,
            tools="hover", tooltips="@category: @value")
            
        # create pie chart auto compute angle for each category
        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='category', source=data)
        p.output_backend = 'svg'
        if os.path.exists('frontend/src/views/Dashboard/categoryChart.svg'):
            return {'result': 'categoryChart has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/Dashboard/categoryChart.svg')
            return {'result': 'categoryChart success'}

@show.route('/dateVsAppSize')
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
        if os.path.exists('frontend/src/views/Dashboard/dateVsAppSize.svg'):
            return {'result': 'dateVsAppSize has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/Dashboard/dateVsAppSize.svg')
            return {'result': 'dateVsAppSize success'}



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
