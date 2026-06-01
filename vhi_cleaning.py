import os
import re
import pandas as pd
from io import StringIO

DATA_DIR = "data"

noaa_to_ukraine = {
    1: ("Черкаська", 22),
    2: ("Чернігівська", 24),
    3: ("Чернівецька", 23),
    4: ("АР Крим", 25),
    5: ("Дніпропетровська", 3),
    6: ("Донецька", 4),
    7: ("Івано-Франківська", 8),
    8: ("Харківська", 19),
    9: ("Херсонська", 20),
    10: ("Хмельницька", 21),
    11: ("Київська", 9),
    12: ("м. Київ", 26),
    13: ("Кіровоградська", 10),
    14: ("Луганська", 11),
    15: ("Львівська", 12),
    16: ("Миколаївська", 13),
    17: ("Одеська", 14),
    18: ("Полтавська", 15),
    19: ("Рівненська", 16),
    20: ("м. Севастополь", 27),
    21: ("Сумська", 17),
    22: ("Тернопільська", 18),
    23: ("Закарпатська", 6),
    24: ("Вінницька", 1),
    25: ("Волинська", 2),
    26: ("Запорізька", 7),
    27: ("Житомирська", 5),
}

columns = ["Year", "Week", "SMN", "SMT", "VCI", "TCI", "VHI"]

all_data = []

for filename in os.listdir(DATA_DIR):
    if not filename.endswith(".csv"):
        continue

    match = re.search(r"vhi_province_(\d+)_", filename)
    if not match:
        continue

    province_id = int(match.group(1))
    province_name, area_index = noaa_to_ukraine[province_id]

    file_path = os.path.join(DATA_DIR, filename)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    # Видаляємо HTML-теги та службовий текст
    text = re.sub(r"<.*?>", "", text)

    # Залишаємо тільки рядки з даними, які починаються з року
    data_lines = [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^\d{4}\s*,", line.strip())
    ]

    clean_text = "\n".join(data_lines)

    df = pd.read_csv(StringIO(clean_text), header=None)
    df = df.iloc[:, :7]
    df.columns = columns

    df["Province_ID_NOAA"] = province_id
    df["Area"] = province_name
    df["Area_ID"] = area_index

    all_data.append(df)

vhi_df = pd.concat(all_data, ignore_index=True)

# Перетворюємо числові стовпці
numeric_columns = ["Year", "Week", "SMN", "SMT", "VCI", "TCI", "VHI"]
for column in numeric_columns:
    vhi_df[column] = pd.to_numeric(vhi_df[column], errors="coerce")

# Прибираємо некоректні та зайві рядки
vhi_df = vhi_df.dropna(subset=["Year", "Week"])
vi_df = vhi_df.drop_duplicates()

# Значення -1 часто означає пропуск
vhi_df = vhi_df.replace(-1, pd.NA)

# Заповнюємо пропуски середнім значенням по відповідній області
for column in ["SMN", "SMT", "VCI", "TCI", "VHI"]:
    vhi_df[column] = vhi_df.groupby("Area")[column].transform(
        lambda x: x.fillna(x.mean())
    )

# Сортування
vhi_df = vhi_df.sort_values(by=["Area_ID", "Year", "Week"])

print(vhi_df.head())
print()
print("Розмір dataframe:", vhi_df.shape)
print("Кількість пропусків:")
print(vhi_df.isna().sum())
print("\nПеревірка зміни індексів областей:")
print(
    vhi_df[["Province_ID_NOAA", "Area_ID", "Area"]]
    .drop_duplicates()
    .sort_values("Area_ID")
)

vhi_df.to_csv("vhi_cleaned.csv", index=False, encoding="utf-8")
print()
print("Очищений dataframe збережено у файл vhi_cleaned.csv")
