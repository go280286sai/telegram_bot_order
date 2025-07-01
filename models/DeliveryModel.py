from pydantic import BaseModel


class Delivery(BaseModel):
    """
    DeliveryModel
    """
    post_id: int
    address_id: int
    city_id: int
