from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self._create_users()
        self._create_admin("Petra", "Pickles")
        self._create_director("Marty", "Major")

    def _create_users(self):
        self._create_user("John", "Doe")
        user_count = 1
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            try:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                self._create_user(first_name, last_name)
            except:
                continue
            user_count += 1
        print("User seeding complete.      ")

    def _create_user(self, first_name, last_name ):
        username = self._email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_student=True
        )

    def _create_admin(self, first_name, last_name ):
        username = self._email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_admin=True
        )
    
    def _create_director(self, first_name, last_name ):
        username = self._email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_admin=True,
            is_director=True
        )

    def _email(self, first_name, last_name):
        email = f'{first_name.lower()}.{last_name.lower()}@example.org'
        return email