from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import get_user_model
from auth.schemas import UserSchema

router = Router(tags=["Customers"])
User = get_user_model()

@router.get("/me", response=UserSchema, auth=JWTAuth())
def get_profile(request):
    user = request.auth
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "first_name": user.first_name,
        "last_name": user.last_name
    }