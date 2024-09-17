import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово 'key'."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_simple_data(name='Барон', animal_type='Мейн-кун', age='1'):
    """Проверяем, что можно добавить питомца с корректными данными."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200, f"Ошибка при добавлении питомца: {result}"
    assert result['name'] == name, "Имя питомца не совпадает с ожидаемым."
    print(result)


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='Мейн-кун', age='4',
                                     pet_photo='images/ONSGxeZ1kfU.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными и изображением."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    print(result)


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового
    if len(my_pets['pets']) == 0:
        status, result = pf.add_new_pet(auth_key, "Суперкот", "кот", "2", "images/мурка.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']  # изменено на 0, чтобы удалить первого питомца
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in [pet['id'] for pet in my_pets['pets']]


def test_successful_update_self_pet_info():
    """Проверяем возможность обновления информации о питомце"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что список питомцев не пустой
    assert len(my_pets['pets']) > 0
    pet_id = my_pets['pets'][0]['id']  # берём id первого питомца

    # Обновляем информацию о питомце
    new_name = "Обновлённый имя"
    new_animal_type = "кошачий"
    new_age = "3"
    status, result = pf.update_pet_info(auth_key, pet_id, new_name, new_animal_type, new_age)

    # Проверяем, что статус ответа равен 200 и данные обновлены
    assert status == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age


def test_add_new_pet_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    pet_photo_path = os.path.join(os.path.dirname(__file__), "images/мурка.jpg")
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo_path)

    if status != 200:
        print(
            f"Не удалось добавить нового питомца - Статус: {status}, Результат: {result}")  # Более информативная ошибка
    assert status == 200


def test_delete_pet():
    pf = PetFriends()
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 1:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "1", "images/ONSGxeZ1kfU.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_add_new_pet_with_empty_name():
    """Проверяем, что нет ошибки при добавлении питомца с пустым именем."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, "", "кот", "2", "images/ONSGxeZ1kfU.jpg")
    assert status == 200  # Ожидаем успешный код 200, если имя может быть пустым


def test_add_new_pet_with_empty_age():
    """Проверяем, что нельзя добавить питомца с пустым возрастом."""
    pet_photo = os.path.join(os.path.dirname(__file__), "images/мурка.jpg")
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, "Барон", "кот", "", "images/мурка.jpg")
    assert status != 200  # Ожидаем неуспех


def test_get_api_key_with_invalid_credentials():
    """Проверяем, что запрос api ключа с неверными данными возвращает статус 403 и сообщение об ошибке."""
    invalid_email = "invalid_email@example.com"
    invalid_password = "invalid_password"
    status, result = pf.get_api_key(invalid_email, invalid_password)

    assert status == 403  # Ожидаем статус 401 для неверных учетных данных.
    assert "error" in result  # Ожидаем, что ответ содержит информацию об ошибке.


def test_get_all_pets_with_missing_key():
    """Проверяем, что запрос всех питомцев без ключа возвращает ошибку."""
    filter = ''
    status, result = pf.get_list_of_pets("", filter)
    assert status != 200  # Ожидаем неуспех


def test_delete_pet_with_invalid_id():
    """Проверяем, что запрос на удаление питомца с неверным идентификатором возвращает статус 404."""
    invalid_pet_id = "invalid_id"
    status, result = pf.delete_pet(invalid_pet_id)

    assert status == 404  # Ожидаем статус 404, если питомец не найден.
    assert "error" in result  # Ожидаем, что ответ содержит информацию об ошибке.


def test_get_pet_info_for_nonexistent_pet():
    """Проверяем, что запрос информации о несуществующем питомце возвращает ошибку."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    nonexistent_pet_id = "123456789"
    status, result = pf.get_pet_info(auth_key, nonexistent_pet_id)
    assert status != 200  # Ожидаем неуспех
