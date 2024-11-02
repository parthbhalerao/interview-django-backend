from ninja import Router
from ninja_extra.permissions import AllowAny
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import get_user_model, authenticate
from .schemas import (
    LoginSchema, 
    RegisterSchema, 
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema,
    TokenRefreshSchema
)
from django.db import IntegrityError
from ninja_jwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

router = Router(tags=["Users"])
User = get_user_model()

@router.post("/register", response={201: dict, 400: dict}, auth=None)
def register(request, data: RegisterSchema):
    try:
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password
        )
        refresh = RefreshToken.for_user(user)
        return 201, {
            "message": "User created successfully",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
    except IntegrityError:
        return 400, {"error": "Username already exists"}
    except Exception as e:
        return 422, {"detail": str(e)}

@router.post("/login", response={200: dict, 401: dict}, auth=None)
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return 200, {
            "message": "Login successful",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
    return 401, {"error": "Invalid credentials"}

'''@router.post("/password/reset", response={200: dict, 400: dict}, auth=None)
def password_reset_request(request, data: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email=data.email)
        token = RefreshToken.for_user(user)
        
        # Send password reset email
        context = {
            'user': user,
            'reset_url': f"{settings.FRONTEND_URL}/reset-password?token={token}"
        }
        
        email_html = render_to_string('auth/password_reset_email.html', context)
        send_mail(
            'Password Reset Request',
            'Please reset your password',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=email_html
        )
        
        return 200, {"message": "Password reset email sent"}
    except User.DoesNotExist:
        return 200, {"message": "Password reset email sent"}  # Same response for security

@router.post("/password/reset/confirm", response={200: dict, 400: dict}, auth=None)
def password_reset_confirm(request, data: PasswordResetConfirmSchema):
    try:
        token = RefreshToken(data.token)
        user_id = token.payload.get('user_id')
        user = User.objects.get(id=user_id)
        
        user.set_password(data.password)
        user.save()
        
        return 200, {"message": "Password reset successful"}
    except Exception as e:
        return 400, {"error": "Invalid or expired token"}'''

@router.post("/token/refresh", response={200: dict, 401: dict}, auth=None)
def token_refresh(request, data: TokenRefreshSchema):
    try:
        refresh = RefreshToken(data.refresh)
        return 200, {
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
    except Exception:
        return 401, {"error": "Invalid refresh token"}