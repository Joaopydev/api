
from flask import request, jsonify
from jwt import jwt
from functools import wraps
from app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401  # Unauthorized

        try:
            token_parts = token.split()
            if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
                raise ValueError('Token format is invalid')
            jwt_token = token_parts[1]
            data = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401  # Unauthorized
        except (jwt.InvalidTokenError, ValueError):
            return jsonify({'message': 'Token is invalid'}), 401  # Unauthorized

        return f(*args, **kwargs)
    return decorated