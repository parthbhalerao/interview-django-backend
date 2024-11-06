from typing import List, Optional
from ..models import Company, JobRole

class CompanyService:
    def create_or_update_company(self, data: dict) -> Company:
        print(f"Creating/updating company with data: {data}")
        company, _ = Company.objects.update_or_create(
            name=data['name'],
            defaults={
                'website': data.get('website_url', ''),
                'location': data.get('location', ''),
                'description': data.get('description', '')
            }
        )
        print(f"Company saved: {company}")
        return company

    def create_job_role(self, company: Company, title: str, level: str) -> JobRole:
        return JobRole.objects.create(
            company=company,
            title=title,
            level=level
        )

    def list_companies(self, search: str = None) -> List[Company]:
        queryset = Company.objects.all()
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
