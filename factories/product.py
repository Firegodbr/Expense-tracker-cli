import factory
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: int
    stock: int

class ProductFactory(factory.Factory):
    class Meta:
        model = Product
    # Define default values for the fields
    name = factory.Faker('word')  # Random word for product name
    price = factory.Faker('random_number', digits=2)  # Random number as price
    stock = factory.Faker('random_int', min=1, max=10)  # Random stock count between 1 and 100
