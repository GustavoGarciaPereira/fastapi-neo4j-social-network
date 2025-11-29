from neo4j import AsyncGraphDatabase
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class Database:
    def __init__(self):
        self.driver = None
        self._connection_attempts = 0
        self._max_attempts = 5
    
    async def connect(self):
        URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
        PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")
        
        while self._connection_attempts < self._max_attempts:
            try:
                self.driver = AsyncGraphDatabase.driver(
                    URI, 
                    auth=(USERNAME, PASSWORD),
                    max_connection_lifetime=3600
                )
                # Testar conexão
                await self.verify_connection()
                print("✅ Conectado ao Neo4j com sucesso!")
                return
            except Exception as e:
                self._connection_attempts += 1
                wait_time = 2 ** self._connection_attempts
                print(f"❌ Tentativa {self._connection_attempts} falhou: {e}")
                print(f"🕐 Tentando novamente em {wait_time} segundos...")
                await asyncio.sleep(wait_time)
        
        raise Exception(f"Falha ao conectar com Neo4j após {self._max_attempts} tentativas")
    
    async def verify_connection(self):
        async with self.driver.session() as session:
            await session.run("RETURN 1 as test")
    
    async def close(self):
        if self.driver:
            await self.driver.close()
    
    def get_session(self):
        if not self.driver:
            raise Exception("Database not connected")
        return self.driver.session()

database = Database()

async def init_db():
    await database.connect()

async def get_db():
    return database.get_session()