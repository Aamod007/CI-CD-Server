from flask import Blueprint, request, jsonify
from auth import register_user, login_user, jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    result, error = register_user(data['email'], data['password'])
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(result), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    result, error = login_user(data['email'], data['password'])
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify(result), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required
def me():
    from flask import g
    return jsonify({
        'user_id': g.user_id,
        'email': g.email
    }), 200
