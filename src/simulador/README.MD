# 🌧️ SIAPI - Simulador de Alerta e Prevenção de InundaçõesMore actions

![Arduino](https://img.shields.io/badge/arduino-3670A0?style=for-the-badge&logo=arduino&logoColor=ffdd54)
![C++](https://img.shields.io/badge/c++-3670A0?style=for-the-badge&logo=c%2B%2B&logoColor=ffdd54)
![PlatformIO](https://img.shields.io/badge/platformio-3670A0?style=for-the-badge&logo=platformio&logoColor=ffdd54)

## 📘 Descrição

Este projeto é uma simulação desenvolvida no [Wokwi](https://wokwi.com/projects/432739416827300865) com o objetivo de representar o funcionamento de um **Sistema Inteligente de Alerta e Prevenção de Inundações (SIAPI)**. A simulação busca demonstrar, com dados coerentes e cenários realistas, como sensores ambientais podem ser utilizados para detectar riscos de alagamentos e desastres naturais.

## 💡 Conceito

A proposta do SIAPI é prever situações de risco relacionadas a enchentes a partir da **análise ambiental simulada**. O sistema utiliza sensores virtuais para monitorar:

- **Nível do rio** (HC-SR04 - ultrassônico)
- **Temperatura e umidade** (DHT22)
- **Velocidade do vento** (simulado)
- **Insolação diária** (simulado)
- **Evaporação de Piche** (simulado)
- **Precipitação / Chuva (mm)** (simulado)

Cada conjunto de dados é gerado com base em **cenários predefinidos**, variando de "Tempo calmo" até "Desastre climático".

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|-----------|------------|
| [Arduino C++](https://www.arduino.cc/reference/en/) | Linguagem base do projeto |
| [PlatformIO](https://platformio.org/) | Ambiente de desenvolvimento e build |
| [Wokwi Simulator](https://wokwi.com/) | Simulador de circuitos ESP32 online |
| [ESP32 DevKit v1](https://docs.espressif.com/) | Microcontrolador simulado no projeto |
| DHT22 | Sensor de temperatura e umidade |
| HC-SR04 | Sensor de distância para medir o nível da água |

## 📊 Simulação de Dados Ambientais

Os dados climáticos são simulados de forma **coerente** com os seguintes cenários:

| Cenário | Velocidade do vento (m/s) | Insolação (h) | Evaporação (mm) | Chuva (mm) |
|--------|----------------------------|---------------|------------------|-------------|
| Calmo | 0.5 - 2.0 | 8.0 - 12.0 | 4.0 - 7.0 | 0.0 |
| Garoa | 1.0 - 3.0 | 6.0 - 10.0 | 2.0 - 5.0 | 0.1 - 2.0 |
| Chuva Fraca | 2.0 - 4.0 | 2.0 - 6.0 | 1.0 - 3.0 | 2.0 - 10.0 |
| Tempestade | 4.0 - 10.0 | 0.0 - 3.0 | 0.0 - 2.0 | 10.0 - 50.0 |
| Desastre | 8.0 - 20.0 | 0.0 - 1.0 | 0.0 - 1.0 | 50.0 - 150.0 |

## 📦 Saída no formato CSV

A cada ciclo, os dados são impressos no `Serial Monitor` no seguinte formato **CSV**:
~~~~
1.99;1.99;24.00;40.00;1.00;10.60;6.50;0.00
~~~~

### Ordem dos campos:
1. Distância atual (cm)
2. Distância anterior (cm)
3. Temperatura (°C)
4. Umidade (%)
5. Velocidade do vento (m/s)
6. Insolação (h)
7. Evaporação de Piche (mm)
8. Quantidade de chuva (mm)
9. Pressao (hpa)
10. Umidade Solo (%)

## Sensores para o projeto fisico real
## Sensores para o projeto fisico real
| Parâmetro                | Sensor / Método                     | Tipo de Sinal          |
| ------------------------ | ----------------------------------- | ---------------------- |
| Distância (nível rio)    | HC-SR04 ou JSN-SR04T                | Digital (echo/trigger) |
| Temperatura/Umidade      | DHT22 ou BME280                     | Digital / I2C          |
| Velocidade do vento      | Anemômetro (reed switch)            | Digital (pulsos)       |
| Insolação (horas de sol) | BH1750 / TSL2561 / LDR              | I2C / Analógico        |
| Evaporação de Piche      | Cálculo (sem sensor direto)         | —                      |
| Chuva (mm)               | Pluviômetro basculante (rain gauge) | Digital (pulsos)       |