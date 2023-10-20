from fastapi import HTTPException
import jwt
import os

SECRET_KEY=os.environ.get('SECRET_KEY')

class AuthenticationService:
    def create_jwt_token(data: dict):
        return jwt.encode(data, SECRET_KEY, algorithm="HS256")


    def decode_jwt_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Token is invalid")