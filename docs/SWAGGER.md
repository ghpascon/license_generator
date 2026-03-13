<img src="/static/images/logo.png" alt="Logo" class="img-fluid" style="height: 50px;" />

# 📡 SMARTX CONNECTOR
[**HOME**](/) | [**LOGS**](/logs) | [**API DOCS**](/docs)

**SMARTX CONNECTOR** é uma solução profissional para gestão de leitores RFID, focada em alta performance, escalabilidade, integração e monitoramento em tempo real.

---

## ⚙️ Funcionamento Geral

O SMARTX CONNECTOR atua como middleware entre leitores RFID físicos e sistemas de gestão, oferecendo:

### 🔌 Conectividade Universal
- Suporte a múltiplos protocolos: TCP/IP, Serial, USB
- Conexão simultânea com vários dispositivos
- Monitoramento de saúde e auto-reconexão

### 📊 Processamento Inteligente
- Filtro automático de tags duplicadas
- Validação em tempo real de EPC/TID
- Controle de antena e potência
- Monitoramento RSSI para análise de proximidade

### 🔄 Integração Flexível
- Suporte a bancos: SQLite, MySQL, PostgreSQL
- Webhook com retry
- MQTT para IoT
- API RESTful completa
- Monitoramento e logging estruturado

---

### 🧪 Testes & Simulação

Ideal para:
- Integração sem hardware
- Desenvolvimento e debugging
- Validação de fluxo de dados
- Treinamento e demonstração
- Testes de carga com múltiplas tags

---

## 🔄 Fluxo Operacional

1. **Configuração**: Definição de dispositivos e parâmetros
2. **Conexão**: Conexão automática aos leitores
3. **Processamento**: Captura e processamento de tags em tempo real
4. **Armazenamento**: Persistência dos dados no banco configurado
5. **Integração**: Envio de dados para sistemas externos
6. **Monitoramento**: Logs e status em tempo real

---

## 📊 Recursos da API

### Device Management
- Listagem e configuração de dispositivos RFID
- Monitoramento de status e saúde
- Exemplos e templates de configuração

### RFID Operations
- Recuperação de tags e estatísticas
- Limpeza de memória de tags e reset de contadores
- Acesso a dados EPC e GTIN

### Integração
- Recepção de dados externos
- Processamento de mensagens webhook e MQTT

### Ferramentas de Teste
- Simulação de eventos de tags
- Geração de dados para validação

---

## 🖥️ Interface Web

### Dashboard
- Monitoramento de dispositivos em tempo real
- Estatísticas de tags e atividades
- Indicadores de saúde do sistema

### Log Viewer
- Streaming de logs com auto-refresh
- Busca e filtros avançados
- Níveis de log coloridos

### API Documentation
- Interface interativa para testes
- Documentação completa dos endpoints
- Exemplos de requisição e resposta

---

## 🛠️ Tecnologia

- **Backend:** FastAPI + SQLAlchemy
- **Frontend:** Interface web moderna com atualização em tempo real
- **Integração:** Webhook, MQTT, suporte a bancos
- **Deploy:** Executável standalone ou instalação em servidor

---
