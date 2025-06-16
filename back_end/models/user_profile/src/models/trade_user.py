from pydantic import Field
from .base_user import BaseUser

class TradeUser(BaseUser):
    company_name: str
    role: str = Field(default="trade", const=True)
