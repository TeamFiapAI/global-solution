
# 🤖🌧️ Sistema de Previsão de Enchentes com Alerta via Telegram

<p align="center">
<a href="https://www.fiap.com.br/">
<img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%">
</a>
</p>

## 🏫 FIAP - Faculdade de Informática e Administração Paulista

## 💡 Projeto: Global Solution - Inteligência Artificial

---

## 👨‍🎓 Integrantes
- 👨‍💻 Fernando Gomes da Silva
- 🧠 Felipe Balthazar de Almeida
- 📊 Guilherme Urbinatti
- 🔧 Vinicius Burchert Vilas Boas

## 👩‍🏫 Professores
- 🎓 Tutor: Lucas Moreira
- 🧭 Coordenador: André Chiovato

---

## 📜 Descrição

Este sistema utiliza técnicas de **Machine Learning** 🤖 aplicadas à previsão de **vazão de rios** 🌊 com base em dados meteorológicos 📡 como:

- precipitação ☔
- temperatura 🌡️
- umidade relativa 💧
- vento 🌬️
- pressão atmosférica 📉

A previsão é classificada em três níveis de risco: **Baixo**, **Moderado** e **Crítico** 🚨. Quando o risco é crítico, o sistema envia automaticamente **alertas via Telegram** 📲 utilizando um bot integrado.

---

## 🗂️ Estrutura de Pastas

```
src/
├── sistema/
│   ├── main.py                # 🚀 Inicialização da API FastAPI
│   ├── prediction/            # 🧠 Modelo de ML e previsão
│   ├── services/              # ⚙️ Lógica de negócio
│   ├── routers/               # 🌐 Endpoints da API
│   ├── telegram_bot.py        # 📲 Integração com Telegram Bot
assets/
└── history_data.csv           # 📁 Base histórica de dados
```

---

## 🔧 Como Executar

Pré-requisitos:
- Python 3.10+
- Pip
- Ambiente virtual (recomendado)

```bash
# Clone o repositório
git clone https://github.com/TeamFiapAI/global-solution.git
cd global-solution

# Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a API
python -m sistema.main

# Acesse a documentação interativa
http://localhost:8000/docs
```

---

## 📈 Exemplo de Payload (JSON)

```json
{
  "precipitacao_mm": 85.0,
  "temperatura_maxima_c": 31.5,
  "temperatura_minima_c": 22.4,
  "temperatura_media_c": 26.8,
  "temperatura_compensada_c": 27.1,
  "umidade_media_pct": 78.0,
  "umidade_minima_pct": 55.0,
  "evaporacao_mm": 4.2,
  "insolacao_horas": 6.5,
  "vento_velocidade_ms": 2.1,
  "pressao_hpa": 1012.3,
  "umidade_solo_pct": 42.7
}
```

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
