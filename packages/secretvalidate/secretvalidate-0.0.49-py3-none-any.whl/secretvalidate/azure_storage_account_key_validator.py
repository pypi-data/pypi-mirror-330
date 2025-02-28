from azure.storage.blob import BlobServiceClient
from secretvalidate.env_loader import get_secret_active, get_secret_inactive
import base64
import re

def extract_connection_string(text):
    pattern = r'(DefaultEndpointsProtocol.*?")'
    match = re.search(pattern, text)
    if match:
        return match.group(1)[:-1]
    return 

def build_connection_string(blob, secret):
    pattern = r'((?<=Microsoft\.Storage\/storageAccounts\/)[^\/]+)'
    match = re.search(pattern, blob["body"])
    if match:
        account_name = match.group(0)
        return f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={secret};EndpointSuffix=core.windows.net"
    return

def validate_azure_storage_account_key(blob, secret, response):
    try:
        connection_string = None
        blob_type = blob["type"]
        
        if blob_type == "pull_request_comment":
            connection_string = build_connection_string(blob["blob"], secret)
        if blob_type == "commit":
            content = base64.b64decode(blob["blob"]).decode('utf-8')
            connection_string = extract_connection_string(content)
        
        container_name = "dummy"
        if connection_string:
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            # If we can list blobs, the key is valid
            blobs_list = container_client.list_blobs()
            return get_secret_active() if response else "Azure Storage Account Key is valid"
    except Exception as e:
        if "ErrorCode:AuthenticationFailed" in str(e):
            return get_secret_inactive if response else "Azure Storage Account Key is invalid"
        elif "ErrorCode:ContainerNotFound" in str(e):
            # This error means that we can list blobs, but the container_name we picked doesn't exist
            return get_secret_active() if response else "Azure Storage Account Key is valid"
        else:
            return (f"Error: {e}")

