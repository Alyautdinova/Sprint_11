from faker import Faker

class GenerateUser:
    # метод генерации данных пользователя
    def generate_user():
        fake = Faker()

        # генерируем почту и пароль пользователя
        email = fake.email()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    
        generate_user = {
            "email": email,
            "password": password,
            }

        return generate_user