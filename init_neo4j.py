import asyncio
from app.database import database

async def init_sample_data():
    await database.connect()
    session = database.get_session()
    
    # Criar algumas pessoas de exemplo
    query = """
    // Limpar dados existentes
    MATCH (n) DETACH DELETE n;

    // Criar pessoas
    CREATE (p1:Pessoa {nome: 'Alice', idade: 25, interesses: ['programação', 'música']})
    CREATE (p2:Pessoa {nome: 'Bob', idade: 30, interesses: ['esportes', 'viagens']})
    CREATE (p3:Pessoa {nome: 'Carol', idade: 28, interesses: ['leitura', 'cinema']})
    CREATE (p4:Pessoa {nome: 'David', idade: 35, interesses: ['tecnologia', 'gastronomia']})
    
    // Criar relacionamentos
    CREATE (p1)-[:CONHECE]->(p2)
    CREATE (p1)-[:CONHECE]->(p3)
    CREATE (p2)-[:CONHECE]->(p4)
    CREATE (p3)-[:CONHECE]->(p4)
    
    RETURN 'Dados iniciais criados com sucesso!' as message
    """
    
    result = await session.run(query)
    record = await result.single()
    print(record["message"])
    
    await database.close()

if __name__ == "__main__":
    asyncio.run(init_sample_data())