from django.core.management.base import BaseCommand
from jobs.services.company_data import CompanyDataService

class Command(BaseCommand):
    help = 'Sync top tech companies data'

    def handle(self, *args, **options):
        self.stdout.write("Starting company sync...")
        service = CompanyDataService()
        try:
            results = service.sync_companies()
            for result in results:
                self.stdout.write(result)
            self.stdout.write(self.style.SUCCESS("Sync completed successfully"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Sync failed: {str(e)}")
            ) 