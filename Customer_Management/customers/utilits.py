import jwt
import datetime
from django.conf import settings

# Encode JWT tokens (both access and refresh)
def encode_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=5),  # Access token valid for 5 minutes
        'iat': datetime.datetime.now()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def encode_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),  # Refresh token valid for 7 days
        'iat': datetime.datetime.now()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

# Decode JWT tokens
def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
