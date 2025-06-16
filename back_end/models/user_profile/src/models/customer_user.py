from pydantic import Field
from .base_user import BaseUser

class CustomerUser(BaseUser):
    role: str = Field(default="customer", const=True)
