import uuid
from azure.storage.blob import BlobServiceClient
import os
# Initialize client
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
client = BlobServiceClient.from_connection_string(connection_string)
container_client = client.get_container_client("profile-pics")

def upload_profile_picture(file_obj):
    """Uploads a file and returns the public URL."""
    # Create a unique name to avoid overwriting
    try:
        # 1. Reset file pointer to the start
        file_obj.seek(0)
        
        # 2. Use the correct client variable (ensure this matches your init)
        # Assuming your BlobServiceClient is named 'client'
        blob_client = client.get_blob_client(
            container="profile-pics", 
            blob=f"user_pics/{file_obj.name}" # Good practice to use a subfolder
        )
        
        blob_client.upload_blob(file_obj, overwrite=True)
        
        print(f"DEBUG: Successfully uploaded {file_obj.name}")
        return blob_client.url
        
    except Exception as e:
        # This will show up in your terminal if the connection fails
        print(f"DEBUG: Azure Upload Failed! Details: {e}")
        return "No URL Generated"
    """
    # blob upload of profile pic- version 2
    file_obj.seek(0)
    ext = file_obj.name.split('.')[-1]
    unique_name = f"user_pics/{uuid.uuid4()}.{ext}"
    
    blob_client = container_client.get_blob_client(unique_name)
    blob_client.upload_blob(file_obj, overwrite=True)
    
    return blob_client.url
    """
    # blob upload of profile pic- version 1
    """
    def upload_profile_picture(file_obj):

    #Uploads a file and returns the public URL.

    # Create a unique name to avoid overwriting

    try:

        blob_client = blob_service_client.get_blob_client(

            container="profile-pics",

            blob=file_obj.name

        )

        blob_client.upload_blob(file_obj, overwrite=True)

        return blob_client.url

    except Exception as e:

        print(f"DEBUG: Azure Upload Failed! Details: {e}")

        return None
    """