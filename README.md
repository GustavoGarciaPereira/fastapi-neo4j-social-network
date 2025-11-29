# 🚀 FastAPI + Neo4j Social Network

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

Uma aplicação completa de rede social construída com **FastAPI** e **Neo4j**, demonstrando o poder de bancos de dados de grafos para gerenciar relacionamentos complexos entre pessoas.

## ✨ Funcionalidades

### 🔗 Gestão de Relacionamentos
- **Cadastro de Pessoas** com interesses e informações demográficas
- **Criação de Relacionamentos** do tipo "conhece" entre pessoas
- **Visualização de Rede Social** com diferentes níveis de profundidade
- **Sistema de Recomendações** baseado em interesses em comum

### 🎯 Análises Avançadas
- **Caminhos mais curtos** entre pessoas na rede
- **Estatísticas da rede** (densidade, interesses populares, etc.)
- **Busca por interesses** em comum
- **Pessoas similares** baseado em interesses compartilhados

### 🌐 Interface Moderna
- **Dashboard responsivo** com estatísticas em tempo real
- **Visualização interativa** de relacionamentos
- **Formulários dinâmicos** para cadastro e busca
- **Design moderno** com tema escuro/claro implícito

## 🛠 Tecnologias

| Camada | Tecnologias |
|--------|-------------|
| **Backend** | FastAPI, Python 3.11, Pydantic, Uvicorn |
| **Database** | Neo4j 5.13, Cypher Query Language |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Container** | Docker, Docker Compose |
| **Dev Tools** | dotenv, async/await, CORS |

## 📁 Estrutura do Projeto

```
fastapi-neo4j-social-network/
├── app/                          # Backend FastAPI
│   ├── main.py                  # Aplicação principal + CORS
│   ├── database.py              # Conexão com Neo4j
│   ├── models.py                # Modelos Pydantic
│   ├── schemas.py               # Schemas de validação
│   └── crud.py                  # Operações de banco
├── frontend/                    # Interface web
│   ├── index.html              # Página principal
│   ├── styles/
│   │   └── style.css           # Estilos modernos
│   └── js/
│       └── app.js              # Lógica frontend
├── docker-compose.yml          # Orquestração de containers
├── Dockerfile                  # Container da aplicação
├── requirements.txt            # Dependências Python
├── populate_data.py            # Dados de exemplo
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Ou Python 3.11+ e Neo4j local

### Método 1: Docker (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fastapi-neo4j-social-network.git
cd fastapi-neo4j-social-network

# Execute com Docker Compose
docker-compose up -d

# Popular dados iniciais (opcional)
docker exec -it fastapi_app python populate_data.py
```

### Método 2: Desenvolvimento Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar Neo4j (requer Neo4j instalado)
neo4j start

# Executar aplicação
uvicorn app.main:app --reload

# Em outro terminal, servir frontend
cd frontend
python -m http.server 8080
```

## 🌐 Acesso

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **API Backend** | http://localhost:8000 | - |
| **Documentação API** | http://localhost:8000/docs | Auto-gerada |
| **Frontend** | http://localhost:8080 | - |
| **Neo4j Browser** | http://localhost:7474 | neo4j/password123 |

## 📚 Endpoints da API

### 👥 Gestão de Pessoas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/pessoas/` | Lista todas as pessoas |
| `POST` | `/pessoas/` | Cria nova pessoa |
| `GET` | `/pessoas/{id}` | Busca pessoa por ID |
| `GET` | `/pessoas/interesse/{interesse}` | Busca por interesse |

### 🔗 Relacionamentos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/pessoas/{id1}/conhece/{id2}` | Cria relacionamento |
| `GET` | `/pessoas/{id}/amigos` | Lista amigos diretos |
| `GET` | `/pessoas/{id}/rede/{profundidade}` | Rede social completa |

### 🎯 Análises
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/recomendacoes/{id}` | Recomenda amigos |
| `GET` | `/caminho/{id1}/{id2}` | Caminho entre pessoas |
| `GET` | `/estatisticas/` | Estatísticas da rede |
| `GET` | `/pessoas/{id}/similares` | Pessoas com interesses similares |

## 💡 Exemplos de Uso

### Criar uma pessoa
```bash
curl -X POST "http://localhost:8000/pessoas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "idade": 28,
    "cidade": "São Paulo",
    "interesses": ["programação", "música", "esportes"]
  }'
```

### Buscar caminho entre pessoas
```bash
curl "http://localhost:8000/caminho/1/5"
```

### Estatísticas da rede
```bash
curl "http://localhost:8000/estatisticas/"
```

## 🎨 Funcionalidades do Frontend

### Dashboard Interativo
- **Estatísticas em tempo real** da rede social
- **Visualização de densidade** de relacionamentos
- **Interesses mais populares** na comunidade

### Gestão Visual
- **Cards interativos** para cada pessoa
- **Formulários dinâmicos** com validação
- **Busca em tempo real** por interesses

### Análises Gráficas
- **Rede social expandível** com diferentes profundidades
- **Detalhes completos** de cada pessoa
- **Sistema de recomendações** visual

## 🔧 Configuração

### Variáveis de Ambiente
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123
```

### Desenvolvimento
```bash
# Instalação do ambiente de desenvolvimento
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## 🐛 Solução de Problemas

### Erro de CORS
```python
# No app/main.py, verifique se o CORS está configurado:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Neo4j não conecta
```bash
# Verificar se o Neo4j está rodando
docker ps | grep neo4j

# Ver logs do container
docker logs neo4j_db
```

## 🤝 Contribuindo

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor
gustavo
<!-- **Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil) -->

## 🌟 Demonstrações

### Para Portfólio
Este projeto demonstra habilidades em:
- ✅ **APIs REST modernas** com FastAPI
- ✅ **Bancos de dados de grafos** com Neo4j
- ✅ **Design de sistemas** relacionais complexos
- ✅ **Desenvolvimento full-stack** integrado
- ✅ **Containerização** com Docker
- ✅ **Frontend moderno** com vanilla JS

### Próximas Melhorias
- [ ] Autenticação e autorização
- [ ] Gráficos interativos da rede
- [ ] Sistema de posts e mensagens
- [ ] API GraphQL alternativa
- [ ] Testes automatizados

---

**⭐️ Se este projeto te ajudou, deixe uma estrela no repositório!**

---

<div align="center">
  
**🚀 Desenvolvido com FastAPI + Neo4j + ❤️**

*Perfect for your portfolio!*

</div>