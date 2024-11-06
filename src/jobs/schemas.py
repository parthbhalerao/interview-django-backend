from ninja import Schema
from typing import Optional

class CompanyResponseSchema(Schema):
    id: int
    name: str
    website: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None