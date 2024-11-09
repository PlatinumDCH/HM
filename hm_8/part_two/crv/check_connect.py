from part_two.crv.models import Contact
from pymongo.errors import ServerSelectionTimeoutError

def check_connection():
    """light request for check connection"""
    try:
        Contact.objects.first()
        print("MongoDB connection: Successful")
    except ServerSelectionTimeoutError:
        print("MongoDB connection: Failed")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while connecting to MongoDB: {e}")
        exit(1)