from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
import json


app = Flask(__name__)
CORS(app)
token = "dlashjdlkjsahkdljhasldkhsakdlaskhdjalshj";

# Connection parameters
server = 'aawcl.database.windows.net'
database = 'AAWCL'
username = 'aawcladmin'
password = 'CSC430server'

# Establish connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Create cursor
cursor = conn.cursor()

# Create a new user for signup
@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    Username = data.get('Username')
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    if user:
        return jsonify({'message': 'User Existed Already'}), 400

    if not all(key in data for key in ('Username', 'PasswordHash')):
        return jsonify({'error': 'Missing required fields'}), 400


    # Insert into database
    cursor.execute(
        'INSERT INTO Users (Username, PasswordHash, Email, FullName, CurrAddr, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?)',
        data['Username'], data['PasswordHash'], data.get('Email'), data.get('FullName'), data.get('CurrAddr'),
        data.get('PhoneNumber'))
    conn.commit()

    # Retrieve the auto-generated UserID
    cursor.execute('SELECT @@IDENTITY AS UserID')
    new_user_id = cursor.fetchone().UserID

    # Return the newly created user with UserID
    created_user = {'UserID': new_user_id, **data}

    return jsonify({'message': 'User created successfully', 'user': created_user}), 201

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

    if user.PasswordHash == Password:
        return jsonify({'message': 'Login successful', 'Token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

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
    cursor.execute('SELECT * FROM Users WHERE Username = ?', (Username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_dict = dict(zip([column[0] for column in cursor.description], user))
    json_result = json.dumps(user_dict)
    
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
@app.route('/users/<int:UserID>/password', methods=['PUT'])
def update_user_password(UserID):
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', UserID)
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    cursor.execute(
        'UPDATE Users SET Username = ?, PasswordHash = ? WHERE UserID = ?',
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