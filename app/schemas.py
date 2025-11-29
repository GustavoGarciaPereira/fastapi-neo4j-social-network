from pydantic import BaseModel
from typing import List, Optional

class PessoaBase(BaseModel):
    nome: str
    idade: int
    interesses: List[str]

class PessoaCreate(PessoaBase):
    pass

class Pessoa(PessoaBase):
    id: int

    class Config:
        from_attributes = True

class RelacionamentoCreate(BaseModel):
    pessoa_id1: int
    pessoa_id2: int