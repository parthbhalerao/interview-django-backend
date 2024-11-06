from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth
from typing import List
from .services.base import CompanyService
from .schemas import CompanyResponseSchema
from django.http import HttpRequest

router = Router(tags=["Companies"])
company_service = CompanyService()

@router.get("/companies/", response=List[CompanyResponseSchema], auth=JWTAuth())
def list_companies(
    request: HttpRequest,
    search: str = Query(None, description="Search by company name")
):
    """List all companies"""
    return company_service.list_companies(search=search)
