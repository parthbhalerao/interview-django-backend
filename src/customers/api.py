from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth
from typing import List
from .services import CustomerService
from .schemas import CustomerResponseSchema
from django.http import HttpRequest

router = Router(tags=["Customers"])
customer_service = CustomerService()

@router.get("/me", response=CustomerResponseSchema, auth=JWTAuth())
@router.get("/me/", response=CustomerResponseSchema, auth=JWTAuth())
def get_customer_profile(request: HttpRequest):
    """Get the authenticated user's customer profile"""
    customer = customer_service.get_customer_by_user(request.auth.id)
    print(customer)
    return customer

@router.get("/{customer_id}", response=CustomerResponseSchema, auth=JWTAuth())
def get_customer(request: HttpRequest, customer_id: int):
    """Get a specific customer by ID (admin only)"""
    if not request.auth.is_staff:
        return None
    return customer_service.get_customer_by_id(customer_id)

@router.get("/", response=List[CustomerResponseSchema], auth=JWTAuth())
def list_customers(
    request: HttpRequest,
    search: str = Query(None, description="Search by username or email")
):
    """List all customers (admin only)"""
    if not request.auth.is_staff:
        return []
    return customer_service.list_customers(search=search)

