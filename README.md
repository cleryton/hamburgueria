# Sistema Autônomo de Gestão de Pedidos para Hamburgueria

Sistema para gerenciar cardápio, estoque e pedidos de uma hamburgueria, integrando cozinha e geração automática de relatórios gerenciais.

## Tecnologias

- Python 3.12 + Flask
- PostgreSQL
- Docker / Docker Compose
- fpdf2 (relatórios em PDF)
- smtplib (envio de e-mails)

## Estrutura do projeto

```
src/
  app.py                  # ponto de entrada da aplicação
  config.py                # configurações (lidas do .env)
  database.py               # instância do SQLAlchemy
  models/                  # modelos do banco de dados
  routes/                  # rotas da API (produtos, insumos, pedidos, relatórios)
  services/                # regras de negócio (estoque, relatório, e-mail)
db/migrations/             # scripts SQL versionados
docs/                      # documentação do projeto (requisitos, etc.)
tests/                     # testes automatizados
```

## Como rodar o projeto

### 1. Configurar variáveis de ambiente
```bash
cp .env.example .env
# edite o .env com os dados do seu ambiente
```

### 2. Subir com Docker Compose
```bash
docker-compose up --build
```

### 3. Rodar as migrations
```bash
docker exec -i hamburgueria_db psql -U app -d hamburgueria < db/migrations/001_criar_tabelas.sql
docker exec -i hamburgueria_db psql -U app -d hamburgueria < db/migrations/002_seed_inicial.sql
```

A API sobe em `http://localhost:5000`.

### Rodando localmente sem Docker
```bash
python -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
```

## Principais endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/produtos` | Lista o cardápio |
| POST | `/produtos` | Cadastra um produto |
| PUT | `/produtos/<id>` | Edita um produto |
| DELETE | `/produtos/<id>` | Exclui um produto |
| GET | `/insumos` | Lista os insumos e estoque |
| POST | `/insumos` | Cadastra um insumo |
| GET | `/insumos/alertas` | Lista insumos abaixo do mínimo |
| POST | `/pedidos` | Registra um novo pedido |
| GET | `/pedidos/cozinha` | Fila de pedidos pendentes na cozinha |
| PUT | `/pedidos/<id>/status` | Atualiza o status do pedido |
| POST | `/relatorios/diario` | Gera e envia o relatório diário em PDF |

## Fluxo de trabalho do grupo

Todo o desenvolvimento segue o fluxo profissional de Git: issue → branch → commit semântico → Pull Request revisado → merge na `main`. Veja `docs/REQUISITOS.md` para o escopo completo do projeto.
