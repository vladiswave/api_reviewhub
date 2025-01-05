import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import YamdbUser


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в указанные модели'
    model_mapping = {
        'users': YamdbUser,
        'category': Category,
        'genre': Genre,
        'titles': Title,
        'review': Review,
        'comments': Comment,
        'genre_title': Title.genre.through
    }

    def handle(self, *args, **kwargs):
        for model_name, model in self.model_mapping.items():
            self.import_model_data(model_name, model)

    def import_model_data(self, model_name, model):
        csv_file = f'{settings.BASE_DIR}/static/data/{model_name}.csv'
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                objs_to_create = []
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
                    objs_to_create.append(model(**obj_data))
                created_objs = model.objects.bulk_create(
                    objs_to_create, ignore_conflicts=True
                )
                for obj in created_objs:
                    self.stdout.write(self.style.SUCCESS(
                        f'{model_name.capitalize()} "{obj}" создано.')
                    )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'{file} -> Error: {e}'))
