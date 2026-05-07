import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv() 

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("JWT_SECRET")
    expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", 5))

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username: str, is_admin: bool) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "exp": now + timedelta(minutes=self.expire_minutes),
            "iat": now,
            "sub": username,
            "is_admin": is_admin,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"], payload.get("is_admin", False)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен просрочен")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)