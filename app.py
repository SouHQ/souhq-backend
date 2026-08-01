import streamlit as st
import requests

st.set_page_config(page_title="SouHQ - Análise de Currículos", page_icon="📄", layout="centered")

st.title("📄 SouHQ - Analisador Inteligente de Currículos")
st.write("Faça o upload de um currículo em PDF para realizar a triagem automática com Inteligência Artificial.")

# URL do seu backend no Render
API_URL = "https://souhq-backend.onrender.com/api/analisar-curriculo/"

uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analisar Currículo"):
        with st.spinner("Analisando o currículo com IA, aguarde..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(API_URL, files=files)
                if response.status_code == 200:
                    resultado = response.json()
                    st.success("Análise concluída com sucesso!")
                    st.markdown("### Resultado da Análise:")
                    st.write(resultado)
                else:
                    st.error(f"Erro no servidor: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Não foi possível conectar à API: {e}")
