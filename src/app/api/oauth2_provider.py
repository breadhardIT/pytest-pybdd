from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import settings
from app.repository.users_rest_repository import UsersRestRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # tokenUrl solo se usa si hay login

def create_users_repository():
    return UsersRestRepository(base_url=settings.users_base_url)

def get_current_user(token: str = Depends(oauth2_scheme),users_repository = Depends(create_users_repository)) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        if not users_repository.exists(user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
