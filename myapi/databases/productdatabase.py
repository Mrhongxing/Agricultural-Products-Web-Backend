from pydantic import BaseModel

class bakeDataForProduct(BaseModel):
    product_id: int
    product_name: str
    product_introduce: str
    product_price: float
    is_available: int
    product_image: str