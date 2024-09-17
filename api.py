import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API библиотека к веб приложению Pet Friends"""

    BASE_URL = "https://petfriends.skillfactory.ru/api"

    def __init__(self):
        pass

    def get_api_key(self, email: str, passwd: str) -> tuple:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем."""
        headers = {'email': email, 'password': passwd}
        res = requests.get(f"{self.BASE_URL}/key", headers=headers)
        return self._handle_response(res)

    def get_list_of_pets(self, auth_key: dict, filter: str = "") -> tuple:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром."""
        headers = {'auth_key': auth_key['key']}
        params = {'filter': filter}
        res = requests.get(f"{self.BASE_URL}/pets", headers=headers, params=params)
        return self._handle_response(res)
        print(res)

    def add_new_pet_simple(self, auth_key: dict, name: str, animal_type: str, age: str) -> tuple:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца без фото."""
        data = MultipartEncoder(fields={"name": name, "animal_type": animal_type, "age": age, "pet_photo": ""})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(f"{self.BASE_URL}/create_pet_simple", headers=headers, data=data)
        return self._handle_response(res)

    def add_new_pet(self, auth_key: dict, name: str, animal_type: str, age: str, pet_photo: str) -> tuple:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца."""
        try:
            with open(pet_photo, 'rb') as photo:
                data = MultipartEncoder(
                    fields={
                        'name': name,
                        'animal_type': animal_type,
                        'age': age,
                        'pet_photo': (pet_photo, photo, 'image/jpeg')
                    })
                headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
                res = requests.post(f"{self.BASE_URL}/pets", headers=headers, data=data)
                return self._handle_response(res)
        except FileNotFoundError:
            return 404, "File not found"

    def add_pet_photo(self, auth_key: dict, pet_id: str, pet_photo: str) -> tuple:
        try:
            with open(pet_photo, 'rb') as photo:
                data = MultipartEncoder(
                    fields={'pet_id': pet_id, 'pet_photo': (pet_photo, photo, 'image/jpeg')})
                headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
                res = requests.post(f"{self.BASE_URL}/pets/set_photo/{pet_id}", headers=headers, data=data)
                return self._handle_response(res)
        except FileNotFoundError:
            return 404, "File not found"

    def delete_pet(self, auth_key: dict, pet_id: str) -> tuple:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении."""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(f"{self.BASE_URL}/pets/{pet_id}", headers=headers)
        return self._handle_response(res)

    def update_pet_info(self, auth_key: dict, pet_id: str, name: str, animal_type: str, age: str) -> tuple:
        """Метод отправляет запрос на сервер о обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца."""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'age': age, 'animal_type': animal_type}
        res = requests.put(f"{self.BASE_URL}/pets/{pet_id}", headers=headers, json=data)
        return self._handle_response(res)

    def _handle_response(self, res) -> tuple:
        """Обрабатывает ответ от сервера и возвращает статус и результат."""
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
