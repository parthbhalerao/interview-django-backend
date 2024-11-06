from typing import List, Dict, Any
from .base import CompanyService
import logging

logger = logging.getLogger(__name__)

TECH_COMPANIES = [
    {
        "name": "Google",
        "domain": "google.com",
        "description": "A leading technology company specializing in search, cloud computing, software, and online advertising."
    },
    {
        "name": "Microsoft",
        "domain": "microsoft.com",
        "description": "Global technology corporation that develops and supports software, consumer electronics, and services."
    },
    {
        "name": "Apple",
        "domain": "apple.com",
        "description": "Technology company that designs and develops consumer electronics, software, and services."
    },
    {
        "name": "Amazon",
        "domain": "amazon.com",
        "description": "Multinational technology company focusing on e-commerce, cloud computing, and artificial intelligence."
    },
    {
        "name": "Meta",
        "domain": "meta.com",
        "description": "Technology company specializing in social networking, virtual reality, and metaverse technologies."
    }
]

class CompanyDataService:
    def __init__(self):
        self.company_service = CompanyService()

    def sync_companies(self) -> List[str]:
        results = []
        logger.info(f"Starting sync of {len(TECH_COMPANIES)} companies")
        
        for company in TECH_COMPANIES:
            try:
                company_data = {
                    "name": company["name"],
                    "website_url": f"https://{company['domain']}",
                    "description": company["description"],
                    "location": ""
                }
                
                logger.info(f"Attempting to sync company: {company['name']}")
                saved_company = self.company_service.create_or_update_company(company_data)
                logger.info(f"Successfully synced company: {saved_company.name}")
                results.append(f"Synced company: {saved_company.name}")
            except Exception as e:
                logger.error(f"Failed to sync company {company['name']}: {str(e)}")
                results.append(f"Failed to sync company {company['name']}: {str(e)}")
        
        return results 