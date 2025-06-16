from pydantic import BaseModel
from typing import Optional


class PaymentInfo(BaseModel):
    card_last4: Optional[str]
    stripe_customer_id: Optional[str]
    billing_email: Optional[str]
