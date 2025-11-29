from pydantic import BaseModel
from typing import Optional, List

# Modelos Pydantic para validação de dados
class PessoaBase(BaseModel):
    nome: str
    idade: int
    interesses: List[str] = []

class PessoaCreate(PessoaBase):
    pass

class Pessoa(PessoaBase):
    id: int

    class Config:
        from_attributes = True