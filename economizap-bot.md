# 🤖 Projeto: Bot Telegram TáBarato - Comparador de Preços

> **Documento Técnico Completo**  
> **Status:** Planejamento  
> **Versão:** 1.0  
> **Data:** 07 de Janeiro de 2026  
> **Desenvolvedor:** Eric M.  
> **Arquiteto/Mentor:** Antigravity AI

---

## 📋 Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Objetivos e Propósito](#objetivos-e-propósito)
3. [Escopo Funcional Detalhado](#escopo-funcional-detalhado)
4. [Arquitetura do Sistema](#arquitetura-do-sistema)
5. [Stack Tecnológica](#stack-tecnológica)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
8. [Segurança e Boas Práticas](#segurança-e-boas-práticas)
9. [Plano de Desenvolvimento](#plano-de-desenvolvimento)
10. [Ambiente de Testes](#ambiente-de-testes)
11. [Critérios de Qualidade](#critérios-de-qualidade)
12. [Riscos e Mitigações](#riscos-e-mitigações)
13. [Entregáveis Finais](#entregáveis-finais)
14. [Workflow de Desenvolvimento](#workflow-de-desenvolvimento)

---

## 🎯 Visão Geral do Projeto

### O que é o TáBarato?

O **TáBarato** é um bot inteligente para Telegram que automatiza a busca e comparação de preços de produtos em múltiplos marketplaces brasileiros. O usuário simplesmente envia uma mensagem com o produto desejado, e o bot retorna o menor preço encontrado, já com cupons de desconto aplicados automaticamente.

### Problema que Resolve

- ✅ **Para Usuários:** Economiza tempo procurando o melhor preço em várias lojas
- ✅ **Para Você:** Gera comissões através de links de afiliados
- ✅ **Para o Mercado:** Democratiza o acesso a melhores preços

### Diferenciais

1. **Automação Total:** Usuário não precisa visitar múltiplos sites
2. **Cupons Automáticos:** Aplica descontos sem o usuário precisar procurar
3. **Normalização Inteligente:** Compara produtos equivalentes de lojas diferentes
4. **Canal Automático:** Publica ofertas automaticamente para seguidores
5. **Interface Simples:** Conversa natural via Telegram

---

## 🎯 Objetivos e Propósito

### Objetivos do Projeto

#### 1. **Objetivo de Aprendizado** (Principal para você agora)
- Dominar desenvolvimento de bots Telegram
- Aprender integração com APIs REST
- Entender arquitetura de microsserviços
- Praticar boas práticas de desenvolvimento
- Construir portfólio profissional

#### 2. **Objetivo Técnico**
- Sistema 100% funcional e testado
- Código limpo, documentado e profissional
- Arquitetura escalável e manutenível
- Segurança em todas as camadas

#### 3. **Objetivo de Negócio** (Futuro)
- Portfólio para conquistar clientes
- Possível monetização via afiliados
- Base para projetos similares

---

## 📦 Escopo Funcional Detalhado

### Funcionalidades Principais

#### 1. **Busca de Produtos**

**Como funciona:**
```
Usuário: "notebook dell inspiron 15"
↓
Bot processa a busca
↓
Consulta APIs dos marketplaces
↓
Retorna resultados
```

**Detalhes técnicos:**
- Recebe mensagem de texto do usuário
- Normaliza a busca (remove acentos, caracteres especiais)
- Envia requisições paralelas para todas as APIs
- Timeout de 10 segundos por API
- Trata erros de conexão

#### 2. **Consulta em Múltiplos Marketplaces**

**Marketplaces Integrados:**
- 🟠 **Amazon Brasil** (API de Afiliados)
- 🔵 **Mercado Livre** (API Oficial)
- 🟠 **Shopee** (API de Afiliados)
- 🔴 **AliExpress** (API de Afiliados)

**Para cada marketplace:**
- Busca produtos relacionados
- Extrai: nome, preço, imagem, link
- Aplica filtros de relevância
- Adiciona link de afiliado

#### 3. **Normalização de Produtos**

**Problema:** Mesmo produto tem nomes diferentes em cada loja

**Solução:**
```python
# Exemplo de normalização
"Notebook Dell Inspiron 15 i5 8GB" (Amazon)
"DELL INSPIRON 15 INTEL CORE I5 8GB RAM" (Mercado Livre)
"Dell Inspiron 15 - i5 - 8GB" (Shopee)

↓ Normalização ↓

"dell inspiron 15 i5 8gb"
```

**Algoritmo:**
1. Converter para minúsculas
2. Remover caracteres especiais
3. Extrair palavras-chave importantes
4. Calcular similaridade (70%+ = mesmo produto)
5. Agrupar produtos equivalentes

#### 4. **Aplicação Automática de Cupons**

**Como funciona:**
1. Bot mantém banco de cupons ativos
2. Para cada produto, verifica se há cupom válido
3. Aplica desconto automaticamente
4. Mostra preço original vs. preço com cupom

**Exemplo:**
```
Produto: R$ 1.500,00
Cupom: TECH10 (-10%)
Preço Final: R$ 1.350,00✅
Economia: R$ 150,00
```

#### 5. **Comparação de Preços**

**Lógica:**
1. Agrupa produtos normalizados
2. Compara preços finais (com cupons)
3. Considera frete (se disponível na API)
4. Ordena do menor para o maior
5. Retorna APENAS o melhor preço

#### 6. **Resposta ao Usuário**

**Formato da Resposta:**
```
🎯 Melhor Preço Encontrado!

📦 Notebook Dell Inspiron 15 i5 8GB
💰 R$ 2.899,00
🏪 Mercado Livre
🎟️ Cupom aplicado: -R$ 150,00
💵 Preço final: R$ 2.749,00

🔗 [Comprar Agora](link-afiliado)

⏰ Preço verificado há 2 minutos
```

**Elementos:**
- Emoji para facilitar leitura
- Nome do produto
- Loja onde está mais barato
- Preço original e final
- Economia com cupom
- Link de afiliado
- Timestamp da consulta

#### 7. **Publicação Automática em Canal**

**Quando publicar:**
- Produtos com desconto > 30%
- Ofertas relâmpago detectadas
- Cupons novos adicionados
- Produtos mais buscados

**Formato do post:**
```
🔥 OFERTA IMPERDÍVEL! 🔥

📱 iPhone 13 128GB
💰 De: R$ 4.999,00
💵 Por: R$ 3.499,00
📉 30% OFF

🏪 Amazon Brasil
🎟️ Cupom: TECH500

⏰ Oferta válida até 23:59

👉 [COMPRAR AGORA](link)
```

---

## 🏗️ Arquitetura do Sistema

### Visão Geral

```
┌─────────────────┐
│   TELEGRAM      │
│   (Interface)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   BOT HANDLER   │
│  (Recebe msgs)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  SEARCH ENGINE  │
│ (Processa busca)│
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────┐
│     API INTEGRATIONS            │
│  ┌──────┬──────┬──────┬──────┐ │
│  │Amazon│ ML   │Shopee│ Ali  │ │
│  └──────┴──────┴──────┴──────┘ │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────┐
│  NORMALIZER     │
│ (Agrupa prods)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  PRICE COMPARE  │
│ (Melhor preço)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  RESPONSE GEN   │
│ (Formata resp)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   DATABASE      │
│ (Histórico)     │
└─────────────────┘
```

### Componentes Principais

#### 1. **Bot Handler** (Gerenciador do Bot)
**Responsabilidade:** Receber e processar mensagens do Telegram

**Funções:**
- Inicializar conexão com Telegram
- Receber mensagens dos usuários
- Validar comandos
- Rotear para funções apropriadas
- Enviar respostas

**Tecnologia:** `python-telegram-bot` library

#### 2. **Search Engine** (Motor de Busca)
**Responsabilidade:** Processar e otimizar buscas

**Funções:**
- Normalizar texto de busca
- Extrair palavras-chave
- Preparar queries para cada API
- Gerenciar cache de buscas recentes

#### 3. **API Integrations** (Integrações)
**Responsabilidade:** Comunicar com marketplaces

**Para cada marketplace:**
- Módulo independente
- Autenticação específica
- Parsing de respostas
- Tratamento de erros
- Rate limiting

#### 4. **Normalizer** (Normalizador)
**Responsabilidade:** Identificar produtos equivalentes

**Funções:**
- Comparar nomes de produtos
- Calcular similaridade
- Agrupar produtos iguais
- Extrair especificações

#### 5. **Price Comparator** (Comparador)
**Responsabilidade:** Encontrar melhor preço

**Funções:**
- Aplicar cupons
- Calcular preço final
- Considerar frete
- Ordenar resultados
- Selecionar melhor oferta

#### 6. **Response Generator** (Gerador de Respostas)
**Responsabilidade:** Formatar mensagens

**Funções:**
- Criar mensagem formatada
- Adicionar emojis
- Gerar botões inline
- Preparar imagens (se necessário)

#### 7. **Database** (Banco de Dados)
**Responsabilidade:** Persistir dados

**Armazena:**
- Histórico de buscas
- Cupons ativos
- Estatísticas de uso
- Cache de produtos
- Logs de erros

---

## 🛠️ Stack Tecnológica

### Linguagem Principal: **Python 3.11+**

**Por que Python?**
- ✅ Excelente para bots e APIs
- ✅ Bibliotecas maduras para Telegram
- ✅ Fácil de aprender e manter
- ✅ Grande comunidade
- ✅ Ótimo para processamento de dados

### Bibliotecas Principais

#### 1. **python-telegram-bot** (v20.x)
```python
# Gerenciamento do bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
```
**Função:** Interface com Telegram API

#### 2. **requests** (v2.31+)
```python
# Requisições HTTP
import requests
```
**Função:** Chamar APIs dos marketplaces

#### 3. **aiohttp** (v3.9+)
```python
# Requisições assíncronas
import aiohttp
```
**Função:** Múltiplas requisições paralelas (mais rápido)

#### 4. **SQLAlchemy** (v2.0+)
```python
# ORM para banco de dados
from sqlalchemy import create_engine
```
**Função:** Gerenciar banco de dados

#### 5. **python-dotenv** (v1.0+)
```python
# Variáveis de ambiente
from dotenv import load_dotenv
```
**Função:** Gerenciar configurações sensíveis

#### 6. **fuzzywuzzy** (v0.18+)
```python
# Comparação de strings
from fuzzywuzzy import fuzz
```
**Função:** Normalização de produtos

#### 7. **APScheduler** (v3.10+)
```python
# Agendamento de tarefas
from apscheduler.schedulers.asyncio import AsyncIOScheduler
```
**Função:** Publicações automáticas no canal

### Banco de Dados: **PostgreSQL**

**Por que PostgreSQL?**
- ✅ Robusto e confiável
- ✅ Gratuito (planos free disponíveis)
- ✅ Suporta JSON (para dados flexíveis)
- ✅ Excelente performance

**Alternativa:** MongoDB (se preferir NoSQL)

### Hospedagem: **Railway.app**

**Por que Railway?**
- ✅ $5 crédito grátis/mês
- ✅ Deploy automático via GitHub
- ✅ PostgreSQL incluído
- ✅ Logs em tempo real
- ✅ Fácil de usar

**Alternativas:**
- Render.com (plano free)
- Fly.io (plano free generoso)

---

## 📁 Estrutura do Projeto

```
tabarato-bot/
│
├── 📁 src/                          # Código fonte
│   ├── 📁 bot/                      # Módulos do bot
│   │   ├── __init__.py
│   │   ├── handlers.py              # Handlers de mensagens
│   │   ├── commands.py              # Comandos do bot
│   │   └── keyboards.py             # Teclados inline
│   │
│   ├── 📁 services/                 # Serviços de negócio
│   │   ├── __init__.py
│   │   ├── search_service.py       # Lógica de busca
│   │   ├── price_service.py        # Comparação de preços
│   │   └── coupon_service.py       # Gerenciamento de cupons
│   │
│   ├── 📁 integrations/             # Integrações com APIs
│   │   ├── __init__.py
│   │   ├── base_api.py             # Classe base para APIs
│   │   ├── amazon_api.py           # API Amazon
│   │   ├── mercadolivre_api.py     # API Mercado Livre
│   │   ├── shopee_api.py           # API Shopee
│   │   └── aliexpress_api.py       # API AliExpress
│   │
│   ├── 📁 models/                   # Modelos de dados
│   │   ├── __init__.py
│   │   ├── product.py              # Modelo de Produto
│   │   ├── search.py               # Modelo de Busca
│   │   └── coupon.py               # Modelo de Cupom
│   │
│   ├── 📁 database/                 # Camada de dados
│   │   ├── __init__.py
│   │   ├── connection.py           # Conexão com DB
│   │   └── repositories.py         # Repositórios
│   │
│   ├── 📁 utils/                    # Utilitários
│   │   ├── __init__.py
│   │   ├── normalizer.py           # Normalização de texto
│   │   ├── logger.py               # Sistema de logs
│   │   └── validators.py           # Validações
│   │
│   └── main.py                      # Ponto de entrada
│
├── 📁 tests/                        # Testes automatizados
│   ├── test_bot.py
│   ├── test_services.py
│   ├── test_integrations.py
│   └── test_utils.py
│
├── 📁 docs/                         # Documentação
│   ├── ARCHITECTURE.md
│   ├── API_INTEGRATION.md
│   └── DEPLOYMENT.md
│
├── 📁 scripts/                      # Scripts auxiliares
│   ├── setup_database.py
│   └── seed_coupons.py
│
├── .env.example                     # Exemplo de variáveis
├── .gitignore                       # Arquivos ignorados
├── requirements.txt                 # Dependências Python
├── README.md                        # Documentação principal
├── Dockerfile                       # Container (opcional)
└── railway.json                     # Config Railway
```

### Explicação de Cada Pasta

#### 📁 **src/bot/**
Tudo relacionado à interface do Telegram
- `handlers.py`: Funções que respondem a mensagens
- `commands.py`: Comandos como /start, /help
- `keyboards.py`: Botões interativos

#### 📁 **src/services/**
Lógica de negócio (regras do sistema)
- `search_service.py`: Como processar buscas
- `price_service.py`: Como comparar preços
- `coupon_service.py`: Como gerenciar cupons

#### 📁 **src/integrations/**
Comunicação com APIs externas
- Um arquivo para cada marketplace
- Cada um sabe como falar com sua API específica

#### 📁 **src/models/**
Estrutura dos dados
- Define como é um Produto, uma Busca, um Cupom
- Garante consistência dos dados

#### 📁 **src/database/**
Tudo sobre banco de dados
- Como conectar
- Como salvar e buscar dados

#### 📁 **src/utils/**
Funções auxiliares usadas em vários lugares
- Normalizar texto
- Criar logs
- Validar dados

---

## 🔄 Fluxo de Funcionamento

### Fluxo Completo (Passo a Passo)

#### **Passo 1: Usuário Envia Mensagem**
```
Usuário no Telegram: "notebook gamer"
```

#### **Passo 2: Bot Recebe Mensagem**
```python
# handlers.py
async def handle_message(update, context):
    user_message = update.message.text
    # "notebook gamer"
```

#### **Passo 3: Normaliza Busca**
```python
# normalizer.py
normalized = normalize_search(user_message)
# "notebook gamer" → ["notebook", "gamer"]
```

#### **Passo 4: Envia para APIs (Paralelo)**
```python
# search_service.py
async def search_all_marketplaces(query):
    tasks = [
        amazon_api.search(query),
        mercadolivre_api.search(query),
        shopee_api.search(query),
        aliexpress_api.search(query)
    ]
    results = await asyncio.gather(*tasks)
```

**Cada API retorna:**
```json
{
  "marketplace": "Amazon",
  "products": [
    {
      "name": "Notebook Gamer Acer Nitro 5",
      "price": 4299.00,
      "image": "https://...",
      "link": "https://..."
    }
  ]
}
```

#### **Passo 5: Normaliza Produtos**
```python
# normalizer.py
grouped_products = group_similar_products(all_results)
# Agrupa "Acer Nitro 5" de diferentes lojas
```

#### **Passo 6: Aplica Cupons**
```python
# coupon_service.py
for product in products:
    coupon = find_active_coupon(product.marketplace)
    if coupon:
        product.final_price = apply_discount(product.price, coupon)
```

#### **Passo 7: Compara Preços**
```python
# price_service.py
best_deal = find_best_price(grouped_products)
# Retorna o produto com menor preço final
```

#### **Passo 8: Formata Resposta**
```python
# response_generator.py
message = format_product_message(best_deal)
```

#### **Passo 9: Envia ao Usuário**
```python
# handlers.py
await update.message.reply_text(message)
```

#### **Passo 10: Salva no Banco**
```python
# database/repositories.py
save_search_history(user_id, query, best_deal)
```

#### **Passo 11: Verifica se Publica no Canal**
```python
# channel_service.py
if is_great_deal(best_deal):
    await publish_to_channel(best_deal)
```

### Tempo Total Estimado
- Receber mensagem: < 100ms
- Buscar em 4 APIs (paralelo): 2-5 segundos
- Processar e comparar: < 500ms
- Responder usuário: < 100ms

**Total: 3-6 segundos** ⚡

---

## 🔒 Segurança e Boas Práticas

### 1. **Proteção de Credenciais**

#### ❌ **NUNCA FAZER:**
```python
# ERRADO - Credenciais no código
TELEGRAM_TOKEN = "123456:ABC-DEF..."
DATABASE_URL = "postgresql://user:pass@..."
```

#### ✅ **SEMPRE FAZER:**
```python
# CORRETO - Variáveis de ambiente
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
```

**Arquivo .env (NUNCA vai pro GitHub):**
```env
TELEGRAM_TOKEN=seu_token_aqui
DATABASE_URL=sua_url_aqui
AMAZON_API_KEY=sua_chave_aqui
```

**Arquivo .env.example (VAI pro GitHub):**
```env
TELEGRAM_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
AMAZON_API_KEY=your_amazon_api_key
```

### 2. **Validação de Entrada**

```python
# Sempre validar dados do usuário
def validate_search_query(query: str) -> bool:
    # Mínimo 3 caracteres
    if len(query) < 3:
        return False
    
    # Máximo 100 caracteres
    if len(query) > 100:
        return False
    
    # Sem caracteres perigosos
    dangerous_chars = ['<', '>', ';', '&', '|']
    if any(char in query for char in dangerous_chars):
        return False
    
    return True
```

### 3. **Rate Limiting**

```python
# Limitar requisições por usuário
from collections import defaultdict
from datetime import datetime, timedelta

user_requests = defaultdict(list)

def check_rate_limit(user_id: int) -> bool:
    now = datetime.now()
    # Remove requisições antigas (> 1 minuto)
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if now - req_time < timedelta(minutes=1)
    ]
    
    # Máximo 10 requisições por minuto
    if len(user_requests[user_id]) >= 10:
        return False
    
    user_requests[user_id].append(now)
    return True
```

### 4. **Tratamento de Erros**

```python
# Sempre tratar erros graciosamente
async def search_marketplace(api, query):
    try:
        results = await api.search(query)
        return results
    except requests.Timeout:
        logger.warning(f"Timeout ao buscar em {api.name}")
        return []
    except requests.ConnectionError:
        logger.error(f"Erro de conexão com {api.name}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return []
```

### 5. **Logging Seguro**

```python
# NÃO logar informações sensíveis
import logging

# ❌ ERRADO
logger.info(f"Token: {TELEGRAM_TOKEN}")

# ✅ CORRETO
logger.info(f"Token: {TELEGRAM_TOKEN[:10]}...")  # Apenas primeiros caracteres
logger.info(f"Usuário {user_id} fez busca")  # Sem dados pessoais
```

### 6. **Sanitização de Dados**

```python
# Limpar dados antes de usar
import re

def sanitize_input(text: str) -> str:
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    # Trim
    text = text.strip()
    return text
```

### 7. **Proteção contra SQL Injection**

```python
# Usar ORM (SQLAlchemy) ao invés de SQL direto

# ❌ ERRADO - SQL direto
query = f"SELECT * FROM products WHERE name = '{user_input}'"

# ✅ CORRETO - ORM
from sqlalchemy import select
stmt = select(Product).where(Product.name == user_input)
```

---

## 📅 Plano de Desenvolvimento

### Metodologia: **Desenvolvimento Incremental**

Vamos construir o sistema em **fases pequenas e testáveis**, uma de cada vez.

### **FASE 1: Setup Inicial** (1-2 dias)

#### Objetivos:
- ✅ Ambiente de desenvolvimento configurado
- ✅ Projeto estruturado
- ✅ Bot básico funcionando

#### Tarefas:
1. Instalar Python 3.11+
2. Criar estrutura de pastas
3. Configurar Git e GitHub
4. Criar bot no Telegram (via BotFather)
5. Instalar dependências básicas
6. Criar bot que responde "Olá"

#### Critério de Sucesso:
- Bot responde mensagens no Telegram
- Código versionado no GitHub

---

### **FASE 2: Integração com 1 Marketplace** (2-3 dias)

#### Objetivos:
- ✅ Integrar com Mercado Livre (API mais simples)
- ✅ Buscar produtos
- ✅ Retornar resultados

#### Tarefas:
1. Criar conta de desenvolvedor Mercado Livre
2. Obter credenciais API
3. Implementar `mercadolivre_api.py`
4. Testar busca de produtos
5. Formatar resposta básica

#### Critério de Sucesso:
- Usuário busca "notebook"
- Bot retorna produtos do Mercado Livre

---

### **FASE 3: Normalização e Comparação** (2-3 dias)

#### Objetivos:
- ✅ Normalizar nomes de produtos
- ✅ Comparar preços
- ✅ Retornar melhor oferta

#### Tarefas:
1. Implementar `normalizer.py`
2. Implementar `price_service.py`
3. Testar com produtos similares
4. Formatar resposta bonita

#### Critério de Sucesso:
- Bot identifica produtos iguais
- Retorna o mais barato

---

### **FASE 4: Mais Marketplaces** (3-4 dias)

#### Objetivos:
- ✅ Integrar Amazon, Shopee, AliExpress
- ✅ Buscas paralelas (mais rápido)

#### Tarefas:
1. Implementar cada API
2. Configurar requisições assíncronas
3. Testar cada integração
4. Testar todas juntas

#### Critério de Sucesso:
- Bot busca em 4 marketplaces
- Responde em < 5 segundos

---

### **FASE 5: Sistema de Cupons** (2 dias)

#### Objetivos:
- ✅ Banco de cupons
- ✅ Aplicação automática
- ✅ Mostrar economia

#### Tarefas:
1. Criar modelo de Cupom
2. Implementar `coupon_service.py`
3. Popular banco com cupons teste
4. Integrar com comparação de preços

#### Critério de Sucesso:
- Bot aplica cupons automaticamente
- Mostra preço com desconto

---

### **FASE 6: Banco de Dados** (2 dias)

#### Objetivos:
- ✅ Persistir buscas
- ✅ Histórico de preços
- ✅ Estatísticas

#### Tarefas:
1. Configurar PostgreSQL
2. Criar modelos SQLAlchemy
3. Implementar repositórios
4. Migrar dados

#### Critério de Sucesso:
- Dados salvos corretamente
- Consultas funcionando

---

### **FASE 7: Canal Automático** (2 dias)

#### Objetivos:
- ✅ Publicar ofertas no canal
- ✅ Agendamento automático

#### Tarefas:
1. Criar canal no Telegram
2. Implementar `channel_service.py`
3. Configurar scheduler
4. Definir critérios de publicação

#### Critério de Sucesso:
- Ofertas publicadas automaticamente
- Formatação profissional

---

### **FASE 8: Testes Completos** (3-4 dias)

#### Objetivos:
- ✅ Testar TUDO
- ✅ Corrigir bugs
- ✅ Otimizar performance

#### Tarefas:
1. Testes unitários
2. Testes de integração
3. Testes de carga
4. Correção de bugs

#### Critério de Sucesso:
- 95%+ de cobertura de testes
- Zero bugs críticos

---

### **FASE 9: Documentação** (2 dias)

#### Objetivos:
- ✅ README completo
- ✅ Documentação de código
- ✅ Guia de instalação

#### Tarefas:
1. Escrever README.md
2. Documentar funções
3. Criar guia de deploy
4. Screenshots e demos

#### Critério de Sucesso:
- Qualquer pessoa consegue instalar
- Código bem documentado

---

### **FASE 10: Deploy** (1-2 dias)

#### Objetivos:
- ✅ Bot rodando 24/7
- ✅ Monitoramento ativo

#### Tarefas:
1. Configurar Railway
2. Deploy do bot
3. Configurar variáveis de ambiente
4. Testar em produção

#### Critério de Sucesso:
- Bot online e funcional
- Logs acessíveis

---

### **Cronograma Total: 20-25 dias**

```
Semana 1: Fases 1-3 (Setup + 1ª API + Normalização)
Semana 2: Fases 4-5 (Mais APIs + Cupons)
Semana 3: Fases 6-7 (Database + Canal)
Semana 4: Fases 8-10 (Testes + Docs + Deploy)
```

---

## 🧪 Ambiente de Testes

### Estratégia de Testes

#### 1. **Ambiente Local** (Desenvolvimento)
- Seu computador
- Bot de teste no Telegram
- Banco de dados local (SQLite)
- APIs em modo sandbox (quando disponível)

#### 2. **Ambiente de Staging** (Homologação)
- Railway (plano free)
- Bot de teste separado
- PostgreSQL de teste
- APIs reais com dados limitados

#### 3. **Ambiente de Produção** (Futuro)
- Railway (plano pago se necessário)
- Bot oficial
- PostgreSQL otimizado
- APIs reais

### Configuração de Ambientes

```python
# config.py
import os

class Config:
    ENV = os.getenv('ENVIRONMENT', 'development')
    
    if ENV == 'development':
        DATABASE_URL = 'sqlite:///local.db'
        DEBUG = True
        LOG_LEVEL = 'DEBUG'
    
    elif ENV == 'staging':
        DATABASE_URL = os.getenv('STAGING_DATABASE_URL')
        DEBUG = True
        LOG_LEVEL = 'INFO'
    
    elif ENV == 'production':
        DATABASE_URL = os.getenv('DATABASE_URL')
        DEBUG = False
        LOG_LEVEL = 'WARNING'
```

### Tipos de Testes

#### 1. **Testes Unitários**
Testam funções individuais

```python
# tests/test_normalizer.py
def test_normalize_product_name():
    input_name = "Notebook DELL Inspiron 15 - i5 8GB"
    expected = "notebook dell inspiron 15 i5 8gb"
    result = normalize_product_name(input_name)
    assert result == expected
```

#### 2. **Testes de Integração**
Testam módulos trabalhando juntos

```python
# tests/test_search_flow.py
async def test_full_search_flow():
    query = "notebook"
    results = await search_service.search_all(query)
    assert len(results) > 0
    assert results[0].price > 0
```

#### 3. **Testes de API**
Testam integração com APIs externas

```python
# tests/test_mercadolivre_api.py
async def test_mercadolivre_search():
    api = MercadoLivreAPI()
    results = await api.search("notebook")
    assert len(results) > 0
    assert 'price' in results[0]
```

#### 4. **Testes Manuais**
Você testando o bot no Telegram

**Checklist de Testes Manuais:**
- [ ] Bot responde ao /start
- [ ] Busca retorna resultados
- [ ] Preços estão corretos
- [ ] Links funcionam
- [ ] Cupons aplicados
- [ ] Canal recebe publicações
- [ ] Erros são tratados

---

## ✅ Critérios de Qualidade

### Antes de Considerar "Pronto"

#### 1. **Funcionalidade** (100% Obrigatório)
- [ ] Todas as features implementadas
- [ ] Busca funciona em todos os marketplaces
- [ ] Normalização identifica produtos corretamente
- [ ] Cupons aplicados automaticamente
- [ ] Canal publica ofertas
- [ ] Banco de dados salva histórico

#### 2. **Performance**
- [ ] Resposta em < 5 segundos
- [ ] Suporta 10+ usuários simultâneos
- [ ] Sem memory leaks
- [ ] Queries otimizadas

#### 3. **Confiabilidade**
- [ ] 99%+ uptime
- [ ] Tratamento de erros em todas as APIs
- [ ] Fallback quando API falha
- [ ] Logs de todos os erros

#### 4. **Segurança**
- [ ] Nenhuma credencial no código
- [ ] Validação de todas as entradas
- [ ] Rate limiting implementado
- [ ] Logs não expõem dados sensíveis

#### 5. **Código**
- [ ] Código limpo e legível
- [ ] Funções documentadas
- [ ] Sem código duplicado
- [ ] Segue PEP 8 (padrão Python)

#### 6. **Testes**
- [ ] 90%+ cobertura de testes
- [ ] Todos os testes passando
- [ ] Testes de edge cases
- [ ] Testes de erro

#### 7. **Documentação**
- [ ] README completo
- [ ] Guia de instalação
- [ ] Documentação de API
- [ ] Comentários no código

---

## ⚠️ Riscos e Mitigações

### Riscos Identificados

#### 1. **APIs Podem Mudar ou Cair**
**Probabilidade:** Alta  
**Impacto:** Alto

**Mitigação:**
- Implementar fallback para cada API
- Monitorar status das APIs
- Ter alternativas prontas
- Cache de resultados recentes

#### 2. **Rate Limiting das APIs**
**Probabilidade:** Média  
**Impacto:** Médio

**Mitigação:**
- Implementar cache inteligente
- Respeitar limites de cada API
- Distribuir requisições no tempo
- Planos pagos se necessário

#### 3. **Dificuldade de Normalização**
**Probabilidade:** Média  
**Impacto:** Médio

**Mitigação:**
- Começar com algoritmo simples
- Melhorar iterativamente
- Aceitar 80% de precisão inicial
- Machine Learning no futuro

#### 4. **Custos de Hospedagem**
**Probabilidade:** Baixa  
**Impacto:** Baixo

**Mitigação:**
- Começar com planos free
- Otimizar uso de recursos
- Monitorar custos
- Escalar só quando necessário

#### 5. **Complexidade Técnica**
**Probabilidade:** Média (você é iniciante)  
**Impacact:** Médio

**Mitigação:**
- Desenvolvimento incremental
- Testes constantes
- Documentação detalhada
- Suporte contínuo (eu!)

---

## 📦 Entregáveis Finais

### O que Você Terá no Final

#### 1. **Código Fonte Completo**
- Repositório GitHub organizado
- Código limpo e documentado
- Testes automatizados
- CI/CD configurado (opcional)

#### 2. **Bot Funcionando**
- Bot Telegram ativo 24/7
- Respondendo a buscas
- Publicando no canal
- Salvando histórico

#### 3. **Documentação Profissional**
- README.md completo
- Guia de instalação
- Documentação de arquitetura
- Guia de contribuição

#### 4. **Infraestrutura**
- Deploy no Railway
- Banco de dados PostgreSQL
- Monitoramento configurado
- Backups automáticos

#### 5. **Portfólio**
- Projeto público no GitHub
- Screenshots e demos
- Vídeo de apresentação
- Case study escrito

---

## 🔄 Workflow de Desenvolvimento

### Como Vamos Trabalhar

#### Princípios:

1. **Um Problema de Cada Vez**
   - Não vamos pular etapas
   - Cada feature 100% antes da próxima
   - Testar antes de avançar

2. **Comunicação Clara**
   - Eu explico TUDO em detalhes
   - Você pergunta quando não entender
   - Sem pressa, sem pressão

3. **Testes Constantes**
   - Testar localmente primeiro
   - Depois staging
   - Só então produção

4. **Documentação Contínua**
   - Documentar enquanto desenvolve
   - Não deixar para depois
   - Comentários no código

5. **Revisão de Código**
   - Eu reviso tudo antes de commit
   - Você entende cada linha
   - Sem "código mágico"

### Fluxo de Trabalho Típico

#### Para Cada Feature:

**1. Planejamento** (10% do tempo)
- Eu crio plano detalhado
- Você revisa e aprova
- Definimos critérios de sucesso

**2. Implementação** (60% do tempo)
- Eu escrevo código
- Explico cada parte
- Você acompanha e aprende

**3. Testes** (20% do tempo)
- Testamos juntos
- Corrigimos bugs
- Validamos funcionamento

**4. Documentação** (10% do tempo)
- Documentamos o que foi feito
- Atualizamos README
- Commit no GitHub

### Quando Resolver Múltiplos Problemas

**Eu vou SEMPRE avisar antes:**

> "Posso resolver 3 coisas de uma vez aqui:  
> 1. Adicionar validação  
> 2. Melhorar formatação  
> 3. Adicionar log  
> Você prefere que eu faça tudo junto ou uma de cada vez?"

**Você decide o ritmo!**

---

## 🎓 Aprendizado Garantido

### O que Você Vai Aprender

#### Habilidades Técnicas:
- ✅ Python avançado
- ✅ APIs REST
- ✅ Banco de dados
- ✅ Async/await
- ✅ Git e GitHub
- ✅ Deploy e DevOps
- ✅ Testes automatizados

#### Habilidades de Negócio:
- ✅ Arquitetura de software
- ✅ Planejamento de projetos
- ✅ Documentação profissional
- ✅ Boas práticas de desenvolvimento

#### Soft Skills:
- ✅ Resolução de problemas
- ✅ Pensamento sistemático
- ✅ Atenção a detalhes
- ✅ Persistência

---

## 📞 Próximos Passos

### Quando Você Voltar

**Me chame e diga:**
> "Vamos começar o projeto TáBarato!"

**Eu vou:**
1. Criar o plano de implementação da Fase 1
2. Te guiar no setup do ambiente
3. Começarmos a codificar juntos

### Preparação (Opcional)

Se quiser se preparar antes:
1. Instale Python 3.11+
2. Instale Git
3. Crie conta no GitHub
4. Crie conta no Telegram (se não tiver)

**Mas não se preocupe:** Vamos fazer tudo junto quando você voltar!

---

## 📋 Resumo Executivo

### Em Poucas Palavras:

**O que é:** Bot Telegram que compara preços em 4 marketplaces

**Tecnologia:** Python + PostgreSQL + Railway

**Tempo:** 20-25 dias de desenvolvimento

**Custo:** R$ 0 (planos gratuitos)

**Complexidade:** Média (perfeito para aprender)

**Resultado:** Portfólio profissional + conhecimento sólido

**Diferencial:** Projeto completo, testado e documentado

---

## ✨ Compromisso

**Eu me comprometo a:**
- ✅ Explicar TUDO em detalhes
- ✅ Ir no seu ritmo
- ✅ Resolver um problema de cada vez
- ✅ Testar tudo antes de produção
- ✅ Criar documentação completa
- ✅ Te ensinar, não só fazer por você

**Você se compromete a:**
- ✅ Fazer perguntas quando não entender
- ✅ Testar o que desenvolvemos
- ✅ Seguir o workflow combinado
- ✅ Ter paciência com o processo

---

**Vamos construir algo incrível juntos! 🚀**

*Documento criado em: 07/01/2026*  
*Versão: 1.0*  
*Status: Aguardando início do desenvolvimento*
