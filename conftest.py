import requests
import pytest

from data.urls import Urls
from data.generate_user import GenerateUser
from requests_toolbelt import MultipartEncoder
from data.listning_data import LISTING_DATA

#  фикстура для создания пользователя
@pytest.fixture
def register_new_user():

    user_data = GenerateUser.generate_user() 
    payload = {
        "email": user_data["email"],
        "password": user_data["password"],
        "submitPassword": user_data["password"]
        }

    requests.post(Urls.SIGNUP_URL, json=payload)

    return payload

#  фикстура для логина пользователя
@pytest.fixture
def login_user(register_new_user):

    user_data = register_new_user
    
    payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    response = requests.post(Urls.SIGNIN_URL, json=payload)
    token = response.json()["token"]["access_token"]

    return token

#  фикстура для создания объявления
@pytest.fixture
def create_listing(login_user):
    encoder = MultipartEncoder(fields=LISTING_DATA)
    headers = {
        "Authorization": f"Bearer {login_user}",
        "Content-Type": encoder.content_type
    }
    
    response = requests.post(Urls.CREATE_LISTING_URL, headers=headers, data=encoder)
    
    return response.json()["id"]

#  фикстура для создания второго пользователя и логина
@pytest.fixture
def second_user_token():
    user_data = GenerateUser.generate_user()
    
    payload = {
        "email": user_data["email"],
        "password": user_data["password"],
        "submitPassword": user_data["password"]
    }
    
    requests.post(Urls.SIGNUP_URL, json=payload)
    
    response = requests.post(Urls.SIGNIN_URL, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    
    return response.json()["token"]["access_token"]
