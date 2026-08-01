from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pypdf
import io
import json
from groq import Groq

app = FastAPI(title="SouHQ Backend - Portal do Candidato")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o cliente da Groq com a sua chave
client = Groq(api_key="Gsk_W9UR0gJTlb7PjH4vSrakWGdyb3FYMyrDgXgRXYuieNksognRyxJS")

class CandidatoPerfil(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: str
    resumo: str
    habilidades: list[str]
    experiencia_profissional: list[dict]
    nivel_ensino: str
    cursos: list[str]
    linguas: list[str]

@app.post("/extrair-curriculo/")
async def extrair_curriculo(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos.")
    
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = pypdf.PdfReader(pdf_file)
        
        texto_curriculo = ""
        for page in reader.pages:
            texto_curriculo += page.extract_text() or ""
            
        if not texto_curriculo.strip():
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")

        prompt = f"""
        Analise o currículo abaixo e extraia as seguintes informações em formato JSON estrito contendo exatamente estas chaves:
        - nome (string)
        - email (string)
        - telefone (string)
        - endereco (string, cidade/estado se houver)
        - resumo (string breve sobre o perfil)
        - habilidades (lista de strings)
        - experiencia_profissional (uma lista de objetos JSON, onde cada objeto tem as chaves exatas: "empresa_cargo", "periodo", "escopo")
        - nivel_ensino (string informando a escolaridade)
        - cursos (lista de strings)
        - linguas (lista de strings)

        Currículo:
        {texto_curriculo[:4000]}
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        dados = json.loads(completion.choices[0].message.content)
        return dados

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
