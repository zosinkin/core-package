from datetime import datetime, timedelta, UTC, timezone
from jose import JWTError, jwt
import bcrypt
from core.config import get_auth_data
from pydantic import BaseModel, EmailStr
from uuid import UUID

class TokenSchema(BaseModel):
    user_id: UUID
    email: EmailStr | None = None


async def check_password(plain_password, hashed_password: str) -> bool: 
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False
    

async def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def decode_jwt_token(token: str, secret_key: str, algorithm: str):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
    except JWTError:
        return None

    exp = payload.get("exp")
    if not exp:
       return None

    expire_time = datetime.fromtimestamp(int(exp), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None


    return TokenSchema(
        user_id=user_id,
        email=payload.get("email")
    )