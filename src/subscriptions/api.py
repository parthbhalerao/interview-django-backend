from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .models import Subscription, SubscriptionPrice, UserSubscription
from .schemas import (
    SubscriptionDetailSchema,
    SubscriptionPriceSchema,
    UserSubscriptionSchema,
    SubscriptionCancelSchema,
    SubscriptionUpdateSchema,
    ErrorResponseSchema
)
import helpers.billing
from subscriptions import utils as subs_utils
from django.conf import settings

router = Router(tags=["Subscriptions"])

@router.get("/plans", response=List[SubscriptionDetailSchema], auth=None)
@router.get("/plans/", response=List[SubscriptionDetailSchema], auth=None)
def list_subscription_plans(
    request: HttpRequest,
    interval: str = Query("month", description="Billing interval (month/year)")
):
    """List all active subscription plans with their prices"""
    subscriptions = (
        Subscription.objects
        .filter(active=True)
        .prefetch_related('subscriptionprice_set')
    )
    
    return [
        {
            **subscription.__dict__,
            "prices": [
                price for price in subscription.subscriptionprice_set.filter(interval=interval)
            ]
        }
        for subscription in subscriptions
    ]

@router.get("/me", response=UserSubscriptionSchema, auth=JWTAuth())
@router.get("/me/", response=UserSubscriptionSchema, auth=JWTAuth())
def get_my_subscription(request: HttpRequest):
    """Get the authenticated user's subscription"""
    subscription, _ = UserSubscription.objects.get_or_create(user=request.auth)
    return subscription

@router.post("/me/cancel", response={200: dict, 400: ErrorResponseSchema}, auth=JWTAuth())
def cancel_subscription(request: HttpRequest, data: SubscriptionCancelSchema):
    """Cancel the authenticated user's subscription"""
    subscription = get_object_or_404(UserSubscription, user=request.auth)
    
    if not subscription.stripe_id or not subscription.is_active_status:
        return 400, {"detail": "No active subscription found"}
    
    try:
        sub_data = helpers.billing.cancel_subscription(
            subscription.stripe_id,
            reason=data.feedback or "User cancelled subscription",
            cancel_at_period_end=data.cancel_at_period_end,
            raw=False
        )
        
        for k, v in sub_data.items():
            setattr(subscription, k, v)
        subscription.save()
        
        return 200, {"message": "Subscription cancelled successfully"}
    except Exception as e:
        return 400, {"detail": str(e)}

@router.post("/me/refresh", response={200: dict, 400: ErrorResponseSchema}, auth=JWTAuth())
def refresh_subscription(request: HttpRequest):
    """Refresh subscription status from Stripe"""
    try:
        finished = subs_utils.refresh_active_users_subscriptions(
            [request.auth.id], 
            active_only=False
        )
        if finished:
            return 200, {"message": "Subscription refreshed successfully"}
        return 400, {"detail": "Failed to refresh subscription"}
    except Exception as e:
        return 400, {"detail": str(e)}

@router.get("/prices/{price_id}", response=SubscriptionPriceSchema, auth=None)
def get_subscription_price(request: HttpRequest, price_id: int):
    """Get details for a specific subscription price"""
    return get_object_or_404(SubscriptionPrice, id=price_id)

@router.post("/checkout/{price_id}", response={200: dict, 400: ErrorResponseSchema}, auth=JWTAuth())
def create_checkout_session(request: HttpRequest, price_id: int):
    """Create a Stripe checkout session for subscription"""
    try:
        price_obj = get_object_or_404(SubscriptionPrice, id=price_id)
        customer_stripe_id = request.auth.customer.stripe_id
        
        url = helpers.billing.start_checkout_session(
            customer_stripe_id,
            success_url=f"{settings.BASE_URL}/api/subscriptions/checkout/success?session_id={{CHECKOUT_SESSION_ID}}", 
            cancel_url=f"{settings.BASE_URL}/pricing",
            price_stripe_id=price_obj.stripe_id,
            raw=False
        )
        
        return 200, {"checkout_url": url}
    except Exception as e:
        return 400, {"detail": str(e)}
