from django.core.management.base import BaseCommand, CommandError
from lessons.models import Term

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("The unseed command has not been implemented yet!")
        print("TO DO: Create an unseed command following the instructions of the assignment carefully.")
        Term.objects.filter().delete()
