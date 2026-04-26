# core/security.py
from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.src.session import get_db

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_access_token(sub: str, role: str) -> str:
    expire  = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRE)
    payload = {"sub": sub, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# core/deps.py — reusable role guards via Depends()
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2), db=Depends(get_db)):
    payload = decode_token(token)
    user    = await db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401, "Inactive or unknown user")
    return user

async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(403, "Admin access required")

async def require_trainer(current_user=Depends(get_current_user)):
    if current_user.role != RoleEnum.TRAINER:
        raise HTTPException(403, "Trainer access required")