from allauth.account.signals import (
    user_signed_up as allauth_user_signed_up,
    email_confirmed as allauth_email_confirmed
)
from .services import CustomerService

def connect_signals():
    allauth_user_signed_up.connect(CustomerService.handle_user_signup)
    allauth_email_confirmed.connect(CustomerService.handle_email_confirmation) 