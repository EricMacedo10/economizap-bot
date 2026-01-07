# 📂 Guia para Renomear o Projeto

## ✅ Opção 1: Executar o Script (Recomendado)

1. **Abra o PowerShell** (como Administrador)
2. **Execute:**
   ```powershell
   cd "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_TABARATO\tabarato-bot"
   .\rename_project.ps1
   ```

---

## ✅ Opção 2: Comandos Manuais

### Passo 1: Criar nova pasta
```powershell
New-Item -ItemType Directory -Path "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP" -Force
```

### Passo 2: Mover o projeto
```powershell
Move-Item -Path "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_TABARATO\tabarato-bot" -Destination "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot"
```

### Passo 3: Entrar na nova pasta
```powershell
cd "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot"
```

### Passo 4: Verificar Git
```powershell
git status
```

Deve mostrar que está tudo OK! ✅

---

## ✅ Opção 3: Pelo Windows Explorer

1. Abra o Windows Explorer
2. Vá para: `C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL`
3. Crie uma nova pasta: `PROJETO_BOT_TELEGRAM_ECONOMIZAP`
4. Entre em `PROJETO_BOT_TELEGRAM_TABARATO`
5. **Arraste** a pasta `tabarato-bot` para dentro de `PROJETO_BOT_TELEGRAM_ECONOMIZAP`
6. **Renomeie** de `tabarato-bot` para `economizap-bot`

---

## 🎯 Após Renomear

### Verificar que está tudo OK:

```powershell
cd "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot"
git status
git log --oneline -5
```

### Fazer um teste:

```powershell
python src/main.py
```

---

## ✅ O Que NÃO Muda

- ❌ Histórico do Git (fica intacto)
- ❌ Commits (todos preservados)
- ❌ Repositório remoto (continua o mesmo)
- ❌ Código (funciona igual)

## ✅ O Que Muda

- ✅ Caminho local da pasta
- ✅ Consistência total do projeto

---

## 🚀 Pronto!

Depois de renomear, você terá:

**Antes:**
```
C:\...\PROJETO_BOT_TELEGRAM_TABARATO\tabarato-bot
```

**Depois:**
```
C:\...\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot
```

**Tudo funcionando perfeitamente!** 🎉

---

## ⚠️ Importante

Depois de renomear, **não esqueça** de atualizar seus atalhos/favoritos se tiver algum apontando para a pasta antiga!
