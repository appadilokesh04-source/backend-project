
import pytest
from fastapi.testclient import TestClient
from main import app
from app.config.database import Base, engine, SessionLocal
from app.services.user_service import create_user

client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def setup_db():
    # recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # create an admin user
    db = SessionLocal()
    create_user(db, 'admin@example.com', 'password', is_admin=True)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_login_and_profile():
    resp = client.post('/api/users/register', json={'email':'user1@example.com','password':'password'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['email'] == 'user1@example.com'

    resp2 = client.post('/api/users/login', json={'email':'user1@example.com','password':'password'})
    assert resp2.status_code == 200
    token = resp2.json()['access_token']
    assert token

    resp3 = client.get('/api/users/profile', headers={'Authorization': f'Bearer {token}'})
    assert resp3.status_code == 200
    assert resp3.json()['email'] == 'user1@example.com'

def test_create_and_fetch_product():
    # login admin
    resp = client.post('/api/users/login', json={'email':'admin@example.com','password':'password'})
    token = resp.json()['access_token']

    prod = {
        'name':'Ring',
        'description':'Gold ring',
        'price':100.0,
        'category_id': None
    }
    r = client.post('/api/products', json=prod, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 201
    pid = r.json()['id']

    r2 = client.get(f'/api/products/{pid}')
    assert r2.status_code == 200
    assert r2.json()['name'] == 'Ring'

def test_create_order():
    # register user and login
    client.post('/api/users/register', json={'email':'buyer@example.com','password':'password'})
    resp = client.post('/api/users/login', json={'email':'buyer@example.com','password':'password'})
    token = resp.json()['access_token']

    # create a product by admin
    resp_admin = client.post('/api/users/login', json={'email':'admin@example.com','password':'password'})
    admin_token = resp_admin.json()['access_token']
    prod = {'name':'Necklace','price':50.0,'category_id':None,'description':'','stock':10}
    r = client.post('/api/products', json=prod, headers={'Authorization': f'Bearer {admin_token}'})
    pid = r.json()['id']

    order = {'items':[{'product_id':pid,'quantity':1}],'address':'123 Street'}
    resp_order = client.post('/api/orders', json=order, headers={'Authorization': f'Bearer {token}'})
    assert resp_order.status_code == 200
    assert resp_order.json()['total_price'] == 50.0
