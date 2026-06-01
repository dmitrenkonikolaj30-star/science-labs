import os
import urllib.request
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

BASE_URL = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php"

YEAR1 = 1981
YEAR2 = 2024


def download_vhi_data():

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for province_id in range(1, 28):

        existing_files = [
            file for file in os.listdir(DATA_DIR)
            if file.startswith(f"vhi_province_{province_id}_")
        ]

        if existing_files:
            print(
                f"Область {province_id}: файл вже існує, пропуск."
            )
            continue

        url = (
            f"{BASE_URL}?country=UKR"
            f"&provinceID={province_id}"
            f"&year1={YEAR1}"
            f"&year2={YEAR2}"
            f"&type=Mean"
        )

        filename = (
            f"vhi_province_{province_id}_{current_datetime}.csv"
        )

        filepath = os.path.join(DATA_DIR, filename)

        try:
            urllib.request.urlretrieve(url, filepath)

            print(
                f"Область {province_id}: успішно завантажено."
            )

        except Exception as error:
            print(
                f"Область {province_id}: помилка -> {error}"
            )


download_vhi_data()
