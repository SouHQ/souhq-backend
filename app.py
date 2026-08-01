import streamlit as st
import requests

st.set_page_config(
    page_title="SouHQ - A Nova Era das HRtechs & Soluções Inteligentes", 
    page_icon="🚀",
    layout="wide"
)

# Estilização CSS personalizada com a identidade visual oficial SouHQ (#0b0f0e e verde #39FF14)
st.markdown("""
    <style>
    /* Fundo geral da aplicação */
    .stApp {
        background-color: #0b0f0e;
        color: #f1f5f9;
    }
    
    /* Títulos principais */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Seção de Pilares / Título secundário */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #39FF14;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    /* Cards de valor */
    .card-box {
        background-color: #121a17;
        border: 1px solid #1e332b;
        padding: 1.8rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }
    .card-box:hover {
        border-color: #39FF14;
    }
    
    /* Customização de botões primários do Streamlit para o verde #39FF14 da SouHQ */
    .stButton > button {
        background-color: #39FF14;
        color: #0b0f0e;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #32e011;
        color: #0b0f0e;
    }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "https://souhq-backend.onrender.com"

# Inicializar estados da sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""
if "tipo_perfil" not in st.session_state:
    st.session_state["tipo_perfil"] = None

# ==========================================
# HOME PAGE / LANDING PAGE (Identidade SouHQ)
# ==========================================
if not st.session_state["logado"] and st.session_state["tipo_perfil"] is None:
    
    # Hero Section
    st.markdown('<p class="hero-title">SouHQ: A Nova Era das HRtechs & Soluções Inteligentes</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">A SouHQ garante feedback técnico para 100% dos candidatos. Sem silêncio. Apenas respeito.</p>', unsafe_allow_html=True)
    
    # Seção dos 3 Pilares com o cabeçalho exato solicitado
    st.markdown('<p class="section-title">A Tecnologia por Trás do Respeito</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card-box">
                <h3 style="color: #39FF14; font-size: 1.05rem; margin-bottom: 1rem;">📄 PDF PARSER AUTOMATIZADO</h3>
                <p style="color: #94a3b8; font-size: 0.92rem;">Leitura instantânea e estruturação de currículos e portfólios no momento da candidatura.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="card-box">
                <h3 style="color: #39FF14; font-size: 1.05rem; margin-bottom: 1rem;">🤖 DEVOLUTIVA TÉCNICA POR IA</h3>
                <p style="color: #94a3b8; font-size: 0.92rem;">Inteligência artificial treinada para gerar análises técnicas reais e construtivas para 100% dos candidatos.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="card-box">
                <h3 style="color: #39FF14; font-size: 1.05rem; margin-bottom: 1rem;">⏱️ GARANTIA DE SLA (TIME-TO-RESPECT)</h3>
                <p style="color: #94a3b8; font-size: 0.92rem;">Cronômetro e pipeline em tempo real, eliminando o silêncio e garantindo transparência total.</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.divider()
    
    # Seção de Acesso Dinâmico (Escolha de Perfil)
    st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem; color: #ffffff;'>Como você deseja acessar a SouHQ?</h3>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("👤 Sou Candidato (Gerenciar Perfil e CV)", use_container_width=True):
            st.session_state["tipo_perfil"] = "candidato"
            st.rerun()
            
    with col_b:
        if st.button("🏢 Sou Empresa (Cadastrar Vagas e Recrutar)", use_container_width=True):
            st.session_state["tipo_perfil"] = "empresa"
            st.rerun()

# ==========================================
# FLUXO DE AUTENTICAÇÃO E PAINEL: CANDIDATO
# ==========================================
elif st.session_state["tipo_perfil"] == "candidato":
    
    if st.button("⬅ Voltar para a Página Inicial"):
        st.session_state["tipo_perfil"] = None
        st.rerun()

    if not st.session_state["logado"]:
        st.title("SouHQ - Portal do Candidato")
        st.write("Faça login ou crie sua conta para estruturar seu currículo com inteligência artificial e ter acesso garantido a 100% de feedback técnico.")

        aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])

        with aba_login:
            st.subheader("Fazer Login")
            email_login = st.text_input("E-mail", key="email_l")
            senha_login = st.text_input("Senha", type="password", key="senha_l")
            
            if st.button("Entrar no Portal"):
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
            
            if st.button("Cadastrar Conta"):
                if email_cad and senha_cad:
                    st.session_state["logado"] = True
                    st.session_state["usuario"] = email_cad
                    st.success("Conta criada com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")
    else:
        st.sidebar.title("Painel do Candidato")
        st.sidebar.write(f"Logado como:\n*{st.session_state['usuario']}*")
        
        if st.sidebar.button("Sair (Logout)"):
            st.session_state["logado"] = False
            st.session_state["usuario"] = ""
            st.session_state["tipo_perfil"] = None
            if "dados_cv" in st.session_state:
                del st.session_state["dados_cv"]
            if "experiencias_lista" in st.session_state:
                del st.session_state["experiencias_lista"]
            st.rerun()

        st.title("SouHQ - Gerenciamento de Perfil e Currículo")
        st.write("Envie seu currículo em PDF para que nossa Inteligência Artificial preencha todos os campos automaticamente.")

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
                            exp_extraida = st.session_state["dados_cv"].get("experiencia_profissional", [])
                            if isinstance(exp_extraida, str):
                                st.session_state["experiencias_lista"] = [{"empresa_cargo": exp_extraida, "periodo": "", "escopo": ""}]
                            else:
                                st.session_state["experiencias_lista"] = exp_extraida
                            st.success("Currículo processado com sucesso! Revise abaixo.")
                        else:
                            st.error(f"Erro no servidor: {response.text}")
                    except Exception as e:
                        st.error(f"Não foi possível conectar ao backend: {e}")

        if "dados_cv" in st.session_state and "experiencias_lista" not in st.session_state:
            exp_inicial = st.session_state["dados_cv"].get("experiencia_profissional", [])
            if isinstance(exp_inicial, list):
                st.session_state["experiencias_lista"] = exp_inicial
            else:
                st.session_state["experiencias_lista"] = [{"empresa_cargo": str(exp_inicial), "periodo": "", "escopo": ""}]

        if "dados_cv" in st.session_state:
            dados = st.session_state["dados_cv"]
            
            st.divider()
            st.subheader("📝 Revisão de Dados do Perfil")
            st.write("Ajuste os dados e gerencie suas experiências profissionais individualmente.")

            with st.form("form_perfil_candidato"):
                nome = st.text_input("Nome Completo", value=dados.get("nome", ""))
                email_candidato = st.text_input("E-mail de Contato", value=dados.get("email", st.session_state["usuario"]))
                telefone = st.text_input("Telefone", value=dados.get("telefone", ""))
                endereco = st.text_input("Endereço (Cidade/Estado)", value=dados.get("endereco", ""))
                resumo = st.text_area("Resumo Profissional", value=dados.get("resumo", ""))
                
                hab_val = dados.get("habilidades", [])
                hab_str = ", ".join(hab_val) if isinstance(hab_val, list) else str(hab_val)
                habilidades = st.text_input("Habilidades (separadas por vírgula)", value=hab_str)
                
                st.markdown("---")
                st.markdown("### 💼 Experiências Profissionais")
                
                if "experiencias_lista" in st.session_state:
                    for i, exp in enumerate(st.session_state["experiencias_lista"]):
                        st.markdown(f"*Experiência {i+1}*")
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

            if st.button("➕ Adicionar outra experiência"):
                if "experiencias_lista" not in st.session_state:
                    st.session_state["experiencias_lista"] = []
                st.session_state["experiencias_lista"].append({"empresa_cargo": "", "periodo": "", "escopo": ""})
                st.rerun()

# ==========================================
# FLUXO: PAINEL DA EMPRESA (Estrutura Inicial)
# ==========================================
elif st.session_state["tipo_perfil"] == "empresa":
    if st.button("⬅ Voltar para a Página Inicial"):
        st.session_state["tipo_perfil"] = None
        st.rerun()

    st.title("SouHQ - Portal Corporativo (Empresas)")
    st.write("Bem-vindo ao painel de recrutamento inteligente. Cadastre suas vagas e cumpra o compromisso de 100% de feedback aos candidatos.")
    
    st.info("💡 Área da empresa pronta para receber o cadastro de vagas e o motor de match automático nas próximas etapas!")
