from pydantic import BaseModel, Field
from typing import List, Optional
from .address import Address
from .payment import PaymentInfo


class BaseUser(BaseModel):
    user_id: str = Field(..., description="Unique ID from Auth.js")
    role: str = Field(default="customer", description="User role")
    yacht_ids: List[str] = Field(default_factory=list)
    telephone: Optional[str] = None
    address: Optional[Address] = None
    subscription_status: Optional[str] = "free"
    payment_info: Optional[PaymentInfo] = None

    def yacht_count(self) -> int:
        return len(self.yacht_ids)

    def is_trade_user(self) -> bool:
        return self.role == "trade"
