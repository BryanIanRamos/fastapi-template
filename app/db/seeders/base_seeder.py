"""Base seeder class with common utilities"""
from faker import Faker
from sqlalchemy.orm import Session


class BaseSeeder:
    """Base class for all seeders"""
    
    def __init__(self, db: Session):
        self.db = db
        self.faker = Faker()
    
    def run(self):
        """Override this method in child classes"""
        raise NotImplementedError("Subclasses must implement run() method")
    
    def check_if_exists(self, model, **filters):
        """Check if record exists based on filters"""
        return self.db.query(model).filter_by(**filters).first() is not None
    
    def count(self, model):
        """Count records in a table"""
        return self.db.query(model).count()
