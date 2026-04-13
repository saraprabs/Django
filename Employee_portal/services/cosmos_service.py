import os
from azure.cosmos import CosmosClient

# Initialize client
endpoint = os.getenv("COSMOS_ENDPOINT")
key = os.getenv("COSMOS_KEY")
client = CosmosClient(endpoint, key)
container = client.get_database_client("UserDB").get_container_client("Profiles")

def save_user_profile(user_data, image_url):
    """Saves user metadata to Cosmos DB."""
    document = {
        "id": user_data['username'],  # Using username as the unique ID
        "partitionKey": user_data['email'], # Partitioning by email
        "email": user_data['email'],
        "password_hash": user_data['password'],
        "portfolio": user_data['portfolio'],
        "profile_pic_url": image_url,
        "full_name": user_data['name'],
        "type": "employee"
    }
    return container.upsert_item(document)
