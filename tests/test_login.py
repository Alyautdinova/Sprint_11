import requests
import allure

from data.urls import Urls

class TestLogin:

    @allure.title('Вход под существующим в системе пользователем')
    @allure.description('Проверяем, что запрос отдает 200 и accessToken пользователя при входе под существующим в системе пользователем')
    def test_login_success(self, register_new_user):
        with allure.step('Подготовка данных для входа пользователя'):
            user_data = register_new_user

            login_payload = {
                "email": user_data["email"],
                "password": user_data["password"]
            }

        with allure.step('Логин пользователем'):
            response = requests.post(Urls.SIGNIN_URL, json=login_payload)

        with allure.step('Проверка, что вошли под пользователем'):
            assert response.status_code == 201
            assert "access_token" in response.json()["token"]
    