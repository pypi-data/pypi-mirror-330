import os
import re
import time
import base64
import requests
from msal import ConfidentialClientApplication

def generate_access_token(client_id, client_secret, tenant_id):
    """Generates an access token for Microsoft Graph API."""
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }
    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    return token_response.json().get("access_token")

def get_drive_and_folder_ids(folder_link, access_token):
    """Retrieves the drive ID and folder ID from a shared OneDrive link."""
    encoded_link = base64.urlsafe_b64encode(folder_link.encode()).decode().strip("=")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/shares/{encoded_link}/driveItem", headers=headers
    )
    response.raise_for_status()
    drive_item = response.json()
    return drive_item["parentReference"]["driveId"], drive_item["id"]

def download_file(file_id, access_token, download_path):
    """Downloads a file from OneDrive using Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content", headers=headers, stream=True
    )
    if response.status_code == 200:
        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download file: {response.json()}")

def list_and_download_files(access_token, folder_id, download_dir):
    """Lists files in a OneDrive folder and downloads them."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children", headers=headers
    )
    if response.status_code == 200:
        for item in response.json().get("value", []):
            if "file" in item:
                download_file(item["id"], access_token, os.path.join(download_dir, item["name"]))
    else:
        print(f"Failed to list files: {response.json()}")

def upload_file_to_onedrive(client_id, client_secret, tenant_id, file_path, folder_link):
    """Uploads a file to a specific folder in OneDrive using Microsoft Graph API."""
    access_token = generate_access_token(client_id, client_secret, tenant_id)
    site_id, drive_id, folder_id = get_drive_and_folder_ids(folder_link, access_token)
    file_name = os.path.basename(file_path)
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}:/{file_name}:/content"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/octet-stream"}
    with open(file_path, "rb") as f:
        requests.put(upload_url, headers=headers, data=f)

def extract_file_id(file_link):
    """Extracts the file ID from a OneDrive share link."""
    match = re.search(r"personal/.+?/(\w{10,})\?e=", file_link)
    if match:
        return match.group(1)
    raise ValueError("Could not extract file ID from the provided OneDrive link.")
