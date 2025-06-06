import requests

def consultar_api():
    cidades = [
        {"nome": "ORLÂNDIA", "latitude": -20.7204, "longitude": -47.8876},
        {"nome": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
        {"nome": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729},
        {"nome": "Belo Horizonte", "latitude": -19.8157, "longitude": -43.9542}
]
    # Loop para consultar todas as cidades
    for cidade in cidades:
        obter_dados_meteorologicos(cidade["nome"], cidade["latitude"], cidade["longitude"])

def obter_dados_meteorologicos(cidade, latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        temperatura = dados["current_weather"]["temperature"]
        vento = dados["current_weather"]["windspeed"]

        print(f"\nDados Meteorológicos para: {cidade}")
        print(f"Temperatura: {temperatura} °C")
        print(f"Velocidade do vento: {vento} km/h")
    else:
        print(f"\nErro ao obter dados meteorológicos para {cidade} - Código HTTP: {response.status_code}")

def obter_temperatura(cidade, latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["current_weather"]["temperature"]
    else:
        return None

