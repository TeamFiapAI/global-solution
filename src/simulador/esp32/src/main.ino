#include <Wire.h>
#include <SPI.h>
#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>

#define ECHO_PIN 16  
#define TRIG_PIN 17
float distanciaAnterior = 0;
const int intervalo = 1000;

#define DHTPIN 25
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

struct DadosAmbientais {
  float vento;       // m/s
  float insolacao;   // h
  float evaporacao;  // mm
  float chuva;       // mm
  float pressao;      // hPa
  float umidadeSolo;  // %
};

String getIdentificador() {
  uint64_t chipid = ESP.getEfuseMac();
  char id[20];
  snprintf(id, sizeof(id), "%04X%08X", (uint16_t)(chipid >> 32), (uint32_t)chipid);
  return String(id);
}

String identificador;

DadosAmbientais gerarDadosAmbientais(int cenario) {
  DadosAmbientais dados;
  switch (cenario) {
    case 1: dados.vento = random(5, 20) / 10.0; dados.insolacao = random(80, 120) / 10.0; dados.evaporacao = random(40, 70) / 10.0; dados.chuva = 0; dados.pressao = random(1010, 1025) + random(0, 10) / 10.0; dados.umidadeSolo = random(20, 40); break;
    case 2: dados.vento = random(10, 30) / 10.0; dados.insolacao = random(60, 100) / 10.0; dados.evaporacao = random(20, 50) / 10.0; dados.chuva = random(1, 20) / 10.0; dados.pressao = random(1005, 1020) + random(0, 10) / 10.0; dados.umidadeSolo = random(30, 60); break;
    case 3: dados.vento = random(20, 40) / 10.0; dados.insolacao = random(20, 60) / 10.0; dados.evaporacao = random(10, 30) / 10.0; dados.chuva = random(20, 100) / 10.0; dados.pressao = random(990, 1010) + random(0, 10) / 10.0; dados.umidadeSolo = random(50, 80); break;
    case 4: dados.vento = random(40, 100) / 10.0; dados.insolacao = random(0, 30) / 10.0; dados.evaporacao = random(0, 20) / 10.0; dados.chuva = random(100, 500) / 10.0; dados.pressao = random(970, 990) + random(0, 10) / 10.0; dados.umidadeSolo = random(70, 95); break;
    case 5: dados.vento = random(80, 200) / 10.0; dados.insolacao = random(0, 10) / 10.0; dados.evaporacao = random(0, 10) / 10.0; dados.chuva = random(500, 1500) / 10.0; dados.pressao = random(950, 970) + random(0, 10) / 10.0; dados.umidadeSolo = random(90, 100); break;
  }
  return dados;
}

void setup() {
  Serial.begin(9600);
  identificador = getIdentificador();
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  distanciaAnterior = lerDistanciaCM();

  dht.begin();

  Serial.print("Conectando-se ao Wi-Fi");
  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println(" Conectado!");
}

float lerDistanciaCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH, 30000); // timeout de 30ms
  if (duracao == 0) return -1; // sem leitura válida

  return duracao * 0.034 / 2;
}

void loop() {
  //-- HC-R04
  float distanciaAtual = lerDistanciaCM();
  if (distanciaAtual < 0) {
    Serial.println("Falha na leitura");
    delay(intervalo);
    return;
  }

  //-- DHT22
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  int cenario = random(1, 6); // 1 a 5
  DadosAmbientais dados = gerarDadosAmbientais(cenario);

  /*
    CSV ou Integracao:
    01 = distância atual (cm)
    02 = distância anterior (cm)
    03 = temperatura (°C)
    04 = umidade (%)
    05 = vento (m/s)
    06 = insolação (h)
    07 = evaporação (mm)
    08 = chuva (mm)
    09 = Pressao (hPa)
    10 = Umidade Solo (%)
  */

String linha = String(distanciaAtual) + ";" +
               String(distanciaAnterior) + ";" +
               String(temperatura, 2) + ";" +
               String(umidade, 2) + ";" +
               String(dados.vento, 2) + ";" +
               String(dados.insolacao, 2) + ";" +
               String(dados.evaporacao, 2) + ";" +
               String(dados.chuva, 2) + ";" +
               String(dados.pressao, 2) + ";" +
               String(dados.umidadeSolo, 2);

  // Exibe exatamente como antes
  Serial.println("--------------------------------------------------");
  Serial.println(linha);
  Serial.println("--------------------------------------------------");
  Serial.println("");

  // Envia como texto puro (raw string)
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.0.72:8000/dados/receber_wokwi");
    http.addHeader("Content-Type", "text/plain");

    int httpResponseCode = http.POST(linha);

    if (httpResponseCode > 0) {
      String resposta = http.getString();
      Serial.println("✅ POST enviado com sucesso!");
      Serial.println("Resposta: " + resposta);
    } else {
      Serial.print("❌ Erro ao enviar POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("❌ Wi-Fi não conectado.");
  }

  distanciaAnterior = distanciaAtual;
  delay(intervalo);
}
