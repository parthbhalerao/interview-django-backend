from django.core.management.base import BaseCommand
from jobs.services.apollo import ApolloService, test_api_connection

class Command(BaseCommand):
    help = 'Sync companies from Apollo.io'

    def handle(self, *args, **options):
        # First test connection
        self.stdout.write("Testing API connection...")
        health_check = test_api_connection()
        self.stdout.write(f"Health check response: {health_check}")
        
        if health_check['status'] == 'success':
            self.stdout.write("Starting company sync...")
            service = ApolloService()
            try:
                results = service.sync_companies()
                for result in results:
                    self.stdout.write(result)
                self.stdout.write(self.style.SUCCESS("Sync completed successfully"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Sync failed: {str(e)}")
                )
        else:
            self.stdout.write(
                self.style.ERROR("API connection test failed. Aborting sync.")
            )