# 1. Carregar Pacotes
pacotes <- c("ggplot2", "lubridate", "dplyr", "viridis", "scales")
lapply(pacotes, function(p) {
  if (!require(p, character.only = TRUE)) install.packages(p)
  library(p, character.only = TRUE)
})

# 2. Carregar e Preparar Dados
dados <- read.csv("dados_esp32_v1.csv", sep = ";")
dados$datahora <- as.POSIXct(dados$datahora, tz = "UTC")
dados$hora <- hour(dados$datahora)
dados$dia <- as.Date(dados$datahora)
dados$mes <- month(dados$datahora)
dados$ano <- year(dados$datahora)

mes_desejado <- 5
ano_desejado <- 2024
dados_filtrados <- dados %>% filter(mes == mes_desejado, ano == ano_desejado)

# 3. Início do PDF
pdf("relatorio_analise_siapi.pdf", width = 11, height = 8.5)

# Gráfico 1
g1 <- ggplot(dados_filtrados, aes(x = datahora, y = distancia_atual)) +
  geom_line(color = "steelblue", linewidth = 0.8) +
  geom_smooth(method = "loess", se = FALSE, color = "darkred", linewidth = 1) +
  labs(title = "Nível do Rio ao Longo do Tempo", x = "Data e Hora", y = "Distância (cm)") +
  scale_x_datetime(labels = date_format("%d/%m"), date_breaks = "3 days") +
  theme_minimal()
print(g1)

# Gráfico 2
g2 <- ggplot(dados_filtrados, aes(x = chuva, y = distancia_atual)) +
  geom_point(alpha = 0.6, color = "dodgerblue4") +
  geom_smooth(method = "lm", color = "darkgreen", se = TRUE) +
  labs(title = "Relação entre Chuva e Nível do Rio", x = "Chuva (mm)", y = "Distância (cm)") +
  theme_minimal()
print(g2)

# Gráfico 3
dados_heat <- dados_filtrados %>%
  group_by(dia, hora) %>%
  summarise(media_dist = mean(distancia_atual, na.rm = TRUE), .groups = 'drop')

g3 <- ggplot(dados_heat, aes(x = hora, y = dia, fill = media_dist)) +
  geom_tile(color = "white") +
  scale_fill_viridis(option = "A", direction = -1, name = "Distância (cm)") +
  labs(title = "Mapa de Calor: Nível do Rio por Hora e Dia", x = "Hora do Dia", y = "Dia") +
  theme_minimal()
print(g3)

# Gráfico 4
g4 <- ggplot(dados_filtrados, aes(x = chuva - evaporacao, y = distancia_atual)) +
  geom_point(aes(color = temperatura), alpha = 0.7) +
  scale_color_viridis(option = "C", name = "Temperatura (°C)") +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  labs(title = "Saldo Hídrico vs Nível do Rio", x = "Chuva - Evaporação (mm)", y = "Distância (cm)") +
  theme_minimal()
print(g4)

# Modelo Linear e Diagnóstico
modelo <- lm(distancia_atual ~ chuva + evaporacao + umidade + vento + temperatura, data = dados_filtrados)
par(mfrow = c(2, 2))
plot(modelo)
par(mfrow = c(1, 1)) # reset layout

# Gráfico 6
dados_filtrados$risk <- case_when(
  dados_filtrados$distancia_atual <= 30 ~ "Alto",
  dados_filtrados$distancia_atual <= 50 ~ "Médio",
  TRUE ~ "Baixo"
)
g6 <- ggplot(dados_filtrados, aes(x = dia, fill = risk)) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c("Alto" = "red", "Médio" = "yellow", "Baixo" = "green")) +
  labs(title = "Classificação de Risco por Dia", x = "Dia", y = "Ocorrências", fill = "Risco") +
  theme_minimal()
print(g6)

# Gráfico 7
g7 <- ggplot(dados_filtrados, aes(x = datahora, y = distancia_atual)) +
  geom_line(color = "royalblue", linewidth = 1) +
  labs(title = "Evolução do Nível do Rio", x = "Data e Hora", y = "Distância (cm)") +
  theme_minimal()
print(g7)

# Gráfico 8
dados_filtrados <- dados_filtrados %>%
  arrange(datahora) %>%
  mutate(
    dist_ant = lag(distancia_atual),
    tendencia = case_when(
      distancia_atual < dist_ant ~ "Subindo",
      distancia_atual >= dist_ant ~ "Estável/Descendo",
      TRUE ~ NA_character_
    )
  )
g8 <- ggplot(dados_filtrados, aes(x = dia, fill = tendencia)) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c("Subindo" = "red", "Estável/Descendo" = "skyblue")) +
  labs(title = "Tendência Diária do Nível do Rio", x = "Dia", y = "Frequência", fill = "Tendência") +
  theme_minimal()
print(g8)

# Fechar o PDF
dev.off()
