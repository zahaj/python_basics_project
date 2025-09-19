"""
Handles all authentication and authorization logic.

This module is responsible for:
1. Password hashing and verification using passlib.
2. Creating and decoding JSON Web Tokens (JWTs) for authentication.
3. Providing a FastAPI dependency (`get_current_user`) to protect endpoints.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- Configuration ---
# In a real production application, this should be loaded from environment variables.
SECRET_KEY = "a_very_secret_key_that_should_be_in_an_env_var"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme: tells FastAPI where the client should go to get a token.
# The `tokenUrl="token"` means it will point to `/token` endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context using the Bcrypt algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Utilities ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password: The password as entered by the user.
        hashed_password: The password hash stored in the database.

    Returns:
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password.

    Args:
        password: The plain-text password to hash.

    Returns:
        The hashed password as a string.
    """
    return pwd_context.hash(password)

# --- JWT Utilities ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data: The data to encode in the token (payload). Must contain 'sub'.
        expires_delta: Optional timedelta for token expiration.

    Returns:
        The encoded JWT as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Security Dependency ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    FastAPI dependency to secure endpoints.

    This function is injected into protected endpoints. It does the following:
    1. Extracts the token from the `Authorization: Bearer <token>` header.
    2. Decodes and validates the JWT.
    3. Extracts the user identifier ('sub' claim) from the token payload.
    4. Returns the user's data.

    If the token is invalid or missing, it raises an HTTPException.

    Args:
        token: The bearer token from the request header.

    Returns:
        A dictionary containing the user's data (e.g., {"username": "testuser"}).
    """
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # In a real app, you would fetch the user from the database here
        # and return a full user object.
        return {"username": username}
    except JWTError:
        raise credentials_exception