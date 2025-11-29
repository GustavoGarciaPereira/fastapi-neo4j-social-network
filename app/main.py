from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import os
from . import crud, schemas, database
from .database import get_db

app = FastAPI(
    title="Relationship Manager API",
    description="API para gerenciar pessoas e relacionamentos usando Neo4j",
    version="1.0.0"
)

# Configuração CORS para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (apenas para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos do frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.on_event("startup")
async def startup_event():
    await database.init_db()

# Rota para servir o frontend
@app.get("/")
async def read_index():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend não encontrado. Execute o backend e frontend separadamente."}

@app.on_event("startup")
async def startup_event():
    await database.init_db()


@app.post("/pessoas/", response_model=schemas.Pessoa)
async def criar_pessoa(pessoa: schemas.PessoaCreate, db=Depends(get_db)):
    return await crud.criar_pessoa(db=db, pessoa=pessoa)

@app.get("/pessoas/", response_model=List[schemas.Pessoa])
async def listar_pessoas(db=Depends(get_db)):
    return await crud.get_pessoas(db=db)

@app.get("/pessoas/{pessoa_id}", response_model=schemas.Pessoa)
async def buscar_pessoa(pessoa_id: int, db=Depends(get_db)):
    pessoa = await crud.get_pessoa(db=db, pessoa_id=pessoa_id)
    if pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return pessoa

@app.post("/pessoas/{pessoa_id1}/conhece/{pessoa_id2}")
async def criar_relacionamento(pessoa_id1: int, pessoa_id2: int, db=Depends(get_db)):
    success = await crud.criar_relacionamento(db=db, pessoa_id1=pessoa_id1, pessoa_id2=pessoa_id2)
    if not success:
        raise HTTPException(status_code=400, detail="Não foi possível criar o relacionamento")
    return {"message": "Relacionamento criado com sucesso"}

@app.get("/pessoas/{pessoa_id}/amigos", response_model=List[schemas.Pessoa])
async def listar_amigos(pessoa_id: int, db=Depends(get_db)):
    return await crud.get_amigos(db=db, pessoa_id=pessoa_id)

@app.get("/recomendacoes/{pessoa_id}", response_model=List[schemas.Pessoa])
async def recomendar_amigos(pessoa_id: int, db=Depends(get_db)):
    return await crud.recomendar_amigos(db=db, pessoa_id=pessoa_id)


@app.get("/pessoas/{pessoa_id}/rede/{profundidade}")
async def rede_social(pessoa_id: int, profundidade: int = 2, db=Depends(get_db)):
    """
    Mostra toda a rede social de uma pessoa até a profundidade especificada
    """
    return await crud.get_rede_social(db=db, pessoa_id=pessoa_id, profundidade=profundidade)

@app.get("/pessoas/interesse/{interesse}")
async def buscar_por_interesse(interesse: str, db=Depends(get_db)):
    """
    Encontra pessoas por interesse em comum
    """
    return await crud.get_pessoas_por_interesse(db=db, interesse=interesse)

@app.get("/caminho/{pessoa_id1}/{pessoa_id2}")
async def caminho_entre_pessoas(pessoa_id1: int, pessoa_id2: int, db=Depends(get_db)):
    """
    Encontra o caminho mais curto entre duas pessoas
    """
    resultado = await crud.get_caminho_entre_pessoas(db=db, pessoa_id1=pessoa_id1, pessoa_id2=pessoa_id2)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Caminho não encontrado entre as pessoas")
    return resultado

@app.get("/estatisticas/")
async def estatisticas_rede(db=Depends(get_db)):
    """
    Mostra estatísticas gerais da rede social
    """
    return await crud.get_estatisticas_rede(db=db)

@app.get("/pessoas/{pessoa_id}/similares")
async def pessoas_similares(pessoa_id: int, db=Depends(get_db)):
    """
    Encontra pessoas com interesses similares
    """
    return await crud.get_pessoas_similares(db=db, pessoa_id=pessoa_id)

@app.get("/query-personalizada/")
async def query_personalizada(db=Depends(get_db)):
    """
    Exemplo de query complexa: Pessoas de SP que gostam de música e seus amigos
    """
    query = """
    MATCH (p:Pessoa)
    WHERE p.cidade = 'São Paulo' AND 'música' IN p.interesses
    OPTIONAL MATCH (p)-[:CONHECE]->(amigo:Pessoa)
    RETURN p.nome as pessoa, 
           p.interesses as interesses,
           collect(amigo.nome) as amigos
    ORDER BY size(amigos) DESC
    """
    
    session = db
    result = await session.run(query)
    records = await result.values()
    
    resultados = []
    for record in records:
        resultados.append({
            "pessoa": record[0],
            "interesses": record[1],
            "amigos": record[2] if record[2] else []
        })
    
    return resultados



@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Gestão de Relacionamentos"}