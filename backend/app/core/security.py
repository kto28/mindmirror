from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import get_settings

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

security_scheme = HTTPBearer()


def create_admin_token() -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": "admin", "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def verify_admin_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials, settings.jwt_secret, algorithms=[ALGORITHM]
        )
        sub: str = payload.get("sub", "")
        if sub != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not admin")
        return sub
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def verify_automation_secret(secret: str) -> bool:
    settings = get_settings()
    return secret == settings.automation_secret
