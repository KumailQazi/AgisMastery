from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import hashlib
import json
import base64
import hmac
import warnings

# Suppress passlib bcrypt version inspection warning with newer bcrypt
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")

try:
    from jose import jwt
    USE_JOSE = True
except ImportError:
    USE_JOSE = False

from .config import settings

ALGORITHM = "HS256"

def verify_password(plain: str, hashed: str) -> bool:
    return hashed == hashlib.sha256((plain + settings.SECRET_KEY).encode()).hexdigest()

def get_password_hash(password: str) -> str:
    return hashlib.sha256((password + settings.SECRET_KEY).encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    if USE_JOSE:
        try:
            return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        except Exception:
            pass
    # Pure Python token generator
    payload_str = json.dumps(to_encode)
    sig = hmac.new(settings.SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
    token_bytes = base64.urlsafe_b64encode(f"{payload_str}::{sig}".encode())
    return token_bytes.decode()

def decode_token(token: str) -> dict:
    if USE_JOSE:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        except Exception:
            pass
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        payload_str, sig = raw.split("::", 1)
        expected_sig = hmac.new(settings.SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(sig, expected_sig):
            return json.loads(payload_str)
    except Exception:
        pass
    return {}
