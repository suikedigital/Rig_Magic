from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    postcode: str
    country: str
