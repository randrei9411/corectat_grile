
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

        # Complement simplu (întrebări 1–60): 1 punct doar dacă MarkX și PriKeyX sunt egale și ne-goale
        for i in range(1, 61):
            mark = str(row.get(f"Mark{i}", "")).strip().upper()
            key = str(row.get(f"PriKey{i}", "")).strip().upper()
            if mark and key and mark == key:
                scor += 1.0

        # Complement multiplu (întrebări 61–100): 0.2 per literă corect bifată/nebifată
        for i in range(61, 101):
            mark = set(str(row.get(f"Mark{i}", "")).strip().upper())
            key = set(str(row.get(f"PriKey{i}", "")).strip().upper())
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
