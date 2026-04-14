import os
from azure.cosmos import CosmosClient

class CosmosService:
    def __init__(self):
        # Handle credentials properly
        self.endpoint = os.getenv("COSMOS_ENDPOINT")
        self.key = os.getenv("COSMOS_KEY")
        self.database_name = "EmployeeDB"
        self.container_name = "Profiles"
        
        # Initialize the client
        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def create_item(self, data):
        """All Cosmos DB interaction must go through this layer."""
        try:
            return self.container.upsert_item(data)
        except Exception as e:
            print(f"Cosmos Service Error (create_item): {e}")
            raise e

    def get_items(self):
        """Fetches all items from the container."""
        try:
            return list(self.container.read_all_items())
        except Exception as e:
            print(f"Cosmos Service Error (get_items): {e}")
            return []

# Create a singleton instance to use in views
cosmos_service = CosmosService()
"""
# Initialize client
endpoint = os.getenv("COSMOS_ENDPOINT")
key = os.getenv("COSMOS_KEY")
client = CosmosClient(endpoint, key)
container = client.get_database_client("UserDB").get_container_client("Profiles")

def save_user_profile(user_data, image_url):
    #Saves user metadata to Cosmos DB.
    document = {
        "id": user_data['id'],  # Using username as the unique ID
        "partitionKey": user_data['email'], # Partitioning by email
        "email": user_data['email'],
        "password_hash": user_data['password'],
        "portfolio": user_data['portfolio'],
        "profile_pic_url": image_url,
        "full_name": user_data['name'],
        "type": "employee"
    }
    return container.upsert_item(document)
"""