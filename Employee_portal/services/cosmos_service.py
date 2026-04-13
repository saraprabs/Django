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
        "id": user_data['email'],  # Using email as ID for simplicity
        "partitionKey": user_data['email'],
        "name": user_data['name'],
        "portfolio": user_data['portfolio'],
        "profile_pic_url": image_url, # Just the string link
        "status": "active"
    }
    return container.upsert_item(document)
