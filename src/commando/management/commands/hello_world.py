from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        """Command to print 'Hello, World!'"""
        print("Hello, World!")