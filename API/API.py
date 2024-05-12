import random
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

def validate_phone_number(phone_number):
    # Regular expression to match phone numbers with optional country code
    pattern = re.compile(r'^(\+\d{1,3})?(\d{10})$')

    # Check if the phone number matches the pattern
    if pattern.match(phone_number):
        return True
    else:
        return False

# Create a new user for signup
@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    Username = data.get('Username')
    Email = data.get('Email')
    PhoneNumber = data.get('PhoneNumber')
    Password = data.get('PasswordHash')
    cursor.execute('SELECT * FROM Users WHERE Username = ?', Username)
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM Users WHERE Email = ?', Email)
    email = cursor.fetchone()
    cursor.execute('SELECT * FROM Users WHERE PhoneNumber = ?', PhoneNumber)
    phone = cursor.fetchone()

    if user or email or phone:
        return jsonify({'error': 'Username or Email or Phone Number Existed'}), 400

    if not validate_username(Username):
        return jsonify({'error': 'Username must be at least 8 characters(lower case, uppercase or digits) long'}), 401

    if not validate_password(Password):
        return jsonify({'error': 'Password must be at least 8 characters(lower case, uppercase or digits) long'}), 402

    if not validate_email(Email):
        return jsonify({'error': 'Please enter valid email address'}), 403

    if not validate_phone_number(PhoneNumber):
        return jsonify({'error': 'Please enter valid phone number'}), 404

    if not all(key in data for key in ('Username', 'PasswordHash')):
        return jsonify({'error': 'Missing username or password'}), 405

    # Insert into database
    cursor.execute(
        'INSERT INTO Users (Username, PasswordHash, Email, FullName, CurrAddr, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?)',
        data['Username'], hash_password(Password), data['Email'], data['FullName'], data['CurrentAddress'], data['PhoneNumber'])
    conn.commit()

    return jsonify({'message': 'User created successfully'}), 200

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
        required_field = 'AccountType'
        if required_field not in data:
            return jsonify({'error': f'Missing required field: {required_field}'}), 400

        # Generate a unique 16-digit Account Number
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
    user_id = get_jwt_identity()

    cursor.execute('SELECT * FROM Accounts WHERE UserID = ?', user_id)
    accounts = cursor.fetchall()
    result_list = []
    if not accounts:
        return jsonify({'error': 'no account exists'}), 400
    for account in accounts:
        account_dict = dict(zip([column[0] for column in cursor.description], account))

        # Convert decimal values to float
        account_dict['Balance'] = float(account_dict['Balance'])

        # Convert datetime objects to ISO format string
        account_dict['OpeningDate'] = account_dict['OpeningDate'].isoformat()

        result_list.append(account_dict)
    json_result = json.dumps(result_list)
    return jsonify(json_result), 200

@app.route('/changestatus', methods=['POST'])
@jwt_required()
def change_status():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    user_id = get_jwt_identity()
    account_number = data['AccountNumber']
    cursor.execute('SELECT * FROM Accounts WHERE UserID = ? AND AccountNumber = ?', user_id, account_number)
    account = cursor.fetchone()
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    cursor.execute('UPDATE Accounts SET AccStatus = ? WHERE AccountNumber = ?', data['AccountStatus'], data['AccountNumber'])
    conn.commit()
    return jsonify({'message': 'Account status updated successfully'}), 200

@app.route('/accoverview', methods=['GET'])
@jwt_required()
def accounts_overview():
    try:
        user_id = get_jwt_identity()

        cursor.execute('SELECT * FROM Accounts WHERE UserID = ?', user_id)
        accounts = cursor.fetchall()
        result_list = []
        if not accounts:
            return jsonify({'message': 'no account exists'}), 400
        for account in accounts:
            account_dict = {
                'AccountNumber': account[0],
                'AccountType': account[2],
                'Balance': float(account[3])
            }
            result_list.append(account_dict)
        json_result = json.dumps(result_list)
        return jsonify(json_result), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

def generate_transaction_id():
    return ''.join(random.choices('0123456789', k = random.randint(6,8)))

def generate_description(transaction_type, sender, recipient, amount):
    if transaction_type == 'transfer':
        description = f"Transfer from {sender} to {recipient}"
    elif transaction_type == 'deposit':
        description = f"Deposit to {recipient}"
    elif transaction_type == 'withdrawal':
        description = f"Witidrawal from {sender}"
    else:
        description = "UNKNOWN"

    description += f", Amount: {amount}"

    return {description}

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

        sender_account_number = int(data['sender_account_number'])
        recipient_account_number = int(data['recipient_account_number'])
        amount = float(data['amount'])

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
        transaction_type = 'transfer'
        transaction_id = int(generate_transaction_id())
        transaction_date = datetime.now()
        description = str(generate_description(transaction_type, sender_account_number, recipient_account_number, amount))
        cursor.execute(
            'INSERT INTO TransactionLogs (LogID, AccountNumber, Recipient, LogAction, Amount, LogTime, LogDesc) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (transaction_id, sender_account_number, recipient_account_number, transaction_type, amount, transaction_date, description))
        conn.commit()

        return jsonify({'message': 'Transaction successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs', methods=['POST'])
@jwt_required()
def get_log_history():
    try:
        data = request.json
        account_number = int(data['account_number'])
        cursor.execute('SELECT * FROM TransactionLogs WHERE AccountNumber = ?', (account_number,))
        logs = cursor.fetchall()
        if not logs:
            return jsonify({'error': 'No logs exist'}), 400

        history = []
        for log in logs:
            log_dict = dict(zip([column[0] for column in cursor.description], log))

            log_dict['Amount'] = float(log_dict['Amount'])

            log_dict['LogTime'] = log_dict['LogTime'].isoformat()

            history.append(log_dict)

        json_result = json.dumps(history)
        return jsonify(json_result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_expiration_date():
    # Get the current year
    current_year = datetime.now().year

    # Generate a random year between the current year and the next 10 years
    expiration_year = random.randint(current_year, current_year + 10)

    # Generate a random month
    expiration_month = random.randint(1, 12)

    # If the expiration month is February, limit the expiration day to 28
    if expiration_month == 2:
        expiration_day = random.randint(1, 28)
    # For other months, set the maximum day to 30 or 31 depending on the month
    elif expiration_month in [4, 6, 9, 11]:
        expiration_day = random.randint(1, 30)
    else:
        expiration_day = random.randint(1, 31)

    # Create a datetime object for the expiration date
    expiration_date = datetime(expiration_year, expiration_month, expiration_day)

    # Format the expiration date as MM/YYYY
    expiration_date_formatted = expiration_date.strftime("%m-%Y")

    return expiration_date_formatted

def generate_cvv():
    return ''.join(random.choices('0123456789', k=3))

@app.route('/opencard', methods=['POST'])
@jwt_required()
def open_card():
    data = request.json
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required_field = 'CardType'
    if required_field not in data:
        return jsonify({'error': f'Missing required field: {required_field}'}), 400

    # Generate a unique 16-digit Account Number
    card_number = str(uuid.uuid4().int)[:16]

    # Get the UserID from the JWT token
    user_id = get_jwt_identity()

    cursor.execute('SELECT * FROM Users WHERE UserID = ?', user_id)
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Extract account data
    card_holder = user[4]
    expiration = datetime.strptime(generate_expiration_date(), "%m-%Y")
    cvv = generate_cvv()
    card_type = data['CardType']
    opening_date = datetime.now()
    issued = "AAWCLBank"

    cursor.execute('INSERT INTO Creditcard (CardNumber, CardHolder, ExpirationDate, OpeningDate, Cvv, CardType, IssuedBy, UserID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                , card_number, card_holder, expiration, opening_date, cvv, card_type, issued, user_id)
    conn.commit()
    return jsonify({'message': 'Credit card created successfully'}), 201

@app.route('/mycards', methods=['GET'])
@jwt_required()
def my_cards():
    user_id = get_jwt_identity()
    cursor.execute('SELECT * FROM Users WHERE UserID = ?', user_id)
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cursor.execute('SELECT * FROM CreditCard WHERE UserID = ?', user_id)
    cards = cursor.fetchall()
    if not cards:
        return jsonify({'error': 'No cards exist'}), 404
    result_list = []
    for card in cards:
        card_dict = {
            'CardNumber': card[0],
            'CardHolder': card[1],
            'ExpirationDate': card[2],
            'Cvv': card[4],
            'CardType': card[5],
            'Balance': float(card[7]),
            'CardStatus': card[8]
        }
        result_list.append(card_dict)
    json_result = json.dumps(result_list)
    return jsonify(json_result), 200

if __name__ == '__main__':
    app.run(debug=True)
