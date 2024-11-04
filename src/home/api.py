from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from auth.api import router as auth_router
from customers.api import router as customers_router
from subscriptions.api import router as subscriptions_router
api = NinjaExtraAPI()

# Register JWT routes (/api/v1/auth/tokens)
api.register_controllers(NinjaJWTDefaultController)

# Register auth routes (/api/auth/*)
api.add_router("/auth", auth_router)  # without trailing slash

# Register customers routes (/api/customers/*)
api.add_router("/customers", customers_router)

# Register subscriptions routes (/api/subscriptions/*)
api.add_router("/subscriptions", subscriptions_router)  # Add this line