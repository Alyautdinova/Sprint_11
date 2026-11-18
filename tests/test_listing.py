import pytest
import requests
import allure

from requests_toolbelt import MultipartEncoder
from data.urls import Urls
from data.listning_data import LISTING_DATA, UPDATE_LISTING_DATA

class TestListing:
    @allure.title('Создание объявления')
    @allure.description('Проверяем, что объявление создается с кодом 201 и возвращает корректные данные')
    def test_create_listing(self, login_user):
        with allure.step('Подготовка данных для создания объявления'):
            encoder = MultipartEncoder(fields=LISTING_DATA)

            headers = {
                "Authorization": f"Bearer {login_user}",
                "Content-Type": encoder.content_type
            }

        with allure.step('Создание объявления'):
            response = requests.post(Urls.CREATE_LISTING_URL, headers=headers, data=encoder)

        with allure.step('Проверка, что объявление создано'):
            assert response.status_code == 201

            response_json = response.json()
            
            for key, expected_value in LISTING_DATA.items():
                assert str(response_json[key]) == str(expected_value)

    @allure.title('Успешное редактирование объявления')
    @allure.description('Проверяем, что можно изменить любое поле объявления')
    def test_update_listing(self, login_user, create_listing):
        with allure.step('Создание объявления'):
            offer_id = create_listing
            update_url = Urls.get_update_offer_url(offer_id)

        with allure.step('Подготовка данных для редактирования объявления'):
            encoder = MultipartEncoder(fields=UPDATE_LISTING_DATA)
            headers = {
                "Authorization": f"Bearer {login_user}",
                "Content-Type": encoder.content_type
            }

        with allure.step('Редактирование объявления'):
            response = requests.patch(update_url, headers=headers, data=encoder)
        
    
        with allure.step('Проверка, что объявление отредактировано'):
            assert response.status_code == 200
            
        with allure.step('Проверка обновленных данных'):
            response_json = response.json()
            for key, expected_value in UPDATE_LISTING_DATA.items():
                # Пропускаем img1/img2/img3
                if key.startswith("img"):
                    continue 
                assert str(response_json[key]) == str(expected_value)

    @allure.title('Редактирование чужого объявления')
    @allure.description('Проверяем, что нельзя редактировать объявление, созданное другим пользователем')
    def test_update_foreign_listing(self, create_listing, second_user_token):
        with allure.step('Создание объявления первым юзером'):
            offer_id = create_listing
            update_url = Urls.get_update_offer_url(offer_id)
        
        with allure.step('Подготовка данных для редактирования объявления'):
            encoder = MultipartEncoder(fields=UPDATE_LISTING_DATA)

        with allure.step('Используем токен второго пользователя'):
            headers = {
                "Authorization": f"Bearer {second_user_token}",
                "Content-Type": encoder.content_type
            }
        
        with allure.step('Редактирование вторым юзером объявления, созданного первым юзером'):
            response = requests.patch(update_url, headers=headers, data=encoder)
        
        with allure.step('Проверка, что объявление не отредактировано'):
            assert response.status_code == 401
            assert response.json()["message"] == 'Оффер не найден или у вас нет прав на его редактирование'

    @allure.title('Успешное удаление объявления')
    @allure.description('Проверяем, что можно удалить объявление')
    def test_delete_listing(self, login_user, create_listing):
        with allure.step('Создание объявления'):
            offer_id = create_listing
            delete_url = Urls.get_delete_offer_url(offer_id)
            headers = {
                "Authorization": f"Bearer {login_user}"
            }

        with allure.step('Удаление объявления'):
            response = requests.delete(delete_url, headers=headers)
        
        with allure.step('Проверка, что объявление удалено'):
            assert response.status_code == 200
            assert response.json()["message"] == "Объявление удалено успешно"
    