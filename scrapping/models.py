from pydantic import BaseModel

# This Python class represents a product with attributes for title, price, and image path.
class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str