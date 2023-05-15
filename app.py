from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db = SQLAlchemy(app)

ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    nationality = db.Column(db.String)


    def __init__(self, first_name, last_name, date_of_birth, nationality):
        self.first_name=first_name
        self.last_name=last_name
        self.date_of_birth=date_of_birth
        self.nationality=nationality

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'nationality')

user_schema=UserSchema()
users_schema=UserSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():

    first_name=request.json['first_name']
    last_name = request.json['last_name']
    date_of_birth = request.json['date_of_birth']
    nationality = request.json['nationality']

    new_user = User(first_name, last_name, date_of_birth, nationality)

    db.session.add(new_user)

    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_users():
    users=User.query.all()
    result=users_schema.dump(users)
    return jsonify(result)

@app.route('/user/<int:id>', methods=['PUT', 'DELETE'])
def put_delete():
    if request.method=='PUT':
        user=User.query.all(id)
        user.first_name=request.json['first_name']
        user.last_name=request.json['last_name']
        user.date_of_birth=request.json['date_of_birth']
        user.nationality=request.json['nationality']

        db.session.commit()
        return {'message':'data updated'}


    if request.method=='DELETE':
        user=User.query.all(id)
        db.session.delete(user)
        db.session.commit()
        return {'message':'data deleted successfully'}


if __name__ == '__main__':
    app.run(debug=True)