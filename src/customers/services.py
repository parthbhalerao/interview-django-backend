from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Customer
import helpers.billing
from django.db import models

User = get_user_model()

class CustomerService:
    @staticmethod
    def get_customer_by_user(user_id: int) -> Customer:
        return get_object_or_404(
            Customer.objects.select_related('user'),
            user_id=user_id
        )
    
    @staticmethod
    def create_customer(user: User, init_email: str = None) -> Customer:
        if Customer.objects.filter(user=user).exists():
            raise ValidationError("Customer already exists for this user")
            
        customer = Customer.objects.create(
            user=user,
            init_email=init_email or user.email,
            init_email_confirmed=False
        )
        return customer
    
    @staticmethod
    def confirm_customer_email(customer: Customer) -> Customer:
        if not customer.init_email_confirmed:
            customer.init_email_confirmed = True
            
            # Create Stripe customer
            if not customer.stripe_id and customer.init_email:
                stripe_id = helpers.billing.create_customer(
                    email=customer.init_email,
                    metadata={
                        "user_id": customer.user.id,
                        "username": customer.user.username
                    },
                    raw=False
                )
                customer.stripe_id = stripe_id
            
            customer.save()
        return customer

    @staticmethod
    def handle_user_signup(request, user, *args, **kwargs):
        """Handler for allauth user signup signal"""
        CustomerService.create_customer(user, user.email)

    @staticmethod
    def handle_email_confirmation(request, email_address, *args, **kwargs):
        """Handler for allauth email confirmation signal"""
        customers = Customer.objects.filter(
            init_email=email_address,
            init_email_confirmed=False
        )
        for customer in customers:
            CustomerService.confirm_customer_email(customer)

    @staticmethod
    def get_customer_by_id(customer_id: int) -> Customer:
        return get_object_or_404(
            Customer.objects.select_related('user'),
            id=customer_id
        )

    @staticmethod
    def list_customers(search: str = None):
        queryset = Customer.objects.select_related('user')
        if search:
            queryset = queryset.filter(
                models.Q(user__username__icontains=search) |
                models.Q(user__email__icontains=search)
            )
        return queryset
