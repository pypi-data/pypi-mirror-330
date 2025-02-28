import os
import time
import requests
import base64
from msal import ConfidentialClientApplication

def generate_access_token(client_id, client_secret, tenant_id):
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

def baixar_arquivos_onedrive(client_id, client_secret, tenant_id, caminho_pasta, folder_link):
    token = generate_access_token(client_id, client_secret, tenant_id)
    encoded_link = base64.urlsafe_b64encode(folder_link.encode()).decode().strip("=")

    headers = {"Authorization": f"Bearer {token}"}
    shared_link_url = f"https://graph.microsoft.com/v1.0/shares/u!{encoded_link}/driveItem"
    shared_link_response = requests.get(shared_link_url, headers=headers)
    shared_link_response.raise_for_status()
    drive_item = shared_link_response.json()

    folder_id = drive_item["id"]
    files_url = f'https://graph.microsoft.com/v1.0/drives/{drive_item["parentReference"]["driveId"]}/items/{folder_id}/children'
    files_response = requests.get(files_url, headers=headers)
    files_response.raise_for_status()
    files = files_response.json().get("value", [])

    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

    for file in files:
        file_name = file["name"]
        file_id = file["id"]
        download_url = f'https://graph.microsoft.com/v1.0/drives/{drive_item["parentReference"]["driveId"]}/items/{file_id}/content'

        file_response = requests.get(download_url, headers=headers, stream=True)
        with open(os.path.join(caminho_pasta, file_name), "wb") as f:
            for chunk in file_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Arquivo baixado: {file_name}")
