import asyncio
from app.database import database

async def populate_sample_data():
    await database.connect()
    session = database.get_session()
    
    try:
        # Query 1: Limpar o banco
        query_clean = "MATCH (n) DETACH DELETE n"
        await session.run(query_clean)
        print("✅ Banco limpo com sucesso!")
        
        # Query 2: Criar pessoas
        query_create_people = """
        CREATE (alice:Pessoa {nome: 'Alice Silva', idade: 28, interesses: ['programação', 'música', 'viagens'], cidade: 'São Paulo'})
        CREATE (bob:Pessoa {nome: 'Bob Santos', idade: 32, interesses: ['esportes', 'tecnologia', 'cerveja'], cidade: 'Rio de Janeiro'})
        CREATE (carol:Pessoa {nome: 'Carol Oliveira', idade: 25, interesses: ['leitura', 'cinema', 'música'], cidade: 'São Paulo'})
        CREATE (david:Pessoa {nome: 'David Costa', idade: 35, interesses: ['tecnologia', 'gastronomia', 'viagens'], cidade: 'Belo Horizonte'})
        CREATE (eva:Pessoa {nome: 'Eva Pereira', idade: 29, interesses: ['yoga', 'natureza', 'culinária'], cidade: 'Rio de Janeiro'})
        CREATE (felipe:Pessoa {nome: 'Felipe Lima', idade: 31, interesses: ['esportes', 'música', 'festas'], cidade: 'São Paulo'})
        CREATE (gina:Pessoa {nome: 'Gina Rodrigues', idade: 27, interesses: ['arte', 'cinema', 'tecnologia'], cidade: 'Porto Alegre'})
        RETURN 'Pessoas criadas' as result
        """
        await session.run(query_create_people)
        print("✅ Pessoas criadas com sucesso!")
        
        # Query 3: Criar relacionamentos
        query_create_relationships = """
        MATCH (alice:Pessoa {nome: 'Alice Silva'})
        MATCH (bob:Pessoa {nome: 'Bob Santos'})
        MATCH (carol:Pessoa {nome: 'Carol Oliveira'})
        MATCH (david:Pessoa {nome: 'David Costa'})
        MATCH (eva:Pessoa {nome: 'Eva Pereira'})
        MATCH (felipe:Pessoa {nome: 'Felipe Lima'})
        MATCH (gina:Pessoa {nome: 'Gina Rodrigues'})
        
        CREATE (alice)-[:CONHECE {desde: '2022-01-15', tipo: 'amigo'}]->(bob)
        CREATE (alice)-[:CONHECE {desde: '2021-03-20', tipo: 'colega'}]->(carol)
        CREATE (bob)-[:CONHECE {desde: '2020-08-10', tipo: 'amigo'}]->(david)
        CREATE (carol)-[:CONHECE {desde: '2023-02-14', tipo: 'amigo'}]->(david)
        CREATE (david)-[:CONHECE {desde: '2022-11-05', tipo: 'colega'}]->(eva)
        CREATE (eva)-[:CONHECE {desde: '2021-07-30', tipo: 'amigo'}]->(felipe)
        CREATE (felipe)-[:CONHECE {desde: '2020-12-25', tipo: 'familia'}]->(gina)
        CREATE (bob)-[:CONHECE {desde: '2023-01-08', tipo: 'colega'}]->(felipe)
        
        CREATE (bob)-[:CONHECE {desde: '2022-01-15', tipo: 'amigo'}]->(alice)
        CREATE (carol)-[:CONHECE {desde: '2021-03-20', tipo: 'colega'}]->(alice)
        
        RETURN 'Relacionamentos criados' as result
        """
        await session.run(query_create_relationships)
        print("✅ Relacionamentos criados com sucesso!")
        
        # Query 4: Verificar dados criados
        query_verify = """
        MATCH (p:Pessoa)
        RETURN count(p) as total_pessoas
        """
        result = await session.run(query_verify)
        record = await result.single()
        total_pessoas = record["total_pessoas"]
        
        query_verify_rels = """
        MATCH ()-[r:CONHECE]->()
        RETURN count(r) as total_relacionamentos
        """
        result_rels = await session.run(query_verify_rels)
        record_rels = await result_rels.single()
        total_relacionamentos = record_rels["total_relacionamentos"]
        
        print(f"✅ Dados populados com sucesso!")
        print(f"   👥 {total_pessoas} pessoas criadas")
        print(f"   🔗 {total_relacionamentos} relacionamentos criados")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {e}")
    finally:
        await database.close()

if __name__ == "__main__":
    asyncio.run(populate_sample_data())