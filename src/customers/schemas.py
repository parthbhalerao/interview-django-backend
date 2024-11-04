from ninja import Schema
from typing import Optional
from auth.schemas import UserSchema

# Add an error response schema
class ErrorResponseSchema(Schema):
    detail: str

class CustomerBaseSchema(Schema):
    stripe_id: Optional[str] = None
    init_email: Optional[str] = None
    init_email_confirmed: bool = False

class CustomerCreateSchema(CustomerBaseSchema):
    user_id: int

class CustomerResponseSchema(CustomerBaseSchema):
    id: int
    user: UserSchema
