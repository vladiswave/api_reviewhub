# :file_folder: api_yamdb

## :scroll: Описание
**Api_YaMDb** - это API проекта YaИспользуемые технологииMDb, который собирает отзывы пользователей на произведения.

## :globe_with_meridians: Используемые технологии
- Python 3.9
- Django 3.2
- Django REST Framework
- JWT

## :computer: Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/vladiswave/api_yamdb/
```

```
cd api_yamdb
```
Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать и выполнить  миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Наполнить БД из csv файлов:

```
python manage.py add_date_from_csv
```

Запустить проект:

```
python manage.py runserver
```


## :books: Документация проекта
Техническая документация API проекта YaMDb расположена в файле 
[redoc.yaml](api_yamdb/static/redoc.yaml).

## :busts_in_silhouette: Авторы и контакты 
* [**Марат Айсин**](https://github.com/mbaisin)

* [**Виталий Багданов**](https://github.com/VitaliyBagdanov)

* [**Владислав Филиппов**](https://github.com/vladiswave)
