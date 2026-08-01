from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pypdf
import io
import os
from openai import OpenAI

app = FastAPI(title="SouHQ Backend - Motor de IA & SLA")

# Inicialize o cliente da OpenAI (certifique-se de configurar sua chave de API nas variáveis de ambiente)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class DevolutivaResponse(BaseModel):
    candidato: str
    status: str
    devolutiva_tecnica: str

@app.post("/api/analisar-curriculo/", response_model=DevolutivaResponse)
async def analisar_curriculo(file: UploadFile = File(...), vaga_requisitos: str = "Desenvolvedor Python Pleno"):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos.")
    
    try:
        # 1. Leitura e extração do texto do PDF enviado
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = pypdf.PdfReader(pdf_file)
        
        texto_curriculo = ""
        for page in reader.pages:
            texto_curriculo += page.extract_text() or ""
            
        if not texto_curriculo.strip():
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")

        # 2. Engenharia de Prompt para o Motor de IA da SouHQ
        prompt_sistema = (
            "Você é o motor de inteligência artificial da SouHQ, uma HRtech focada em eliminar o ghosting "
            "e fornecer devolutivas técnicas transparentes para candidatos. Analise o currículo fornecido "
            "em relação aos requisitos da vaga e produza um relatório técnico construtivo, direto, "
            "destacando pontos fortes e lacunas técnicas de forma profissional."
        )
        
        prompt_usuario = f"Requisitos da Vaga: {vaga_requisitos}\n\nCurrículo do Candidato:\n{texto_curriculo}"

        # 3. Chamada à API de IA
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.3,
        )
        
        devolutiva_gerada = response.choices[0].message.content

        return {
            "candidato": file.filename,
            "status": "Processado com Sucesso",
            "devolutiva_tecnica": devolutiva_gerada
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o currículo: {str(e)}")
