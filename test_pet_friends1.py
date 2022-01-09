from .api import PetFriends
from .settings import valid_email, valid_password, wrong_password, wrong_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем возможность получения списка питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo="images/screens.jpg"):
    """Проверяем что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    my_pets = my_pets["pets"]
    my_ids = [my_pets[i]["id"] for i in range(len(my_pets))]
    assert status == 200
    assert pet_id not in my_ids


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_simple(name="Шарик", animal_type="Шпиц", age="7"):
    """Проверяем возможность добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_add_pets_set_photo():
    """Проверяем возможность добавления фото уже добавленному питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet_simple(auth_key, name="Шарик", animal_type="Шпиц", age="7")
    pet_id = result["id"]
    status, result = pf.add_pets_set_photo(auth_key, pet_id, "images/screens.jpg")
    assert status == 200
    assert result["pet_photo"]


def test_get_api_key_for_wrong_user(email=wrong_email, password=wrong_password):
    """"Проверяем возможность получения ключа по неверному e-mail"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_wrong_user(email=valid_email, password=wrong_password):
    status, result = pf.get_api_key(email, password)
    """Проверяем возможность получения ключа с неверным паролем"""
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_wrong_age(name='Шарик', animal_type='двортерьер',
                                     age='-5', pet_photo="images/screens.jpg"):
    """Проверяем возможность добавления питомца с отрицательным значением возраста """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_wrong_name(name='a'*300, animal_type='двортерьер',
                                     age='4',pet_photo="images/screens.jpg"):
    """Проверяем возможность добавления питомца со слишком длинным именем (300 символов)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_simple_empty(name="", animal_type="", age=""):
    """Проверяем возможность отправки пустой формы"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_delete_deleted_pet():
    """Проверяем возможность удаления удалённого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/screens.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 400


def test_try_delete_alien_pet():
    """Проверяем возможность удаления чужого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    _, all_pets = pf.get_list_of_pets(auth_key,"")
    all_pets = all_pets["pets"]
    my_pets = my_pets["pets"]
    all_ids = [all_pets[i]["id"] for i in range(len(all_pets))]
    my_ids = [my_pets[i]["id"] for i in range(len(my_pets))]
    for k in all_ids:
        if k not in my_ids:
            break

    status, _ = pf.delete_pet(auth_key, k)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert k not in my_ids


def test_successful_update_alein_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации у чужого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    all_pets = all_pets["pets"]
    my_pets = my_pets["pets"]
    all_ids = [all_pets[i]["id"] for i in range(len(all_pets))]
    my_ids = [my_pets[i]["id"] for i in range(len(my_pets))]
    for k in all_ids:
        if k not in my_ids:
            break

    status, result = pf.update_pet_info(auth_key, k, name, animal_type, age)
    assert status == 200
    assert result['name'] == name























