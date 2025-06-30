
import streamlit as st
import pandas as pd

st.title("Corectare grile Rezidențiat din ZipGrade")

uploaded_file = st.file_uploader("Încarcă fișierul complet CSV exportat din ZipGrade", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    rezultate = []

    for idx, row in df.iterrows():
        scor = 0.0

        # Complement simplu (întrebări 1–60): 1 punct doar dacă Mark == Key, iar Mark nu este X (adică nebifat)
        for i in range(1, 61):
            mark = str(row.get(f"Mark{i}", "")).strip().upper()
            key = str(row.get(f"PriKey{i}", "")).strip().upper()
            if mark == "X":
                mark = ""  # tratăm X ca nebifat
            if key == "X":
                key = ""
            if mark and key and mark == key:
                scor += 1.0

        # Complement multiplu (întrebări 61–100): 0.2 pentru fiecare literă corect bifată sau nebifată
        for i in range(61, 101):
            mark_raw = str(row.get(f"Mark{i}", "")).strip().upper()
            key_raw = str(row.get(f"PriKey{i}", "")).strip().upper()

            mark = set(mark_raw if mark_raw != "X" else "")
            key = set(key_raw if key_raw != "X" else "")

            for litera in "ABCDE":
                if (litera in key and litera in mark) or (litera not in key and litera not in mark):
                    scor += 0.2

        rezultate.append({
            "ID": row.get("StudentID", f"Elev {idx+1}"),
            "Punctaj": round(scor, 2)
        })

    rezultate_df = pd.DataFrame(rezultate)
    st.subheader("Rezultate corectare complete:")
    st.dataframe(rezultate_df)
