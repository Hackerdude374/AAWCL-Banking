from decimal import Decimal
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pyodbc
import json
import bcrypt
import re
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'CSC430AAWCLBank'
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

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

# Create a new user for signup
@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    Username = data.get('Username')
    Email = data.get('Email')
    Password = data.get('PasswordHash')
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM Users WHERE Email = ?', Email)
    email = cursor.fetchone()

    if user or email:
        return jsonify({'message': 'Username or Email Existed'}), 400

    if not validate_username(Username):
        return jsonify({'message': 'Username must be at least 8 characters(lower case, uppercase or digits) long'}), 400

    if not validate_email(Email):
        return jsonify({'message': 'Please enter valid email address'}), 400

    if not validate_password(Password):
        return jsonify({'message': 'Password must be at least 8 characters(lower case, uppercase or digits) long'}), 400

    if not all(key in data for key in ('Username', 'PasswordHash')):
        return jsonify({'error': 'Missing username or password'}), 400

    # Insert into database
    cursor.execute(
        'INSERT INTO Users (Username, PasswordHash, Email, FullName, CurrAddr, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?)',
        data['Username'], hash_password(Password), data['Email'], data['FullName'], data['CurrAddr'], data['PhoneNumber'])
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
        access_token = create_access_token(identity=user.UserID)
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

@app.route('/openaccount', methods=['POST'])
@jwt_required()
def open_account():
    try:
        data = request.json

        # Validate input data
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        required_fields = ['AccountType']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Generate a unique 16-digit AccountID
        account_number = str(uuid.uuid4().int)[:16]

        # Get the UserID from the JWT token
        user_id = get_jwt_identity()

        cursor.execute('SELECT * FROM Users WHERE UserID = ?', user_id)
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Extract account data
        account_type = data['AccountType']
        opening_date = datetime.now()
        acc_status = data.get('AccStatus', 'Active')  # Default to 'Active' if not provided

        cursor.execute('INSERT INTO Accounts (AccountNumber, UserID, AccountType, OpeningDate, AccStatus) VALUES (?, ?, ?, ?, ?)'
                   , account_number, int(user_id), account_type, opening_date, acc_status)
        conn.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/myaccounts', methods=['GET'])
@jwt_required()
def my_accounts():
    try:
        user_id = get_jwt_identity()
        cursor.execute('SELECT * FROM Accounts WHERE UserID = ?', user_id)
        accounts = cursor.fetchall()
        result_list = []
        for account in accounts:
            account_dict = dict(zip([column[0] for column in cursor.description], account))

            # Convert decimal values to float
            account_dict['Balance'] = float(account_dict['Balance'])

            # Convert datetime objects to ISO format string
            account_dict['OpeningDate'] = account_dict['OpeningDate'].isoformat()

            result_list.append(account_dict)
        json_result = json.dumps(result_list)
        return jsonify(json_result), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/transactions', methods=['POST'])
@jwt_required()
def make_transaction():
    try:
        data = request.json

        # Validate input data
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        required_fields = ['sender_account_number', 'recipient_account_number', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        sender_account_number = data['sender_account_number']
        recipient_account_number = data['recipient_account_number']
        amount = data['amount']

        # Verify sender's identity
        sender_id = get_jwt_identity()

        # Retrieve sender's and recipient's account details from database
        cursor.execute('SELECT * FROM Accounts WHERE UserID = ? AND AccountNumber = ?', sender_id, sender_account_number)
        sender_account = cursor.fetchone()
        cursor.execute('SELECT * FROM Accounts WHERE AccountNumber = ?', recipient_account_number)
        recipient_account = cursor.fetchone()

        if not sender_account or not recipient_account:
            return jsonify({'error': 'Invalid account numbers'}), 400

        if sender_account.Balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400

        # Update sender's and recipient's account balances
        cursor.execute('UPDATE Accounts SET Balance = Balance - ? WHERE AccountNumber = ? AND UserID = ?', amount, sender_account_number, sender_id)
        conn.commit()
        cursor.execute('UPDATE Accounts SET Balance = Balance + ? WHERE AccountNumber = ?', amount, recipient_account_number)
        conn.commit()

        # Record transaction history

        return jsonify({'message': 'Transaction successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/accounts/<account_number>/balance', methods=['GET'])
@jwt_required()
def get_account_balance(account_number):

    user_id = get_jwt_identity()

    cursor.execute('SELECT * FROM Users WHERE UserID = ?', user_id)
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cursor.execute('SELECT * FROM Accounts WHERE AccountNumber = ?', account_number)
    account = cursor.fetchone()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    cursor.execute('SELECT Balance FROM Accounts WHERE AccountNumber = ? AND UserID = ?', account_number, user_id)
    balance = cursor.fetchone()
    return jsonify({'balance': balance})

if __name__ == '__main__':
    app.run(debug=True)