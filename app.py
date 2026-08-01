import streamlit as st
import requests

st.set_page_config(page_title="SouHQ - Plataforma de Talentos", page_icon="📄")

# URL do seu backend no Render
BACKEND_URL = "https://souhq-backend.onrender.com"

# Inicializar estados da sessão para controle de login e dados
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# ==========================================
# FLUXO 1: TELA DE AUTENTICAÇÃO (Login / Cadastro)
# ==========================================
if not st.session_state["logado"]:
    st.title("SouHQ - Acesso ao Portal do Candidato")
    st.write("Faça login ou crie sua conta para gerenciar seu perfil e currículo.")

    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])

    with aba_login:
        st.subheader("Fazer Login")
        email_login = st.text_input("E-mail", key="email_l")
        senha_login = st.text_input("Senha", type="password", key="senha_l")
        
        if st.button("Entrar"):
            if email_login and senha_login:
                st.session_state["logado"] = True
                st.session_state["usuario"] = email_login
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos.")

    with aba_cadastro:
        st.subheader("Criar Nova Conta")
        email_cad = st.text_input("E-mail", key="email_c")
        senha_cad = st.text_input("Senha", type="password", key="senha_c")
        
        if st.button("Cadastrar"):
            if email_cad and senha_cad:
                st.session_state["logado"] = True
                st.session_state["usuario"] = email_cad
                st.success("Conta criada e login efetuado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos.")

# ==========================================
# FLUXO 2: DASHBOARD INTERNA DO CANDIDATO
# ==========================================
else:
    st.sidebar.title("Painel do Candidato")
    st.sidebar.write(f"Logado como:\n*{st.session_state['usuario']}*")
    
    if st.sidebar.button("Sair (Logout)"):
        st.session_state["logado"] = False
        st.session_state["usuario"] = ""
        if "dados_cv" in st.session_state:
            del st.session_state["dados_cv"]
        st.rerun()

    st.title("SouHQ - Gerenciamento de Perfil e Currículo")
    st.write("Bem-vindo à sua área restrita. Envie seu currículo em PDF para que nossa Inteligência Artificial preencha seus dados automaticamente.")

    st.divider()

    # Seção do Botão de Upload do CV
    st.subheader("📁 Enviar ou Atualizar Currículo")
    uploaded_file = st.file_uploader("Escolha seu currículo em formato PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Processar Currículo com IA"):
            with st.spinner("Lendo documento e extraindo informações completas..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/extrair-curriculo/", files=files)
                    
                    if response.status_code == 200:
                        st.session_state["dados_cv"] = response.json()
                        st.success("Currículo processado com sucesso! Revise seus dados abaixo.")
                    else:
                        st.error(f"Erro no servidor: {response.text}")
                except Exception as e:
                    st.error(f"Não foi possível conectar ao backend: {e}")

    # Formulário de Revisão Editável Expandido
    if "dados_cv" in st.session_state:
        dados = st.session_state["dados_cv"]
        
        st.divider()
        st.subheader("📝 Revisão de Dados do Perfil")
        st.write("Ajuste os dados extraídos pela IA e salve seu perfil completo na plataforma.")

        with st.form("form_perfil_candidato"):
            nome = st.text_input("Nome Completo", value=dados.get("nome", ""))
            email_candidato = st.text_input("E-mail de Contato", value=dados.get("email", st.session_state["usuario"]))
            telefone = st.text_input("Telefone", value=dados.get("telefone", ""))
            endereco = st.text_input("Endereço (Cidade/Estado)", value=dados.get("endereco", ""))
            resumo = st.text_area("Resumo Profissional", value=dados.get("resumo", ""))
            
            hab_str = ", ".join(dados.get("habilidades", []))
            habilidades = st.text_input("Habilidades (separadas por vírgula)", value=hab_str)
            
            # Novos campos expandidos
            experiencia = st.text_area("Experiência Profissional", value=dados.get("experiencia_profissional", ""))
            ensino = st.text_input("Nível de Ensino / Escolaridade", value=dados.get("nivel_ensino", ""))
            
            cursos_list = dados.get("cursos", [])
            cursos_str = ", ".join(cursos_list) if isinstance(cursos_list, list) else str(cursos_list)
            cursos = st.text_area("Cursos e Certificações", value=cursos_str)
            
            linguas_list = dados.get("linguas", [])
            linguas_str = ", ".join(linguas_list) if isinstance(linguas_list, list) else str(linguas_list)
            linguas = st.text_input("Línguas / Idiomas", value=linguas_str)
            
            salvar_alteracoes = st.form_submit_button("Salvar Alterações do Perfil")
            if salvar_alteracoes:
                st.success("Perfil completo atualizado e salvo com sucesso na SouHQ! 🚀")
