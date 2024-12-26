import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в указанные модели'
    model_mapping = {
        'users': CustomUser,
        'category': Category,
        'genre': Genre,
        'titles': Title,
        'review': Review,
        'comments': Comment,
    }

    def handle(self, *args, **kwargs):
        for model_name, model in self.model_mapping.items():
            self.import_model_data(model_name, model)
        self.import_genre_title(
            f'{settings.BASE_DIR}/static/data/genre_title.csv'
        )

    def import_model_data(self, model_name, model):
        csv_file = f'{settings.BASE_DIR}/static/data/{model_name}.csv'
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    obj_data = {}
                    for field in row.keys():
                        field_instance = model._meta.get_field(field)
                        if field_instance.is_relation:
                            related_model = field_instance.related_model
                            related_instance = related_model.objects.filter(
                                id=row[field]
                            ).first()
                            if related_instance:
                                obj_data[field] = related_instance
                            else:
                                self.stderr.write(
                                    self.style.ERROR(
                                        'Error: Связанное поле'
                                        f' {field_instance.__name__}'
                                        f' с id {row[field]} не существует.'
                                    )
                                )
                                continue
                        else:
                            obj_data[field] = row[field]
                    obj, created = model.objects.get_or_create(**obj_data)
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f'{model_name.capitalize()} "{obj}" создано.')
                        )
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'{model_name.capitalize()} "{obj}" уже создано.')
                        )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'{file} -> Error: {e}'))

    def import_genre_title(self, csv_file):
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                for row in csv.DictReader(file):
                    try:
                        title_object = Title.objects.get(
                            pk=int(row['title_id'])
                        )
                        genre_object = Genre.objects.get(
                            pk=int(row['genre_id'])
                        )
                        title_object.genre.add(genre_object)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Добавлено {genre_object} к {title_object}.'
                            )
                        )
                    except Title.DoesNotExist:
                        self.stderr.write(
                            self.style.ERROR(
                                f'Error: Заголовок Title с {row["title_id"]} '
                                'не существует.'
                            )
                        )
                    except Genre.DoesNotExist:
                        self.stderr.write(
                            self.style.ERROR(
                                f'Error: Обзор Genre с {row["genre_id"]} '
                                'не существует.'
                            )
                        )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'{file} -> Error:- {e}'))
