import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category
from tqdm import tqdm


class Command(BaseCommand):
    help = "Import categories from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file_path", type=str, help="The path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file_path"]
        self.import_categories_from_csv(csv_file_path)
        self.stdout.write(self.style.SUCCESS("Categories imported successfully."))

    def get_or_create_category(self, title, parent=None):
        slug = slugify(title, allow_unicode=True)
        category = Category.objects.filter(slug=slug).first()
        if category is None:
            category = Category.objects.create(title=title, slug=slug, parent=parent)
        return category

    def import_categories_from_csv(self, csv_file_path):
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            csv_reader = list(csv.reader(csvfile))
            total_rows = len(csv_reader)

            for row in tqdm(
                csv_reader,
                total=total_rows,
                desc="Importing Categories",
                unit="row",
                ncols=100,
                bar_format="{l_bar}\033[32m{bar}\033[0m| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
            ):
                parent = None
                for title in row:
                    if title:
                        category = self.get_or_create_category(title, parent)
                        parent = category
