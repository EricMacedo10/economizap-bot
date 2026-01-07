# Script para Renomear o Projeto para EconomiZap

## Passo 1: Criar nova pasta
New-Item -ItemType Directory -Path "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP" -Force

## Passo 2: Mover o projeto
Move-Item -Path "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_TABARATO\tabarato-bot" -Destination "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot"

## Passo 3: Verificar se funcionou
Set-Location "C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot"
git status

Write-Host "✅ Projeto renomeado com sucesso!" -ForegroundColor Green
Write-Host "📂 Nova localização: C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\PROJETO_BOT_TELEGRAM_ECONOMIZAP\economizap-bot" -ForegroundColor Cyan
