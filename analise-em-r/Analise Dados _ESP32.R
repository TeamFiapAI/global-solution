# ===============================
# 📦 1. Carregar Pacotes
# ===============================
pacotes <- c("ggplot2", "lubridate", "dplyr", "viridis")
lapply(pacotes, function(p) {
  if (!require(p, character.only = TRUE)) install.packages(p)
  library(p, character.only = TRUE)
})

# ===============================
# 📂 2. Carregar e Preparar Dados
# ===============================
dados <- read.csv("dados_esp32_v1.csv", sep = ";")
dados$datahora <- as.POSIXct(dados$datahora)
dados$hora <- hour(dados$datahora)
dados$dia <- as.Date(dados$datahora)

# ===============================
# 📊 3. Gráficos para Especialistas
# ===============================

# 1️⃣ Nível do Rio ao Longo do Tempo
ggplot(dados, aes(x = datahora, y = distancia_atual)) +
  geom_line(color = "blue") +
  geom_smooth(method = "loess", se = FALSE, color = "red") +
  labs(title = "Nível do Rio no Tempo", x = "Data", y = "Distância (cm)")

# 2️⃣ Chuva vs Nível do Rio
ggplot(dados, aes(x = chuva, y = distancia_atual)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", color = "darkgreen") +
  labs(title = "Chuva vs Nível do Rio", x = "Chuva (mm)", y = "Distância (cm)")

# 3️⃣ Mapa de Calor Hora x Dia
dados_heat <- dados %>%
  group_by(dia, hora) %>%
  summarise(media_dist = mean(distancia_atual, na.rm = TRUE))

ggplot(dados_heat, aes(x = hora, y = dia, fill = media_dist)) +
  geom_tile() +
  scale_fill_viridis(option = "A", direction = -1) +
  labs(title = "Mapa de Risco por Hora", x = "Hora", y = "Dia", fill = "Distância")

# 4️⃣ Saldo Hídrico vs Distância
ggplot(dados, aes(x = chuva - evaporacao, y = distancia_atual)) +
  geom_point(aes(color = temperatura), alpha = 0.6) +
  scale_color_viridis(option = "C", name = "Temperatura (°C)") +
  geom_smooth(method = "lm", color = "black") +
  labs(title = "Saldo Hídrico vs Distância", x = "Chuva - Evaporação", y = "Distância (cm)")

# 5️⃣ Modelo Preditivo Linear
modelo <- lm(distancia_atual ~ chuva + evaporacao + umidade + vento + temperatura, data = dados)
summary(modelo)

# ===============================
# 👥 4. Gráficos para o Público
# ===============================

# 1️⃣ Semáforo de Risco
dados$risk <- case_when(
  dados$distancia_atual <= 30 ~ "Alto",
  dados$distancia_atual <= 50 ~ "Médio",
  TRUE ~ "Baixo"
)

ggplot(dados, aes(x = as.Date(datahora), fill = risk)) +
  geom_bar() +
  scale_fill_manual(values = c("Alto" = "red", "Médio" = "yellow", "Baixo" = "green")) +
  labs(title = "Classificação de Risco", x = "Data", y = "Ocorrências", fill = "Risco")

# 2️⃣ Linha Simples de Evolução
ggplot(dados, aes(x = datahora, y = distancia_atual)) +
  geom_line(color = "blue") +
  labs(title = "Como Está o Nível do Rio?", x = "Data", y = "Distância (cm)")

# 3️⃣ Última Medição
ultima <- tail(dados[complete.cases(dados), ], 1)
cat("🌡️ Temperatura:", ultima$temperatura, "°C\n")
cat("🌧️ Chuva:", ultima$chuva, "mm\n")
cat("📏 Distância:", ultima$distancia_atual, "cm\n")

# 4️⃣ Tendência do Nível
dados <- dados %>%
  arrange(datahora) %>%
  mutate(
    dist_ant = lag(distancia_atual),
    tendencia = case_when(
      distancia_atual < dist_ant ~ "Subindo",
      distancia_atual >= dist_ant ~ "Estável/Descendo",
      TRUE ~ NA_character_
    )
  )

ggplot(dados, aes(x = datahora, fill = tendencia)) +
  geom_histogram(binwidth = 86400) +
  scale_fill_manual(values = c("Subindo" = "red", "Estável/Descendo" = "skyblue")) +
  labs(title = "Tendência do Nível", x = "Data", fill = "Tendência")
