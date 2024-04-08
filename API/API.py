from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pyodbc
import json
import bcrypt
import string
import secrets
import re

def generate_random_key(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

# Generate a 64-character random key
random_key = generate_random_key(64)

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = random_key
jwt = JWTManager(app)

# Connection parameters
server = 'aawcl.database.windows.net'
database = 'AAWCL'
username = 'aawcladmin'
password = 'CSC430server'

# Establish connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Create cursor
cursor = conn.cursor()

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_username(username):
    # Define the regex pattern for the password
    pattern = r'^[a-zA-Z0-9]{8,}$'

    # Check if the password matches the pattern
    if re.match(pattern, username):
        return True
    else:
        return False

def validate_password(password):
    # Define the regex pattern for the password
    pattern = r'^[a-zA-Z0-9]{8,}$'

    # Check if the password matches the pattern
    if re.match(pattern, password):
        return True
    else:
        return False

# Create a new user for signup
@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    Username = data.get('Username')
    Password = data.get('PasswordHash')
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    if user:
        return jsonify({'message': 'Username Existed'}), 400

    if not validate_username(Username):
        return jsonify({'message': 'Username must be at least 8 characters(lower case, uppercase or digits) long'}), 400

    if not validate_password(Password):
        return jsonify({'message': 'Password must be at least 8 characters(lower case, uppercase or digits) long'}), 400

    if not all(key in data for key in ('Username', 'PasswordHash')):
        return jsonify({'error': 'Missing username or password'}), 400

    # Insert into database
    cursor.execute(
        'INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)',
        data['Username'], hash_password(Password))
    conn.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Check for login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    Username = data.get('Username')
    Password = data.get('PasswordHash')
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    if not user:
        return jsonify({'message': 'User does not exist'}), 401

    if not Username or not Password:
        return jsonify({'message': 'Missing username or password'}), 400

    if verify_password(Password, user.PasswordHash):
        access_token = create_access_token(identity=Username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    result_list = []
    for user in users:
        result_list.append(dict(zip([column[0] for column in cursor.description], user)))
    json_result = json.dumps(result_list)
    return jsonify(json_result), 200

# Get user by Username
@app.route('/users/<string:Username>', methods=['GET'])
def get_user(Username):
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    user_dict = dict(zip([column[0] for column in cursor.description], user))
    json_result = json.dumps(user_dict)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': json_result}), 200

# Update user information by UserID
@app.route('/users/<int:UserID>', methods=['PUT'])
def update_user(UserID):
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', UserID)
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    cursor.execute(
        'UPDATE Users SET Email=?, FullName=?, CurrAddr=?, PhoneNumber=? WHERE UserID=?',
        data.get('Email'), data.get('FullName'), data.get('CurrAddr'),
        data.get('PhoneNumber'), UserID)
    conn.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# Update user username and password by UserID
@app.route('/users/<int:UserID>', methods=['PUT'])
def update_user_password(UserID):
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', UserID)
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    cursor.execute(
        'UPDATE Users SET Username = ?, PasswordHash = ?',
        data.get('Username'), data.get('PasswordHash'), UserID)
    conn.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# Delete user by UserID
@app.route('/users/<int:UserID>', methods=['DELETE'])
def delete_user(UserID):
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', UserID)
    user = cursor.fetchone()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    cursor.execute('DELETE FROM Users WHERE UserID = ?', UserID)
    conn.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)