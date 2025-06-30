
import streamlit as st
import pandas as pd

st.title("Corectare grile Rezidențiat din ZipGrade")

uploaded_file = st.file_uploader("Încarcă fișierul complet CSV exportat din ZipGrade", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    studenti = df["StudentID"]
    rezultate = []

    for idx, row in df.iterrows():
        scor = 0.0

        # Complement simplu (intrebari 1–60)
        for i in range(1, 61):
            key = str(row[f"PriKey{i}"]).strip().upper()
            mark = str(row[f"Mark{i}"]).strip().upper()
            if key and mark and key == mark:
                scor += 1.0

        # Complement multiplu (intrebari 61–100)
        for i in range(61, 101):
            key = set(str(row.get(f"PriKey{i}", "")).strip().upper())
            mark = set(str(row.get(f"Mark{i}", "")).strip().upper())
            for litera in "ABCDE":
                if (litera in key and litera in mark) or (litera not in key and litera not in mark):
                    scor += 0.2

        rezultate.append({"ID": row["StudentID"], "Punctaj": round(scor, 2)})

    rezultate_df = pd.DataFrame(rezultate)
    st.subheader("Rezultate corectare complete:")
    st.dataframe(rezultate_df)
