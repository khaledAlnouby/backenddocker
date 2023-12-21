from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB configuration
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/clinic_reservation.users')
client = MongoClient(mongo_uri)
db = client.get_database()
users_collection = db.get_collection('users')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Check if the email already exists
    existing_user = users_collection.find_one({'email': data['email']})
    if existing_user:
        return jsonify({"msg": "User with this email already exists"}), 400

    new_user = {
        'email': data['email'],
        'password': data['password'],
        'userType': 'doctor' if data.get('isDoctor') else 'patient',
    }

    users_collection.insert_one(new_user)
    print("User inserted successfully")
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data:
        return jsonify({"msg": "Email not provided"}), 400

    user = users_collection.find_one({'email': data['email']})
    if user and user['password'] == data['password']:
        return jsonify({"msg": "Login successful", "userType": user.get('userType', 'patient')}), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
