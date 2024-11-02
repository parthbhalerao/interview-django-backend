import helpers.billing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from subscriptions.models import SubscriptionPrice, UserSubscription
from subscriptions import utils as subs_utils

@login_required
def user_subscription_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        print("refresh sub")
        finished = subs_utils.refresh_active_users_subscriptions([request.user.id], active_only=False)

        if finished:
            print('Sending Message of success')
            messages.success(request, "Your subscription details have been refreshed.")
        else:
            messages.error(request, "Failed to refresh your subscription details.")

        return redirect(user_sub_obj.get_absolute_url())
    return render(request, "subscriptions/user_detail_view.html", {"subscription": user_sub_obj})

@login_required
def user_subscription_cancel_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        print("refresh sub")
        if user_sub_obj.stripe_id and user_sub_obj.is_active_status:
            sub_data = helpers.billing.cancel_subscription(
                user_sub_obj.stripe_id, 
                reason="User wanted subscription to end!", 
                feedback="other",
                cancel_at_period_end=True,
                raw=False
            )

            for k,v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
            print('Sending Message of success')
            messages.success(request, "Your subscription has been cancelled.")
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, "subscriptions/user_cancel_view.html", {"subscription": user_sub_obj})

# Create your views here.
def subscription_price_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    int_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    int_yr = SubscriptionPrice.IntervalChoices.YEARLY
    object_list = qs.filter(interval = int_mo)
    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": int_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": int_yr})
    active = int_mo
    
    if interval == int_yr:
        active = int_yr
        object_list = qs.filter(interval = int_yr )

    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "mo_url": mo_url,
        "yr_url": yr_url,
        "active": active,
    })