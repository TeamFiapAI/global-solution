
# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Previsão de Enchentes com Alerta via Telegram

## Grupo: Global Solution - Inteligência Artificial

## 👨‍🎓 Integrantes: 
- <a href="#">Fernando Gomes da Silva</a>
- <a href="#">Felipe Balthazar de Almeida</a>
- <a href="#">Guilherme Urbinatti</a> 
- <a href="#">Vinicius Burchert Vilas Boas</a> 

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="#">Nome do Tutor</a>
### Coordenador(a)
- <a href="#">Nome do Coordenador</a>

## 📜 Descrição

Este sistema tem como objetivo prever o risco de enchentes com base em dados meteorológicos como precipitação, temperatura, umidade, velocidade do vento e pressão atmosférica. Utilizando um modelo de Machine Learning treinado com dados históricos, o sistema classifica o risco de vazão como Baixo, Moderado ou Crítico. Em casos críticos, um alerta é automaticamente enviado para um grupo ou usuário via Telegram, utilizando um bot integrado.

A solução foi desenvolvida em Python com FastAPI, estruturada em módulos limpos que separam o core do modelo preditivo, regras de negócio e notificações. A API permite testar a entrada de dados em tempo real e responde com a previsão da vazão e o nível de risco correspondente. O projeto representa uma aplicação prática da Inteligência Artificial na mitigação de desastres naturais, promovendo ação preventiva em comunidades vulneráveis.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: arquivos de configuração do GitHub.
- <b>assets</b>: imagens e arquivos auxiliares (ex: base histórica .csv).
- <b>config</b>: arquivos de configuração (em desenvolvimento).
- <b>document</b>: documentação do projeto.
- <b>scripts</b>: scripts utilitários (deploy, testes).
- <b>src</b>: código-fonte principal da aplicação.
  - <b>routers</b>: controladores das rotas da API.
  - <b>services</b>: regras de negócio e orquestração.
  - <b>prediction</b>: modelo de ML e previsão de vazão.
  - <b>telegram_bot.py</b>: integração com Telegram Bot.

## 🔧 Como executar o código

Pré-requisitos:
- Python 3.10+
- Pip
- Ambiente virtual (recomendado)

Passos:

```bash
# Clone o repositório
git clone https://github.com/TeamFiapAI/global-solution.git
cd global-solution

# Instale as dependências
pip install -r requirements.txt

# Execute a API
python -m sistema.main

# Acesse a documentação interativa
http://localhost:8000/docs
```

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>