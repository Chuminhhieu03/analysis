from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from income.models import Income
#use random choice to generate random data
import random
class Command(BaseCommand):
    help = 'Creates fake income data'

    def handle(self, *args, **options):

        Income.objects.all().delete()
        user = User.objects.get(username='chuhieu')
        for month in range(1,13):
            for day in range(1,29):
                Income.objects.create(user=user, date=f'2023-{month}-{day}', amount=random.randrange(1000,5000), source='0', description='Salary')
                Income.objects.create(user=user, date=f'2023-{month}-{day}', amount=random.randrange(1000,5000), source='1', description='Business')
                Income.objects.create(user=user, date=f'2023-{month}-{day}', amount=random.randrange(1000,5000), source='2', description='Side Hustle')
                Income.objects.create(user=user, date=f'2023-{month}-{day}', amount=random.randrange(1000,5000), source='3', description='Other')