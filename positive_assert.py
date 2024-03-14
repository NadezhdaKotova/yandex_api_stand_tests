import data
import configuration
import requests
import sender_stand_request
from create_user_test import get_user_body


# Функция для позитивной проверки
def positive_assert1(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400
    assert response.json()["code"] == 400
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert1("Aa")
# Тест 2. Успешное создание пользователя
# Параметр firstName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert1("Ааааааааааааааа")
# Тест 3.Количество символов меньше допустимого (1)
# Параметр firstName состоит из 1 символов
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")
# Тест 4.Количество символов больше допустимого (16)
# Параметр firstName состоит из 1 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")
# Тест 4.Количество символов больше допустимого (16)
# Параметр firstName состоит из 1 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")
# Тест 5.Разрешены английские буквы
# Параметр firstName состоит из QWErty
def test_create_user_qw_letter_in_first_name_get_error_response():
    positive_assert1("QWErty")
# Тест 6.Разрешены русские буквы
# Параметр firstName состоит из Мария
def test_create_user_mar_letter_in_first_name_get_error_response():
    positive_assert1("Мария")
# Тест 7. Запрещены пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")
# Тест 8. Запрещены спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")
# Тест 9. Запрещены цифры
def test_create_user_has_numbers_in_first_name_get_error_response():
    negative_assert_symbol("123")
# Тест 10. Не передан параметр
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)
# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)
# Тест 12. Передан другой тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
