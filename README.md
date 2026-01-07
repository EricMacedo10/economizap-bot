# 🤖 EconomiZap Bot - Comparador de Preços Telegram

> **Bot inteligente para Telegram que automatiza a busca e comparação de preços em múltiplos marketplaces brasileiros**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://telegram.org/)

> [!TIP]
> **🚀 Quer colocar em produção AGORA?** Veja o [**GUIA RÁPIDO (15 minutos)**](QUICK_START.md) - perfeito para iniciantes!

---

## 📋 Sobre o Projeto

O **EconomiZap Bot** é um assistente inteligente que ajuda usuários a encontrar os melhores preços de produtos em múltiplos marketplaces brasileiros, tudo através de uma simples conversa no Telegram.

### 🎯 Problema que Resolve

- ✅ **Economia de Tempo**: Elimina a necessidade de visitar múltiplos sites
- ✅ **Melhores Preços**: Compara automaticamente preços entre marketplaces
- ✅ **Cupons Automáticos**: Aplica descontos sem o usuário precisar procurar
- ✅ **Simplicidade**: Interface conversacional via Telegram

### 🌟 Diferenciais

1. **Automação Total**: Busca simultânea em múltiplos marketplaces
2. **Normalização Inteligente**: Identifica produtos equivalentes com nomes diferentes
3. **Cupons Automáticos**: Aplica descontos automaticamente
4. **Canal de Ofertas**: Publica automaticamente as melhores ofertas
5. **Interface Simples**: Conversa natural via Telegram

---

## 🏗️ Arquitetura

```
┌─────────────────┐
│   TELEGRAM      │  ← Interface do usuário
└────────┬────────┘
         ↓
┌─────────────────┐
│   BOT HANDLER   │  ← Processa mensagens
└────────┬────────┘
         ↓
┌─────────────────┐
│  SEARCH ENGINE  │  ← Motor de busca
└────────┬────────┘
         ↓
┌─────────────────────────────────┐
│     API INTEGRATIONS            │
│  ┌──────┬──────┬──────┬──────┐ │
│  │Amazon│  ML  │Shopee│ Ali  │ │  ← Marketplaces
│  └──────┴──────┴──────┴──────┘ │
└─────────────────────────────────┘
         ↓
┌─────────────────┐
│  NORMALIZER     │  ← Agrupa produtos
└────────┬────────┘
         ↓
┌─────────────────┐
│  PRICE COMPARE  │  ← Encontra melhor preço
└────────┬────────┘
         ↓
┌─────────────────┐
│   DATABASE      │  ← Armazena histórico
└─────────────────┘
```

---

## 🛠️ Stack Tecnológica

### Core
- **Python 3.11+**: Linguagem principal
- **python-telegram-bot**: Interface com Telegram
- **aiohttp**: Requisições assíncronas
- **SQLAlchemy**: ORM para banco de dados

### Integrações
- **Amazon Product Advertising API**
- **Mercado Livre API**
- **Shopee Affiliate API**
- **AliExpress Affiliate API**

### Infraestrutura
- **PostgreSQL**: Banco de dados (produção)
- **SQLite**: Banco de dados (desenvolvimento)
- **Railway.app**: Hospedagem (recomendado)

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Conta no Telegram
- Credenciais de API dos marketplaces (opcional para testes)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/EricMacedo10/economizap-bot.git
cd economizap-bot
```

### Passo 2: Crie o Ambiente Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instale as Dependências

```bash
cd tabarato-bot
pip install -r requirements.txt
```

### Passo 4: Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas credenciais
# Mínimo necessário para testes:
# TELEGRAM_BOT_TOKEN=seu_token_do_botfather
```

### Passo 5: Execute o Bot

```bash
python src/main.py
```

---

## ⚙️ Configuração

### Obter Token do Telegram

1. Abra o Telegram e procure por [@BotFather](https://t.me/botfather)
2. Envie `/newbot` e siga as instruções
3. Copie o token fornecido
4. Cole no arquivo `.env` na variável `TELEGRAM_BOT_TOKEN`

### Configurar APIs dos Marketplaces (Opcional)

Para funcionalidade completa, configure as credenciais de API:

- **Mercado Livre**: [developers.mercadolivre.com.br](https://developers.mercadolivre.com.br/)
- **Amazon**: [affiliate-program.amazon.com.br](https://affiliate-program.amazon.com.br/)
- **Shopee**: [open.shopee.com](https://open.shopee.com/)
- **AliExpress**: [portals.aliexpress.com](https://portals.aliexpress.com/)

Consulte o arquivo [`.env.example`](tabarato-bot/.env.example) para todas as variáveis disponíveis.

---

## 📖 Uso

### Comandos Disponíveis

- `/start` - Inicia o bot e mostra boas-vindas
- `/help` - Mostra ajuda e comandos disponíveis
- **Envie o nome de um produto** - Busca e compara preços

### Exemplo de Uso

```
Você: notebook gamer

Bot: 🎯 Melhor Preço Encontrado!

📦 Notebook Gamer Acer Nitro 5
💰 R$ 4.299,00
🏪 Amazon Brasil
🎟️ Cupom aplicado: -R$ 200,00
💵 Preço final: R$ 4.099,00

🔗 [Comprar Agora](link-afiliado)

⏰ Preço verificado há 2 minutos
```

---

## 🔒 Segurança

Este projeto segue as melhores práticas de segurança:

- ✅ **Variáveis de Ambiente**: Credenciais nunca no código
- ✅ **Gitignore Configurado**: Arquivos sensíveis excluídos
- ✅ **Validação de Entrada**: Proteção contra injeção
- ✅ **Rate Limiting**: Proteção contra abuso
- ✅ **Logging Seguro**: Sem exposição de dados sensíveis

### ⚠️ Importante

- **NUNCA** commite o arquivo `.env`
- **NUNCA** compartilhe suas credenciais de API
- Use `.env.example` apenas como template

---

## 📁 Estrutura do Projeto

```
economizap-bot/
├── tabarato-bot/              # Código principal
│   ├── src/                   # Código fonte
│   │   ├── bot/              # Módulos do bot
│   │   ├── services/         # Lógica de negócio
│   │   ├── integrations/     # APIs dos marketplaces
│   │   ├── models/           # Modelos de dados
│   │   ├── database/         # Camada de dados
│   │   ├── utils/            # Utilitários
│   │   └── main.py           # Ponto de entrada
│   ├── tests/                # Testes automatizados
│   ├── docs/                 # Documentação adicional
│   ├── .env.example          # Template de configuração
│   ├── .gitignore            # Arquivos ignorados
│   └── requirements.txt      # Dependências Python
├── economizap-bot.md         # Documentação técnica completa
└── README.md                 # Este arquivo
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_bot.py
```

---

## 🚀 Deploy

### Railway.app (Recomendado)

1. Crie uma conta em [railway.app](https://railway.app)
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente
4. Deploy automático!

Consulte [`tabarato-bot/docs/DEPLOYMENT.md`](tabarato-bot/docs/DEPLOYMENT.md) para instruções detalhadas.

---

## 📚 Documentação Adicional

- [**Documentação Técnica Completa**](economizap-bot.md) - Arquitetura, fluxos e detalhes técnicos
- [**Guia de Setup**](tabarato-bot/docs/SETUP.md) - Configuração passo a passo
- [**Credenciais de API**](tabarato-bot/docs/API_CREDENTIALS.md) - Como obter credenciais
- [**Guia de Deploy**](tabarato-bot/docs/DEPLOYMENT.md) - Deploy em produção

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](tabarato-bot/LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Eric Macedo**

- GitHub: [@EricMacedo10](https://github.com/EricMacedo10)
- LinkedIn: [Eric Macedo](https://www.linkedin.com/in/eric-macedo/)

---

## 🙏 Agradecimentos

- Projeto desenvolvido como parte de um trabalho freelance via **99Freelas**
- Mentoria técnica e arquitetura: **Antigravity AI**
- Comunidade Python e Telegram Bot

---

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação completa](economizap-bot.md)
2. Abra uma [issue](https://github.com/EricMacedo10/economizap-bot/issues)
3. Entre em contato via LinkedIn

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Made with ❤️ by Eric Macedo

</div>
