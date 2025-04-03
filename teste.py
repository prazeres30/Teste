import streamlit as st
import pandas as pd
import os
import requests
import shutil

st.set_page_config(page_title="Baixar Arquivos de Planilha", layout="centered")

st.title("📁 Baixar arquivos de uma planilha com links")

uploaded_file = st.file_uploader("1️⃣ Envie sua planilha (.csv, .xls ou .xlsx)", type=["csv", "xls", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        st.stop()

    st.success("✅ Arquivo carregado com sucesso!")
    st.dataframe(df.head())

    # Tenta detectar a coluna com links
    url_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains("http").any():
            url_col = col
            break

    if not url_col:
        st.error("❌ Nenhuma coluna com URLs detectada.")
        st.stop()

    st.info(f"🔗 Coluna detectada com links: **{url_col}**")

    start = st.number_input("2️⃣ Linha inicial", min_value=0, max_value=len(df)-1, value=0, step=1)
    end = st.number_input("3️⃣ Linha final", min_value=start, max_value=len(df)-1, value=len(df)-1, step=1)

    if st.button("📥 Baixar arquivos"):
        # Cria a pasta
        if os.path.exists("arquivos brutos"):
            shutil.rmtree("arquivos brutos")
        os.makedirs("arquivos brutos", exist_ok=True)

        links = df.loc[start:end, url_col].dropna().tolist()
        success, fail = 0, 0

        for i, url in enumerate(links):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(f"arquivos brutos/arquivo_{i+1}.pdf", 'wb') as f:
                        f.write(response.content)
                    success += 1
                else:
                    fail += 1
            except Exception as e:
                fail += 1

        st.success(f"✅ Download concluído: {success} arquivos baixados.")
        if fail > 0:
            st.warning(f"⚠️ {fail} arquivos falharam.")
