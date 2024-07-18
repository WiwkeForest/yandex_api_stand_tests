import sender_stand_request
import data



def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

def positive_assert(first_name):
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
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

def test_create_user_2_letter_in_first_name_get_success_response(): # тест 1
        positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response(): # тест 2
    positive_assert("Ааааааааааааааа")

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_create_user_1_letter_in_first_name_get_error_response(): # тест 3
    negative_assert_symbol("А")

def test_create_user_16_letter_in_first_name_get_error_response(): # тест 4
    negative_assert_symbol("Аааааааааааааааа")

def test_create_user_english_letter_in_first_name_get_success_response(): # тест 5
    positive_assert("QWErty")

def test_create_user_russian_letter_in_first_name_get_success_response(): # тест 6
    positive_assert("Мария")

def test_create_user_has_space_in_first_name_get_error_response(): # тест 7
    negative_assert_symbol("Человек и Ко")

def test_create_user_has_special_symbol_in_first_name_get_error_response(): # тест 8
    negative_assert_symbol("№%@")

def test_create_user_has_number_in_first_name_get_error_response(): # тест 9
    negative_assert_symbol("123")

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

def test_create_user_no_first_name_get_error_response(): # тест 10
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

def test_create_user_empty_first_name_get_error_response(): # тест 11
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response(): # тест 12
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400

