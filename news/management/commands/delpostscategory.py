from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Удаляет все посты из указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы хотите удалить все статьи в категории {options["category"]}? (y/n): ')

        if answer != 'y'.lower():
            self.stdout.write(self.style.ERROR('Отменено'))
        else:

            posts_cat = Post.objects.filter(categoriesPost__nameNewsCategories=options["category"])

            if posts_cat.exists():
                posts_cat.delete()
                self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории {options["category"]}'))
            else:
                self.stdout.write(self.style.ERROR(f'Не удалось найти посты выбранной категории {options["category"]}'))
