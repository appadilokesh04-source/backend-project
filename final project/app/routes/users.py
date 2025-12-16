from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.schemas import UserCreate, UserOut, Token
from app.models.models import User
from app.utils.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.services import services
router = APIRouter(prefix="/api/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------
# REGISTER
# ---------------------------------------------------
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # username = email
    user = services.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = services.create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------------------------------------------------
# AUTH HELPERS
# ---------------------------------------------------
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def _get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #data = User.decode_token(token)
    from app.utils.security import decode_access_token
    data = decode_access_token(token)

    user = db.query(User).filter(User.id == data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

def admin_required(current_user: User = Depends(_get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user
