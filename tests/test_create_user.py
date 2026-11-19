import requests
import allure

from data.urls import Urls
from data.generate_user import GenerateUser

class TestCreateUser:
    @allure.title('Создание нового пользователя')
    @allure.description('Проверяем, что запрос отдает 200 и True при создании пользователя с валидными данными')
    def test_create_uniq_user(self):
        with allure.step('Подготовка данных для создании пользователя'):
            user_data = GenerateUser.generate_user() 
            payload = {
                "email": user_data["email"],
                "password": user_data["password"],
                "submitPassword": user_data["password"]
            }
        
        with allure.step('Проверка, что создали пользователя'):
            response = requests.post(Urls.SIGNUP_URL, json=payload)
            assert response.status_code == 201
            assert response.json()["user"]["email"] == user_data["email"]

    @allure.title('Создание пользователя с данными существующими в системе')
    @allure.description('Проверяем, что запрос отдает 400 и ошибку при создании пользователя с данными как у существующего пользователя в системе')
    def test_create_two_identical_user(self, register_new_user):
        with allure.step('Создание второго пользователя с такими же данными как первый пользователь'):
            payload = register_new_user
            response = requests.post(Urls.SIGNUP_URL, json=payload)
        
        with allure.step('Проверка, что пользователь с данными, которые уже есть в системе, не создается'):
            assert response.status_code == 400
            assert response.json()["message"] == 'Почта уже используется'
    