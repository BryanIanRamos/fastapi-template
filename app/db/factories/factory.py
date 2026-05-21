"""Factory helper for generating fake data (Laravel-style)"""
from faker import Faker


class Factory:
    """Factory for generating test data using Faker (similar to Laravel)"""
    
    def __init__(self):
        self.faker = Faker()
    
    # Text methods
    def name(self):
        """Generate a full name"""
        return self.faker.name()
    
    def first_name(self):
        """Generate a first name"""
        return self.faker.first_name()
    
    def last_name(self):
        """Generate a last name"""
        return self.faker.last_name()
    
    def email(self):
        """Generate a unique email"""
        return self.faker.unique.email()
    
    def username(self):
        """Generate a unique username"""
        return self.faker.user_name()
    
    def word(self):
        """Generate a single word"""
        return self.faker.word()
    
    def words(self, nb=3):
        """Generate multiple words"""
        return " ".join(self.faker.words(nb=nb))
    
    def sentence(self, nb_words=6):
        """Generate a sentence"""
        return self.faker.sentence(nb_words=nb_words)
    
    def sentences(self, nb=3):
        """Generate multiple sentences"""
        return " ".join(self.faker.sentences(nb=nb))
    
    def paragraph(self, nb_sentences=3):
        """Generate a paragraph"""
        return self.faker.paragraph(nb_sentences=nb_sentences)
    
    def paragraphs(self, nb=3):
        """Generate multiple paragraphs"""
        return "\n\n".join(self.faker.paragraphs(nb=nb))
    
    def text(self, max_nb_chars=200):
        """Generate random text up to max characters"""
        return self.faker.text(max_nb_chars=max_nb_chars)
    
    # Number methods
    def number(self, digits=None, positive=True):
        """Generate a random number"""
        if digits:
            return self.faker.numerify(text="#" * digits)
        return self.faker.random_int(min=0 if positive else -999, max=999)
    
    def integer(self, min=0, max=100):
        """Generate a random integer"""
        return self.faker.random_int(min=min, max=max)
    
    def phone_number(self):
        """Generate a phone number"""
        return self.faker.phone_number()
    
    def url(self):
        """Generate a URL"""
        return self.faker.url()
    
    def ipv4(self):
        """Generate an IPv4 address"""
        return self.faker.ipv4()
    
    # Date/Time methods
    def date(self):
        """Generate a random date"""
        return self.faker.date()
    
    def datetime(self):
        """Generate a random datetime"""
        return self.faker.date_time()
    
    def time(self):
        """Generate a random time"""
        return self.faker.time()
    
    # Location methods
    def city(self):
        """Generate a city name"""
        return self.faker.city()
    
    def state(self):
        """Generate a state or region name"""
        return self.faker.state()
    
    def country(self):
        """Generate a country name"""
        return self.faker.country()
    
    def address(self):
        """Generate a full address"""
        return self.faker.address()
    
    def latitude(self):
        """Generate latitude coordinate"""
        return self.faker.latitude()
    
    def longitude(self):
        """Generate longitude coordinate"""
        return self.faker.longitude()
    
    def coordinates(self):
        """Generate latitude and longitude"""
        return self.faker.latitude(), self.faker.longitude()
    
    # Custom helpers
    def rating(self, min=1, max=5):
        """Generate a rating"""
        return self.faker.random_int(min=min, max=max)
    
    def boolean(self, chance_of_getting_true=50):
        """Generate a boolean"""
        return self.faker.pybool(truth_percentage=chance_of_getting_true)


# Global factory instance
fake = Factory()
