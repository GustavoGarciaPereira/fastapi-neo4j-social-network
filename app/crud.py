from typing import List, Optional
from . import schemas

async def criar_pessoa(db, pessoa: schemas.PessoaCreate):
    query = """
    CREATE (p:Pessoa {nome: $nome, idade: $idade, interesses: $interesses})
    RETURN p, id(p) as id
    """
    
    result = await db.run(query, nome=pessoa.nome, idade=pessoa.idade, interesses=pessoa.interesses)
    record = await result.single()
    
    return {
        "id": record["id"],
        "nome": record["p"]["nome"],
        "idade": record["p"]["idade"],
        "interesses": record["p"]["interesses"]
    }

async def get_pessoas(db) -> List[schemas.Pessoa]:
    query = "MATCH (p:Pessoa) RETURN p, id(p) as id"
    
    result = await db.run(query)
    records = await result.values()
    
    pessoas = []
    for record in records:
        pessoas.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"]
        })
    
    return pessoas

async def get_pessoa(db, pessoa_id: int) -> Optional[schemas.Pessoa]:
    query = "MATCH (p:Pessoa) WHERE id(p) = $pessoa_id RETURN p, id(p) as id"
    
    result = await db.run(query, pessoa_id=pessoa_id)
    record = await result.single()
    
    if record:
        return {
            "id": record["id"],
            "nome": record["p"]["nome"],
            "idade": record["p"]["idade"],
            "interesses": record["p"]["interesses"]
        }
    return None

async def criar_relacionamento(db, pessoa_id1: int, pessoa_id2: int) -> bool:
    query = """
    MATCH (p1:Pessoa), (p2:Pessoa)
    WHERE id(p1) = $pessoa_id1 AND id(p2) = $pessoa_id2
    CREATE (p1)-[:CONHECE]->(p2)
    RETURN p1, p2
    """
    
    result = await db.run(query, pessoa_id1=pessoa_id1, pessoa_id2=pessoa_id2)
    record = await result.single()
    
    return record is not None

async def get_amigos(db, pessoa_id: int) -> List[schemas.Pessoa]:
    query = """
    MATCH (p:Pessoa)-[:CONHECE]->(amigo:Pessoa)
    WHERE id(p) = $pessoa_id
    RETURN amigo, id(amigo) as id
    """
    
    result = await db.run(query, pessoa_id=pessoa_id)
    records = await result.values()
    
    amigos = []
    for record in records:
        amigos.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"]
        })
    
    return amigos

async def recomendar_amigos(db, pessoa_id: int) -> List[schemas.Pessoa]:
    query = """
    MATCH (p:Pessoa)-[:CONHECE]->(amigo:Pessoa)-[:CONHECE]->(recomendacao:Pessoa)
    WHERE id(p) = $pessoa_id AND NOT (p)-[:CONHECE]->(recomendacao) AND p <> recomendacao
    RETURN DISTINCT recomendacao, id(recomendacao) as id
    LIMIT 5
    """
    
    result = await db.run(query, pessoa_id=pessoa_id)
    records = await result.values()
    
    recomendacoes = []
    for record in records:
        recomendacoes.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"]
        })
    
    return recomendacoes

async def get_rede_social(db, pessoa_id: int, profundidade: int = 2):
    """
    Mostra toda a rede social de uma pessoa até uma profundidade específica
    """
    query = """
    MATCH (p:Pessoa)-[:CONHECE*1..$profundidade]-(conexao:Pessoa)
    WHERE id(p) = $pessoa_id AND p <> conexao
    RETURN DISTINCT conexao, id(conexao) as id
    ORDER BY conexao.nome
    """
    
    result = await db.run(query, pessoa_id=pessoa_id, profundidade=profundidade)
    records = await result.values()
    
    conexoes = []
    for record in records:
        conexoes.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"],
            "cidade": record[0].get("cidade", "Não informada")
        })
    
    return conexoes

async def get_pessoas_por_interesse(db, interesse: str):
    """
    Encontra pessoas por interesse em comum
    """
    query = """
    MATCH (p:Pessoa)
    WHERE $interesse IN p.interesses
    RETURN p, id(p) as id
    ORDER BY p.nome
    """
    
    result = await db.run(query, interesse=interesse)
    records = await result.values()
    
    pessoas = []
    for record in records:
        pessoas.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"],
            "cidade": record[0].get("cidade", "Não informada")
        })
    
    return pessoas

async def get_caminho_entre_pessoas(db, pessoa_id1: int, pessoa_id2: int):
    """
    Encontra o caminho mais curto entre duas pessoas
    """
    query = """
    MATCH path = shortestPath((p1:Pessoa)-[:CONHECE*]-(p2:Pessoa))
    WHERE id(p1) = $pessoa_id1 AND id(p2) = $pessoa_id2
    RETURN [node IN nodes(path) | node.nome] as caminho,
           length(path) as graus_separacao
    """
    
    result = await db.run(query, pessoa_id1=pessoa_id1, pessoa_id2=pessoa_id2)
    record = await result.single()
    
    if record and record["caminho"]:
        return {
            "caminho": record["caminho"],
            "graus_separacao": record["graus_separacao"]
        }
    return None

async def get_estatisticas_rede(db):
    """
    Estatísticas gerais da rede social
    """
    query = """
    // Total de pessoas
    MATCH (p:Pessoa)
    WITH count(p) as total_pessoas
    
    // Total de relacionamentos
    MATCH ()-[r:CONHECE]->()
    WITH total_pessoas, count(r) as total_relacionamentos
    
    // Pessoas por cidade
    MATCH (p:Pessoa)
    WHERE p.cidade IS NOT NULL
    WITH total_pessoas, total_relacionamentos,
         p.cidade as cidade, count(p) as count
    ORDER BY count DESC
    WITH total_pessoas, total_relacionamentos,
         collect({cidade: cidade, quantidade: count})[0..5] as top_cidades
    
    // Interesses mais comuns
    MATCH (p:Pessoa)
    UNWIND p.interesses AS interesse
    WITH total_pessoas, total_relacionamentos, top_cidades,
         interesse, count(*) as count
    ORDER BY count DESC
    WITH total_pessoas, total_relacionamentos, top_cidades,
         collect({interesse: interesse, quantidade: count})[0..5] as top_interesses
    
    RETURN total_pessoas, total_relacionamentos, top_cidades, top_interesses
    """
    
    result = await db.run(query)
    record = await result.single()
    
    return {
        "total_pessoas": record["total_pessoas"],
        "total_relacionamentos": record["total_relacionamentos"],
        "densidade_rede": round(record["total_relacionamentos"] / record["total_pessoas"], 2),
        "top_cidades": record["top_cidades"],
        "top_interesses": record["top_interesses"]
    }

async def get_pessoas_similares(db, pessoa_id: int):
    """
    Encontra pessoas com interesses similares (não necessariamente conectadas)
    """
    query = """
    MATCH (p:Pessoa)
    WHERE id(p) = $pessoa_id
    
    // Encontrar pessoas com pelo menos 2 interesses em comum
    MATCH (similar:Pessoa)
    WHERE id(similar) <> $pessoa_id 
      AND size([interest IN p.interesses WHERE interest IN similar.interesses]) >= 2
      AND NOT (p)-[:CONHECE]-(similar)
    
    RETURN similar, id(similar) as id,
           [interest IN p.interesses WHERE interest IN similar.interesses] as interesses_comuns,
           size([interest IN p.interesses WHERE interest IN similar.interesses]) as qtd_interesses_comuns
    ORDER BY qtd_interesses_comuns DESC
    LIMIT 5
    """
    
    result = await db.run(query, pessoa_id=pessoa_id)
    records = await result.values()
    
    similares = []
    for record in records:
        similares.append({
            "id": record[1],
            "nome": record[0]["nome"],
            "idade": record[0]["idade"],
            "interesses": record[0]["interesses"],
            "cidade": record[0].get("cidade", "Não informada"),
            "interesses_comuns": record[2],
            "score_similaridade": record[3]
        })
    
    return similares