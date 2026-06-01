import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ЛР5 VHI", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("vhi_cleaned.csv")
    return df

df = load_data()

st.title("Лабораторна робота №5")
st.subheader("Аналіз індексів VCI, TCI та VHI по областях України")

st.sidebar.header("Фільтри")

index_type = st.sidebar.selectbox(
    "Оберіть індекс для аналізу",
    ["VCI", "TCI", "VHI"]
)

area = st.sidebar.selectbox(
    "Оберіть область",
    sorted(df["Area"].unique())
)

week_range = st.sidebar.slider(
    "Оберіть інтервал тижнів",
    int(df["Week"].min()),
    int(df["Week"].max()),
    (1, 52)
)

year_range = st.sidebar.slider(
    "Оберіть інтервал років",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

sort_order = st.sidebar.radio(
    "Сортування",
    ["Без сортування", "За зростанням", "За спаданням"]
)

if st.sidebar.button("Reset"):
    st.rerun()

filtered = df[
    (df["Area"] == area) &
    (df["Week"] >= week_range[0]) &
    (df["Week"] <= week_range[1]) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

if sort_order == "За зростанням":
    filtered = filtered.sort_values(by=index_type)
elif sort_order == "За спаданням":
    filtered = filtered.sort_values(by=index_type, ascending=False)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Відфільтровані дані")
    st.dataframe(filtered)

with col2:
    st.subheader(f"Графік {index_type} для області: {area}")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(filtered["Year"], filtered[index_type], marker="o")
    ax.set_xlabel("Рік")
    ax.set_ylabel(index_type)
    ax.set_title(f"{index_type} для області {area}")
    ax.grid(True)
    st.pyplot(fig)

st.subheader(f"Порівняння {index_type} між областями")

comparison = df[
    (df["Week"] >= week_range[0]) &
    (df["Week"] <= week_range[1]) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

comparison_mean = comparison.groupby("Area")[index_type].mean().sort_values()

fig2, ax2 = plt.subplots(figsize=(12, 5))
comparison_mean.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Область")
ax2.set_ylabel(index_type)
ax2.set_title(f"Середнє значення {index_type} по областях")
plt.xticks(rotation=90)
st.pyplot(fig2)

st.subheader("Короткий висновок")
st.write(
    f"Було виконано фільтрацію даних за областю, роками та тижнями. "
    f"Для аналізу обрано показник {index_type}. "
    f"Побудовано графік зміни показника для області {area} та графік порівняння середніх значень між областями."
)
