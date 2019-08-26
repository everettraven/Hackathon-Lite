from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (JWTManager, jwt_required, 
    create_access_token, get_jwt_identity)
from API_Models.models import *
from flask_cors import CORS
import requests
from datetime import *
from dateutil import parser
from API.reminder import sendEmail
from pytz import utc

base_request_url = "https://canvas.instructure.com/api/v1/"


#set the database url
db_url = "sqlite:////tmp/temp.db"

#Create the flask application
app = Flask(__name__)
CORS(app)

#Set the config properties of the application
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['JWT_SECRET_KEY'] = "Hackathon-Lite"

#set up the JWT manager
JWTManager(app)

#set up the database
db.app = app
db.init_app(app)
db.create_all()

current_date = datetime.now().astimezone(utc)


@app.route("/user/register", methods=['POST'])
def register():
    if not request.json:
        return jsonify(error="Please send json data as your request"), 400
    
    data = request.json


    if ("username" not in data) or ("password" not in data) or ("access_token" not in data):
        return jsonify(error="Missing vital data to create a user for this application"), 400
    
    if "phone" in data:
        user = User(data["username"], data["password"], data["access_token"], data["phone"], True)
    else:
        user = User(data["username"], data["password"], data["access_token"])

    db.session.add(user)
    db.session.commit()

    return jsonify(msg="User successfully created."), 200

@app.route("/user/login", methods=['POST'])
def login():
    if not request.json:
        return jsonify(error="Please make a json body request with the data"), 400
    
    data = request.json

    if ("username" not in data) or ("password" not in data):
        return jsonify(error="Please specify the username and password of the user you would like to login as"), 400
    

    user = User.query.filter(User.username == data["username"], User.password == data["password"]).first()

    auth_token = create_access_token(identity=user.id, expires_delta=False)

    return jsonify(access_token=auth_token), 200

@app.route("/user/data", methods=['GET'])
@jwt_required
def data():
    user_courses = []
    cur_identity = get_jwt_identity()
    user = User.query.filter(User.id == cur_identity).first()

    assignment_due_count = 0
    message = "Canvas Alert! \n\n"

    #get the user's courses
    course_request = requests.get(base_request_url + "courses", headers={'Authorization': "Bearer " + user.access_token})

    course_request_data = course_request.json()


    for i in range(len(course_request_data)):
        if "name" in course_request_data[i]:

            course = Course(course_request_data[i]["id"], course_request_data[i]["name"], course_request_data[i]["course_code"])
            
            assignment_request = requests.get(base_request_url + "courses/" + str(course.course_id) + "/assignments", headers={'Authorization': "Bearer " + user.access_token})

            assignment_data = assignment_request.json()


            for j in range(len(assignment_data)):
                due_date = parser.parse(assignment_data[j]["due_at"])
                if due_date.date() < datetime.today().date():
                    assignment = Assignment(assignment_data[j]["id"], assignment_data[j]["name"], assignment_data[j]["description"], assignment_data[j]["due_at"])
                    course.assignments.append(assignment)
                
                if (due_date - current_date).days < 3:
                    assignment_due_count += 1

            user_courses.append(course)

    message += "You have {} assignments due in 2 days! Make sure you get them done!".format(assignment_due_count)

    sendEmail(user.username, message)

    return jsonify([e.serialize() for e in user_courses]), 200



