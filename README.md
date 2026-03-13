# SMARTX CONNECTOR v1.2.0

## Overview
SMARTX CONNECTOR is a robust and scalable RFID reader management platform, built com FastAPI, voltado para integração, monitoramento e automação de dispositivos RFID. O sistema oferece alta performance, flexibilidade e recursos avançados para ambientes industriais, comerciais e laboratoriais.

---

## Estrutura do Projeto

**Principais Pastas:**

- **app/** — Código principal da aplicação:
  - **async_func/**: Funções assíncronas para operações RFID e tarefas de background.
  - **core/**: Configuração, middlewares, templates, handlers de exceção e lógica central.
  - **db/**: Gerenciamento de conexão, sessão e inicialização do banco de dados.
  - **models/**: Modelos SQLAlchemy para tags, eventos e mixins utilitários.
  - **routers/**:
    - **api/v1/**: Endpoints RESTful para dispositivos, tags, simulação e integração.
    - **pages/**: Rotas da interface web (dashboard, logs, settings, etc).
  - **schemas/**: Schemas Pydantic para validação de dados e simulação.
  - **services/**: Lógica de negócio, integração, gerenciamento de dispositivos e eventos.
    - **rfid/**: Gerenciamento de dispositivos, eventos e integração com banco/webhook.
    - **settings_service/**: Gerenciamento de configurações dinâmicas.
    - **tray/**: Integração com área de notificação/sistema.
  - **static/**: Assets do frontend (CSS, JS, imagens, sons, ícones, docs Swagger).
  - **templates/**: Templates Jinja2 para páginas, componentes e includes reutilizáveis.

- **config/** — Arquivos de configuração:
  - `config.json`: Configuração principal do sistema.
  - **devices/**: Configurações específicas de cada leitor RFID.
  - **examples/**: Exemplos de configuração para dispositivos.

- **alembic/** — Gerenciamento de migrações do banco de dados:
  - **versions/**: Scripts de migração.

- **Logs/** — Arquivos de log da aplicação.
- **scripts/** — Scripts utilitários para build, migração, formatação e inicialização.
- **tests/** — Testes unitários e de integração.

---

## Ambiente e Dependências

- **Linguagem:** Python 3.11
- **Gerenciador de pacotes:** Poetry
- **Principais dependências:**
  - FastAPI, Uvicorn, SQLAlchemy, Alembic, Jinja2, Python-Multipart, SMARTX-RFID, HTTPx, PyGame, GMQTT, Prometheus FastAPI Instrumentator, Cryptography, Passlib[bcrypt]
- **Dev dependencies:** Tomli, Ruff, PyInstaller, Pytest

---

## Instalação e Execução

```bash
# Instalar dependências
poetry install

# Executar aplicação
poetry run python main.py

# Gerar executável
poetry run python build_exe.py
```

---

## Principais Funcionalidades

- **Gerenciamento RFID:**
  - Suporte multi-protocolo (TCP/IP, Serial, USB)
  - Leitura e processamento de tags em tempo real
  - Controle de antena, potência e RSSI
  - Filtro automático de tags duplicadas
  - Validação EPC/TID

- **Interface Web:**
  - Dashboard responsivo com atualização em tempo real
  - Monitoramento de dispositivos e configuração
  - Visualização de logs com filtros e busca
  - Simulação de tags para testes e desenvolvimento
  - Documentação interativa da API (Swagger UI)

- **Integração & API:**
  - API RESTful completa
  - Integração com banco de dados (SQLAlchemy)
  - Webhook para sistemas externos
  - Conectividade MQTT para IoT
  - Métricas Prometheus
  - Persistência e políticas de limpeza configuráveis

---

## Configuração

- **config/config.json:**
  - Título, porta, URL do banco, URLs de integração, configuração de logs, dispositivos, MQTT, políticas de armazenamento.
- **config/devices/*.json:**
  - Configuração individual de cada leitor RFID (protocolo, antena, eventos, etc).
- **app/core/config.py:**
  - Carregamento dinâmico, variáveis de ambiente, atualização em runtime, validação.

---

## Endpoints Principais

- **Device Management** (`/api/v1/devices`):
  - `GET /get_devices` — Lista dispositivos registrados
  - `GET /get_device_config/{name}` — Configuração de dispositivo
  - `GET /get_device_types_list` — Tipos suportados
  - `GET /get_device_config_example/{name}` — Exemplos de configuração

- **RFID Operations** (`/api/v1/rfid`):
  - `GET /get_tags` — Tags detectadas
  - `GET /get_tag_count` — Contagem de tags
  - `POST /clear_tags` — Limpar tags
  - `GET /get_epcs` — EPCs detectados
  - `GET /get_gtin_count` — Estatísticas GTIN

- **Simulation & Testing** (`/api/v1/simulator`):
  - `POST /tag` — Simular tag
  - `POST /event` — Simular evento
  - `POST /tag_list` — Simular múltiplas tags

- **Web Interface:**
  - `/` — Dashboard
  - `/logs` — Visualização de logs
  - `/docs` — Documentação interativa

---

## Modelos de Banco de Dados

- **Tag Model** (`app/models/rfid.py`):
  - Identificação de dispositivo, EPC/TID, antena, RSSI, timestamp, índices.
- **Event Model** (`app/models/rfid.py`):
  - Log de eventos, classificação, dados JSON, timestamp automático.
- **Base Models** (`app/models/mixin.py`):
  - Funcionalidades comuns, serialização, mixins de timestamp, sessão.

---

## Desenvolvimento & Build

- **Gerenciador:** Poetry
- **Qualidade:** Ruff
- **Testes:** Pytest
- **Migrações:** Alembic
- **Build:** PyInstaller (`build_exe.py`)
- **Recursos:** Todos os diretórios, arquivos estáticos e dependências incluídos no executável.
