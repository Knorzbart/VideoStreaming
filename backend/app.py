from flask import Flask, request, jsonify
from pymongo import MongoClient
from keycloak import KeycloakOpenID
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://mongo:27017/')
db = client.auth_db
users_col = db.users

# Keycloak configuration
keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/",
    realm_name="myrealm",
    client_id="myclient",
)

@app.route('/api/users', methods=['POST'])
def save_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'error': 'missing token'}), 401
    try:
        user_info = keycloak_openid.userinfo(token)
    except Exception:
        return jsonify({'error': 'invalid token'}), 401

    username = user_info.get('preferred_username')
    users_col.update_one({'username': username}, {'$set': user_info}, upsert=True)
    return jsonify({'status': 'saved', 'username': username})

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
