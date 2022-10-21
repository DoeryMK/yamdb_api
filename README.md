# api_yamdb

## API сервиса обсуждения популярных произведений

## **Краткое описание**
Данный проект является учебным групповым проектом. 

### _Распределение ролей_
В проекте реализовано четыре пользовательские роли:
1. Аноним
2. Аутентифицированный пользователь - user
3. Модератор - moderator
4. Администратор - admin
### _Доступные возможности ролей (разрешения)_
- анониму доступна возможность просмотра контента без регистрации
- зарегистрированному пользователю доступен следующий функционал:
	*  _просмотр и изменение персональных данных учетной записи;_
	*  _просмотр контента;_
	*  _добавление отзывов к произведениям;_
	*  _добавление комментариев к существующим отзывам;_
	*  _корректировка и удаление собственных отзывов и комментариев._
- модератору доступен весь функционал зарегистрированного пользователя с следующими дополнительными разрешениями:
	*  _корректировка и удаление существующих отзывов;_
	*  _корректировка и удаление существующих комментариев;_
- администратору доступен весь перечисленный выше функционал с дополнительными возможностями:

	*  _добавление и удаление пользователей;_
	*  _просмотр списка всех зарегистрированных пользователей;_
	*  _просмотр и корректировка данных зарегистрированных пользователей._
 
## **Требования**

Python 3.9.12
python-dotenv 0.19.0
requests 2.26.0
Django 2.2.16
django-filter 21.1
djangorestframework 3.12.4
djangorestframework-simplejwt 5.2.0


## **Запуск проекта**

В консоли выполните следующие команды:

1. Клонировать проект из репозитория
```
git clone git@github.com:DoeryMK/api_yamdb.git
```
или
```
git clone https://github.com/DoeryMK/api_yamdb.git
```
2. Перейти в папку с проектом и создать виртуальное окружение
```
cd <имя папки>
```
```
python -m venv venv
```
или
```
python3 -m venv venv
```
3. Активировать виртуальное окружение
```
source venv/Scripts/activate
```
или
```
source venv/bin/activate
```
4. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
5. Перейти в папку api_yamdb и выполнить миграции
```
cd api_yamdb
```
```
python manage.py makemigrations
```
или 
```
python3 manage.py makemigrations
```
```
python manage.py migrate
```
или
```
python3 manage.py migrate
```
6. Перейти в папку yatube/yatube и создать файл .env. В файле указать значение SECRET_KEY. 
```
SECRET_KEY = *ваш уникальный секретный ключ Django*
```
7. Запустить проект
```
python manage.py runserver
```
или 
```
python3 manage.py runserver
```

## **Тестирование через HHTP-клиент**
Для тестирования работы API проекта можно воспользоваться HHTP-клиентом [Postman](https://www.postman.com) или [httpie](https://httpie.io). 

## **Заполнение базы данными для тестирования**
Выполнить команду из директории api_yamdb/api_yamdb/
```
/api_yamdb/api_yamdb/$ python manage.py import_data
```
## **Пример запросов и ответов**

_Redoc доступен по ссылке_ http://127.0.0.1:8000/redoc/

1. *Создание пользователя администратором* 
POST-запрос к эндпоинту http://127.0.0.1:8000/api/v1/users
Request
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
Response
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
2. *Регистрация пользователя* 
POST-запрос к эндпоинту http://127.0.0.1:8000/api/v1/auth/signup/
Request
```
{
    "username": "string",
    "email": "user@example.com"
}
```
Response
```
{
    "username": "string",
    "email": "user@example.com"
}
```
_На указанную почту будет отправлен код подтверждения для получения токена._
3. *Получение токена для аутентификации в системе*
POST-запрос к эндпоинту http://127.0.0.1:8000/api/v1/auth/token/
Request
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
Response
```
{
    "token": "string"
}
```
4. *Просмотр данных собственной учетной записи*
GET-запрос к эндпоинту http://127.0.0.1:8000/api/v1/users/me
Response
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
5. *Обновление данных пользователя по username*
PATCH-запрос к эндпоинту http://127.0.0.1:8000/api/v1/users/username/
Request
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
Response
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
6. *Создание новой категории произведения администатором*
POST-запрос к эндпоинту http://127.0.0.1:8000/api/v1/categories/
Request
```
{
    "name": "string",
    "slug": "string"
}
```
Response
```
{
    "name": "string",
    "slug": "string"
}
```
7. *Удаление существующего жанра администатором*
DELETE-запрос к эндпоинту http://127.0.0.1:8000/api/v1/genres/{slug}/
8. *Обновление информации о произведении администратором*
PATCH-запрос к эндпоинту http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Request
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
    "string"
    ],
    "category": "string"
}
```
Response
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
    {}
    ],
    "category": {
    "name": "string",
    "slug": "string"
    }
}
```
9. *Добавление нового отзыва*
POST-запрос к эндпоинту http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Request
```
{
    "text": "string",
    "score": 1
}
```
Response
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
10. *Корректировка комментария по id*
PATCH-запрос к эндпоинту http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Request
```
{
    "text": "string"
}
```
Response
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

### Соавторы

[DoeryMK](https://github.com/DoeryMK) - часть Auth/Users и readme  
Перепелкин Александр - часть Categories/Genres/Titles и импорт для наполнения БД