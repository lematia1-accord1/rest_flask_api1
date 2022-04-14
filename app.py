# import required packages
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import delete
# inti the app
app = Flask(__name__)
# Database for sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# initialize Database
db = SQLAlchemy(app)

# initialize marshmallow

ma = Marshmallow(app)

# inializing the api
api = Api(app)
# Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    nationality = db.Column(db.String)
    def __init__(self, first_name, last_name, date_of_birth, nationality):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.nationality = nationality
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name','last_name', 'date_of_birth','nationality')
# inialize schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# create class to handle requests
class UserGetPost(Resource):
    def post(self):
        # instantiate a new user
        new_user = User(first_name=request.json['first_name'], last_name=request.json['last_name'], 
        date_of_birth=request.json['date_of_birth'], nationality=request.json['nationality'])
        # add new user
        db.session.add(new_user)
        # commit the change to reflect in database
        db.session.commit()
        # Return the response
        return user_schema.jsonify(new_user)
    def get(self):
        # get users from database
        users = User.query.all()
        #Return the list of users
        return jsonify(users_schema.dump(users))



class UserPutDelete(Resource):
    def put(self,id):
        # get User
        user = User.query.get(id)
        # Update user data
        user.first_name = request.json(['first_name'])
        user.last_name = request.json(['last_name'])
        user.date_of_birth = request.json(['date_of_birth'])
        user.nationality = request.json(['nationality'])
        # Commit to changes in database
        db.session.commit()
        return {'message' : 'data updated'}

    def delete(self, id):
        # get user
        user = User.query.get(id)
        # Delete user
        db.session.delete(user)
        # Commit to reflect in database
        db.session.commit()
        return {'massage' : 'data deleted sucessfully'}


# Bind the classes with routes
api.add_resource(UserGetPost, '/user')
api.add_resource(UserPutDelete, '/user/<int:id>')

# Run server
if__name__= '__main__'
app.run(debug=True)