# 🚀 GUIA RÁPIDO: Do Zero à Produção em 15 Minutos

> **Para iniciantes**: Este guia assume que você NUNCA usou Python, Git ou serviços de hospedagem antes.

---

## ⚡ Opção Mais Fácil: Railway.app (RECOMENDADO)

**Por que Railway?**
- ✅ 100% grátis para começar (500 horas/mês)
- ✅ Não precisa instalar nada no seu computador
- ✅ Deploy automático do GitHub
- ✅ Banco de dados incluído

---

## 📋 Passo a Passo (15 minutos)

### **Passo 1: Criar seu Bot no Telegram** (3 minutos)

1. Abra o Telegram no celular ou computador
2. Procure por: `@BotFather`
3. Clique em **START**
4. Digite: `/newbot`
5. Escolha um nome (exemplo: `Meu Bot de Preços`)
6. Escolha um username que termine com `bot` (exemplo: `meubot_precos_bot`)
7. **COPIE O TOKEN** que aparece (algo como `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
   - ⚠️ **GUARDE ESSE TOKEN!** Você vai precisar dele

---

### **Passo 2: Fazer Fork do Projeto** (2 minutos)

1. Acesse: https://github.com/EricMacedo10/economizap-bot
2. Clique no botão **Fork** (canto superior direito)
3. Clique em **Create fork**
4. Pronto! Agora você tem uma cópia do projeto na sua conta

---

### **Passo 3: Criar Conta no Railway** (2 minutos)

1. Acesse: https://railway.app
2. Clique em **Login**
3. Escolha **Login with GitHub**
4. Autorize o Railway a acessar sua conta GitHub
5. Pronto! Conta criada

---

### **Passo 4: Fazer Deploy** (5 minutos)

1. No Railway, clique em **New Project**
2. Escolha **Deploy from GitHub repo**
3. Selecione o repositório `economizap-bot` (o fork que você fez)
4. Aguarde o deploy inicial (pode dar erro, é normal!)

---

### **Passo 5: Adicionar Banco de Dados** (1 minuto)

1. No seu projeto Railway, clique em **New**
2. Escolha **Database**
3. Selecione **Add PostgreSQL**
4. Pronto! O banco foi criado automaticamente

---

### **Passo 6: Configurar Variáveis de Ambiente** (2 minutos)

1. Clique no serviço do bot (não no database)
2. Vá na aba **Variables**
3. Clique em **+ New Variable**
4. Adicione estas variáveis **UMA POR VEZ**:

```
TELEGRAM_BOT_TOKEN = cole_aqui_o_token_que_voce_copiou_do_botfather
ENVIRONMENT = production
LOG_LEVEL = INFO
DATABASE_URL = ${{Postgres.DATABASE_URL}}
```

> 💡 **Dica**: Para `DATABASE_URL`, digite exatamente `${{Postgres.DATABASE_URL}}` - o Railway vai preencher automaticamente!

5. Clique em **Deploy** (botão no canto superior direito)

---

### **Passo 7: Testar o Bot** (1 minuto)

1. Abra o Telegram
2. Procure pelo username do seu bot (aquele que você criou no Passo 1)
3. Clique em **START**
4. Digite: `/start`
5. Você deve receber uma mensagem de boas-vindas! 🎉

---

## ✅ Pronto! Seu Bot Está no Ar!

Seu bot agora está rodando 24/7 na nuvem, sem precisar deixar seu computador ligado!

---

## 🧪 Como Testar

Envie mensagens para o bot:

```
Você: notebook
Bot: [Vai buscar preços de notebooks]

Você: /help
Bot: [Mostra comandos disponíveis]
```

---

## 📊 Como Ver os Logs (Se Algo Der Errado)

1. No Railway, clique no seu serviço (bot)
2. Vá na aba **Deployments**
3. Clique no deployment ativo
4. Vá em **View Logs**
5. Você verá todas as mensagens do bot

**O que procurar:**
- ✅ `Bot is now running!` = Tudo certo!
- ❌ `Missing required environment variables` = Faltou configurar alguma variável

---

## 🔧 Problemas Comuns e Soluções

### ❌ "Bot não responde"

**Solução:**
1. Verifique os logs no Railway
2. Confirme que o `TELEGRAM_BOT_TOKEN` está correto
3. Tente fazer um novo deploy (botão **Deploy** no Railway)

### ❌ "Missing required environment variables"

**Solução:**
1. Vá em **Variables** no Railway
2. Confirme que `TELEGRAM_BOT_TOKEN` está preenchido
3. Faça deploy novamente

### ❌ "Database connection failed"

**Solução:**
1. Verifique se o PostgreSQL está rodando no Railway
2. Confirme que `DATABASE_URL` está como `${{Postgres.DATABASE_URL}}`
3. Reinicie o serviço

---

## 💰 Quanto Custa?

**Railway Free Tier:**
- ✅ **GRÁTIS** para até 500 horas/mês
- ✅ Suficiente para 1 bot rodando 24/7 (~720 horas/mês)
- ⚠️ Você vai precisar de um cartão de crédito para verificação (mas não será cobrado)

**Se ultrapassar o limite:**
- Railway Pro: $5/mês (sem limites)

---

## 🔒 Segurança - IMPORTANTE!

### ✅ O QUE FAZER:
- Guarde seu `TELEGRAM_BOT_TOKEN` em segredo
- Use variáveis de ambiente no Railway
- Nunca compartilhe seu token publicamente

### ❌ O QUE NÃO FAZER:
- **NUNCA** coloque o token diretamente no código
- **NUNCA** compartilhe o token em fóruns ou grupos
- **NUNCA** commite o arquivo `.env` no GitHub

---

## 📱 Próximos Passos (Opcional)

### 1. Adicionar APIs de Marketplaces

Para o bot buscar preços reais, você precisa de credenciais de API:

- **Mercado Livre**: https://developers.mercadolivre.com.br/
- **Amazon**: https://affiliate-program.amazon.com.br/

Consulte o arquivo [`API_CREDENTIALS.md`](tabarato-bot/docs/API_CREDENTIALS.md) para instruções detalhadas.

### 2. Criar um Canal no Telegram

Para o bot postar ofertas automaticamente:

1. Crie um canal no Telegram
2. Adicione seu bot como administrador
3. Adicione a variável `TELEGRAM_CHANNEL_ID=@seu_canal` no Railway

### 3. Personalizar Mensagens

Edite os arquivos em `tabarato-bot/src/bot/` para customizar as respostas do bot.

---

## 🆘 Precisa de Ajuda?

1. **Documentação Completa**: Veja [`DEPLOYMENT.md`](tabarato-bot/docs/DEPLOYMENT.md)
2. **Setup Detalhado**: Veja [`SETUP.md`](tabarato-bot/docs/SETUP.md)
3. **Issues no GitHub**: https://github.com/EricMacedo10/economizap-bot/issues

---

## 🎯 Checklist Final

Antes de considerar concluído, verifique:

- [ ] Bot responde ao comando `/start`
- [ ] Bot responde a buscas de produtos
- [ ] Logs no Railway não mostram erros
- [ ] Bot está rodando há pelo menos 1 hora sem parar
- [ ] Você guardou o `TELEGRAM_BOT_TOKEN` em local seguro

---

## 🎉 Parabéns!

Você acabou de colocar um bot Telegram em produção! 🚀

**Tempo total**: ~15 minutos  
**Custo**: R$ 0,00 (free tier)  
**Disponibilidade**: 24/7

---

<div align="center">

**Dúvidas?** Abra uma [issue no GitHub](https://github.com/EricMacedo10/economizap-bot/issues)

Made with ❤️ by Eric Macedo

</div>
