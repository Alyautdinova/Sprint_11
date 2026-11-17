import requests
import pytest

from data.urls import Urls
from data.generate_user import GenerateUser

#  фикстура для создания пользователя
@pytest.fixture
def register_new_user():

    user_data = GenerateUser.generate_user() 
    payload = {
        "email": user_data["email"],
        "password": user_data["password"],
        "submitPassword": user_data["password"]
        }

    response = requests.post(Urls.SIGN_URL, json=payload)

    return {
        "payload": payload,
        "token": response.json().get("accessToken")
    }
