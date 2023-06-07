from faker import Faker
from core.models import MyModel  

def generate_mock_data():
    fake = Faker()
    
    for _ in range(10):  # Generate 10 records
        my_model = MyModel()
        my_model.field1 = fake.name()
        my_model.field2 = fake.email()
        my_model.field3 = fake.random_int(min=1, max=100)
        my_model.save()