from rest_framework_jwt.settings import api_settings
from datetime import datetime
import uuid
import calendar

def jwt_payload_handler(user):
    payload = {
    'user_id': user.pk,
    'username': user.email,
    'pwd': user.password[-10:],
    'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
   
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = calendar.timegm(
            datetime.utcnow().utctimetuple()
        )
    return payload

