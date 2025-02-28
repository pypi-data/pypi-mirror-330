import os
import shutil
import wget
import zipfile
import requests
from subprocess import run, PIPE

def atualiza_chromedriver():
    bin_folder_path = "ArquivosRobo/bin"
    os.makedirs(bin_folder_path, exist_ok=True)

    def get_actual_chromedriver_path(folder):
        pattern = os.path.join(folder, "chromedriver.exe")
        if os.path.exists(pattern):
            return pattern
        return None

    def get_latest_chromedriver_version():
        url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data["channels"]["Stable"]["version"]
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch ChromeDriver version: {e}")

    def get_local_chromedriver_version(driver_path):
        if driver_path and os.path.exists(driver_path):
            result = run([driver_path, "--version"], stdout=PIPE, stderr=PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.split(" ")[1].strip()
        return None

    chrome_driver_path = get_actual_chromedriver_path(bin_folder_path)
    local_version = get_local_chromedriver_version(chrome_driver_path)
    latest_version = get_latest_chromedriver_version()

    if not local_version or local_version.split(".")[0] != latest_version.split(".")[0]:
        print("Atualizando o ChromeDriver")

        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{latest_version}/win64/chromedriver-win64.zip"
        latest_driver_zip = wget.download(download_url, "chromedriver.zip")

        destination_folder = os.path.join("bin")
        os.makedirs(destination_folder, exist_ok=True)

        destination_zip = os.path.join(destination_folder, os.path.basename(latest_driver_zip))
        shutil.move(latest_driver_zip, destination_zip)

        with zipfile.ZipFile(destination_zip, "r") as zip_ref:
            zip_ref.extractall(destination_folder)

        extracted_folder = os.path.join(destination_folder, "chromedriver-win64")
        chromedriver_path = os.path.join(extracted_folder, "chromedriver.exe")

        if os.path.exists(chromedriver_path):
            if chrome_driver_path:
                os.remove(chrome_driver_path)
            shutil.move(chromedriver_path, destination_folder)

        shutil.rmtree(extracted_folder)
        os.remove(destination_zip)
        print(f"\nChromeDriver atualizado com sucesso para a versão {latest_version}.\n")
