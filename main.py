
from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import users, products, categories, orders
from app.middlewares.errors import register_exception_handlers
from app.middlewares.logging import setup_logging
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecuritySchemeType
from app.config.database import SessionLocal
from app.models.user import User
from fastapi.openapi.utils import get_openapi

from app.utils.hash import hash_password
from fastapi.openapi.utils import get_openapi

app = FastAPI(title='BabaFly API')

# create tables (for demo; in production use migrations)
Base.metadata.create_all(bind=engine)

# attach routers
app.include_router(users.router, prefix='/api/users', tags=['users'])
app.include_router(products.router, prefix='/api/products', tags=['products'])
app.include_router(categories.router, prefix='/api/categories', tags=['categories'])
app.include_router(orders.router, prefix='/api/orders', tags=['orders'])

# setup logging and exception handlers
setup_logging(app)
register_exception_handlers(app)

@app.get('/ping')
def ping():
    return {'pong': True}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")




def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        new_admin = User(
            email="admin@example.com",
            hashed_password=hash_password("password"),
            is_admin=True
        )
        db.add(new_admin)
        db.commit()
        print(" Admin created: admin@example.com / password")
    else:
        print("Admin already exists")
    db.close()

create_default_admin()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BabaFly API",
        version="1.0.0",
        description="Backend for BabaFly platform",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    openapi_schema["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
