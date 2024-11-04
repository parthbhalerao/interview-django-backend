from ninja import Schema
from typing import Optional, List
from datetime import datetime

class SubscriptionBaseSchema(Schema):
    name: str
    subtitle: Optional[str] = None
    active: bool = True
    stripe_id: Optional[str] = None
    order: int = -1
    featured: bool = True
    features: Optional[str] = None

class SubscriptionPriceSchema(Schema):
    id: int
    stripe_id: Optional[str] = None
    interval: str  # 'month' or 'year'
    price: float
    order: int = -1
    featured: bool = True
    subscription_id: Optional[int] = None

class SubscriptionDetailSchema(SubscriptionBaseSchema):
    id: int
    prices: List[SubscriptionPriceSchema]
    updated: datetime
    timestamp: datetime

    def get_features_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split('\n')]

class UserSubscriptionSchema(Schema):
    id: int
    subscription_id: Optional[int] = None
    stripe_id: Optional[str] = None
    active: bool = True
    status: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False

class SubscriptionWebhookSchema(Schema):
    type: str
    data: dict

# Response schemas for error handling
class ErrorResponseSchema(Schema):
    detail: str

# Request schemas for subscription operations
class SubscriptionCancelSchema(Schema):
    cancel_at_period_end: bool = True
    feedback: Optional[str] = None

class SubscriptionUpdateSchema(Schema):
    price_id: int  # ID of the SubscriptionPrice to switch to
