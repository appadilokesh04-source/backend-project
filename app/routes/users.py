
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user import UserCreate, UserOut, Token
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.utils.jwt import create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer
from app.utils.hash import verify_password
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
auth_scheme = HTTPBearer()

@router.post('/register', response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = create_user(db, payload.email, payload.password)
    return user
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


#@router.post('/login', response_model=Token)
#def login(form_data: UserCreate, db: Session = Depends(get_db)):
 #   user = authenticate_user(db, form_data.email, form_data.password)
  #  if not user:
   #     raise HTTPException(status_code=401, detail='Invalid credentials')
    #token = create_access_token({'sub': str(user.id), 'email': user.email, 'is_admin': user.is_admin})
    #return {'access_token': token, 'token_type': 'bearer'}
    

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # <-- Extract token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    email = payload.get("sub")   # You store email here

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


#def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
 #   payload = decode_token(token)
  #  if not payload:
   #     raise HTTPException(status_code=401, detail='Invalid token')
    #user = db.query(__import__('app.models.user', fromlist=['User']).User).get(int(payload.get('sub')))
    #if not user:
     #   raise HTTPException(status_code=404, detail='User not found')
    #return user

@router.get('/profile', response_model=UserOut)
def profile(current_user = Depends(get_current_user)):
    return current_user
