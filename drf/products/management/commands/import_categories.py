import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category

class Command(BaseCommand):
    help = 'Import categories from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        self.import_categories_from_csv(csv_file_path)
        self.stdout.write(self.style.SUCCESS('Categories imported successfully.'))

    def get_or_create_category(self, title, parent=None):
        slug = slugify(title, allow_unicode=True)
        # print(slug)
        category = Category.objects.filter(slug=slug).first()
        if category is None:
            # print(f'{category=} || {slug=}')
            category = Category.objects.create(
                title=title,
                slug=slug,
                parent=parent
            )
        return category

    def import_categories_from_csv(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                parent = None
                # print('='*30)
                for title in row:
                    if title:
                      # print(f'{title=}')
                      category = self.get_or_create_category(title, parent)
                      parent = category
