
from datetime import datetime, timedelta
from jose import jwt, JWTError

#SECRET_KEY = "SECRET1234"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "SECRET"

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub") == "admin"
    except:
        return False
