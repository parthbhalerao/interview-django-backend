import requests
from django.conf import settings
from .base import CompanyService
from typing import List, Dict, Any

def test_api_connection() -> dict:
    service = ApolloService()
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": service.api_key
    }
    
    try:
        response = requests.get(
            f"{service.base_url}/auth/health",
            headers=headers
        )
        return {
            "status": "success" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "message": response.json() if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "status_code": None,
            "message": str(e)
        }

class ApolloService:
    def __init__(self):
        self.api_key = settings.APOLLO_IO_API_KEY
        self.base_url = "https://api.apollo.io/v1"
        self.company_service = CompanyService()

    def search_companies(self):
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        
        payload = {
            "api_key": self.api_key,
            "q_organization_industry_types": ["Computer Software", "Information Technology"],
            "page": 1,
            "per_page": 25
        }
        
        response = requests.post(
            f"{self.base_url}/organizations/search",
            json=payload,
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.json()}")
            return None
            
        return response.json()

    def sync_companies(self) -> List[str]:
        results = []
        data = self.search_companies()
        
        for company_data in data.get('organizations', []):
            try:
                company = self.company_service.create_or_update_company(company_data)
                results.append(f"Synced: {company.name}")
            except Exception as e:
                results.append(f"Error syncing {company_data.get('name')}: {str(e)}")
        
        return results
