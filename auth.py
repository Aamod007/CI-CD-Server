import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from config import JWT_SECRET, supabase

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        g.user_id = payload['user_id']
        g.email = payload['email']
        return f(*args, **kwargs)
    
    return decorated

def register_user(email, password):
    # Check if user exists
    existing = supabase.table('users').select('id').eq('email', email).execute()
    if existing.data:
        return None, 'User already exists'
    
    # Create user
    hashed = hash_password(password)
    result = supabase.table('users').insert({
        'email': email,
        'password_hash': hashed
    }).execute()
    
    if result.data:
        user = result.data[0]
        token = create_token(user['id'], email)
        return {'token': token, 'user_id': user['id']}, None
    
    return None, 'Failed to create user'

def login_user(email, password):
    result = supabase.table('users').select('*').eq('email', email).execute()
    
    if not result.data:
        return None, 'Invalid credentials'
    
    user = result.data[0]
    
    if not verify_password(password, user['password_hash']):
        return None, 'Invalid credentials'
    
    token = create_token(user['id'], email)
    return {'token': token, 'user_id': user['id']}, None
