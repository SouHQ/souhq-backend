rom fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pypdf
import io
import os
from groq import Groq

app = FastAPI(title="SouHQ Backend - Motor de IA Gratuito")

# Inicializa o cliente da Groq com a chave gratuita
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

        # 2. Chamada para a IA gratuita da Groq
        prompt = f"""
        Analise o currículo abaixo com base nos requisitos da vaga ({vaga_requisitos}).
        Retorne estritamente um JSON com os campos:
        - "candidato": Nome do candidato encontrado no currículo.
        - "status": "Aprovado" ou "Reprovado".
        - "devolutiva_tecnica": Um parecer detalhado justificando a decisão com base nas competências encontradas.

        Currículo:
        {texto_curriculo}
        """

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um especialista em RH e recrutamento técnico."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        import json
        resultado_ia = json.loads(chat_completion.choices[0].message.content)
        return resultado_ia

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o currículo: {str(e)}")
