import uuid
from azure.storage.blob import BlobServiceClient

# Initialize client
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
client = BlobServiceClient.from_connection_string(connection_string)
container_client = client.get_container_client("profile-pics")

def upload_profile_picture(file_obj):
    """Uploads a file and returns the public URL."""
    # Create a unique name to avoid overwriting
    ext = file_obj.name.split('.')[-1]
    unique_name = f"user_pics/{uuid.uuid4()}.{ext}"
    
    blob_client = container_client.get_blob_client(unique_name)
    blob_client.upload_blob(file_obj, overwrite=True)
    
    return blob_client.url
