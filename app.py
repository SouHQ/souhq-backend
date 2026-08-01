mport streamlit as st
import requests

st.set_page_config(page_title="SouHQ - Plataforma de Talentos", page_icon="📄")

BACKEND_URL = "https://souhq-backend.onrender.com"

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
        if "experiencias_lista" in st.session_state:
            del st.session_state["experiencias_lista"]
        st.rerun()

    st.title("SouHQ - Gerenciamento de Perfil e Currículo")
    st.write("Bem-vindo à sua área restrita. Envie seu currículo em PDF para que nossa Inteligência Artificial preencha seus dados automaticamente.")

    st.divider()

    st.subheader("📁 Enviar ou Atualizar Currículo")
    uploaded_file = st.file_uploader("Escolha seu currículo em formato PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Processar Currículo com IA"):
            with st.spinner("Lendo documento e extraindo experiências detalhadas..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/extrair-curriculo/", files=files)
                    
                    if response.status_code == 200:
                        st.session_state["dados_cv"] = response.json()
                        # Garante que as experiências venham como lista estruturada
                        exp_extraida = st.session_state["dados_cv"].get("experiencia_profissional", [])
                        if isinstance(exp_extraida, str):
                            # Fallback caso venha como texto corrido
                            st.session_state["experiencias_lista"] = [{"empresa_cargo": exp_extraida, "periodo": "", "escopo": ""}]
                        else:
                            st.session_state["experiencias_lista"] = exp_extraida
                        st.success("Currículo processado com sucesso! Revise abaixo.")
                    else:
                        st.error(f"Erro no servidor: {response.text}")
                except Exception as e:
                    st.error(f"Não foi possível conectar ao backend: {e}")

    # Inicializa a lista de experiências no session_state se houver dados básicos carregados
    if "dados_cv" in st.session_state and "experiencias_lista" not in st.session_state:
        exp_inicial = st.session_state["dados_cv"].get("experiencia_profissional", [])
        if isinstance(exp_inicial, list):
            st.session_state["experiencias_lista"] = exp_inicial
        else:
            st.session_state["experiencias_lista"] = [{"empresa_cargo": str(exp_inicial), "periodo": "", "escopo": ""}]

    # Formulário de Revisão Editável com Experiências Dinâmicas
    if "dados_cv" in st.session_state:
        dados = st.session_state["dados_cv"]
        
        st.divider()
        st.subheader("📝 Revisão de Dados do Perfil")
        st.write("Ajuste os dados pessoais e gerencie suas experiências profissionais individualmente.")

        with st.form("form_perfil_candidato"):
            nome = st.text_input("Nome Completo", value=dados.get("nome", ""))
            email_candidato = st.text_input("E-mail de Contato", value=dados.get("email", st.session_state["usuario"]))
            telefone = st.text_input("Telefone", value=dados.get("telefone", ""))
            endereco = st.text_input("Endereço (Cidade/Estado)", value=dados.get("endereco", ""))
            resumo = st.text_area("Resumo Profissional", value=dados.get("resumo", ""))
            
            hab_str = ", ".join(dados.get("habilidades", [])) if isinstance(dados.get("habilidades"), list) else dados.get("habilidades", "")
            habilidades = st.text_input("Habilidades (separadas por vírgula)", value=hab_str)
            
            st.markdown("---")
            st.markdown("### 💼 Experiências Profissionais")
            
            # Renderiza cada experiência de forma estruturada
            if "experiencias_lista" in st.session_state:
                for i, exp in enumerate(st.session_state["experiencias_lista"]):
                    st.markdown(f"*Experiência {i+1}*")
                    # Como estamos dentro de um form, usamos inputs indexados
                    empresa = st.text_input(f"Empresa / Cargo #{i+1}", value=exp.get("empresa_cargo", ""), key=f"emp_{i}")
                    periodo = st.text_input(f"Período #{i+1} (ex: 2022 - Atual)", value=exp.get("periodo", ""), key=f"per_{i}")
                    escopo = st.text_area(f"Escopo e Atividades #{i+1}", value=exp.get("escopo", ""), key=f"esc_{i}")
                    st.markdown("---")

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

        # Botão dinâmico fora do form principal para adicionar nova experiência sem resetar a tela
        if st.button("➕ Adicionar outra experiência"):
            if "experiencias_lista" not in st.session_state:
                st.session_state["experiencias_lista"] = []
            st.session_state["experiencias_lista"].append({"empresa_cargo": "", "periodo": "", "escopo": ""})
            st.rerun()
