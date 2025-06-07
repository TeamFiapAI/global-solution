
pacotes <- c("ggplot2", "dplyr", "lubridate", "readr", "gridExtra", "reshape2")

for (pkg in pacotes) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, repos = "http://cran.rstudio.com")
    library(pkg, character.only = TRUE)
  } else {
    library(pkg, character.only = TRUE)
  }
}

# Ler os dados
dados <- read_delim("dados_esp32_v1.csv", delim = ";", col_types = cols(
  distancia_atual = col_double(),
  distancia_anterior = col_double(),
  temperatura = col_double(),
  umidade = col_double(),
  vento = col_double(),
  insolacao = col_double(),
  evaporacao = col_double(),
  chuva = col_double(),
  datahora = col_datetime(format = "%d/%m/%Y %H:%M")
))

# Preparar os dados
dados <- dados %>%
  mutate(
    ano = year(datahora),
    trimestre = quarter(datahora),
    mes = month(datahora),
    hora = hour(datahora),
    saldo_hidrico = chuva - evaporacao
  )

# Criar o PDF
pdf("analise_sensorial_siapi_R.pdf", width = 10, height = 6)

# 1. Tendencia do nivel do rio
ggplot(dados, aes(x = datahora, y = distancia_atual)) +
  geom_line(color = "blue") +
  geom_smooth(method = "loess", se = FALSE, color = "red") +
  ggtitle("Tendencia do nivel do rio") +
  xlab("Data") + ylab("Distancia atual (cm)")

# 2. Chuva trimestral por ano
chuva_trimestre <- dados %>%
  group_by(ano, trimestre) %>%
  summarise(chuva = sum(chuva, na.rm = TRUE))

ggplot(chuva_trimestre, aes(x = factor(trimestre), y = chuva, fill = factor(ano))) +
  geom_bar(stat = "identity", position = "dodge") +
  ggtitle("Chuva trimestral por ano") +
  xlab("Trimestre") + ylab("Chuva acumulada (mm)")

# 3. Saldo hidrico vs distancia do rio
ggplot(dados, aes(x = saldo_hidrico, y = distancia_atual, color = temperatura)) +
  geom_point() +
  ggtitle("Saldo hidrico vs Distancia do rio") +
  xlab("Chuva - Evaporacao") + ylab("Distancia atual (cm)")

# 4. Predicao linear simples
modelo <- lm(distancia_atual ~ temperatura + umidade + vento + evaporacao + chuva, data = dados)
predicoes <- predict(modelo, dados)
plot(predicoes, dados$distancia_atual,
     main = "Predicao vs Real - Modelo Linear",
     xlab = "Predicao", ylab = "Real")
abline(0, 1, col = "red", lty = 2)

# 5. Mapa de calor de nivel medio por hora e mes
heatmap_data <- dados %>%
  group_by(mes, hora) %>%
  summarise(nivel_medio = mean(distancia_atual, na.rm = TRUE)) %>%
  ungroup()

heatmap_matrix <- acast(heatmap_data, mes ~ hora, value.var = "nivel_medio")

filled.contour(
  t(heatmap_matrix),
  color.palette = colorRampPalette(c("white", "blue")),
  plot.title = title(main = "Mapa de calor: nivel medio por hora e mes", xlab = "Mes", ylab = "Hora do dia")
)

# 6. Semaforo de risco
dados$risco <- cut(dados$distancia_atual, breaks = c(-Inf, 30, 50, Inf), labels = c("Alto", "Medio", "Baixo"))

ggplot(dados, aes(x = as.Date(datahora), fill = risco)) +
  geom_bar() +
  scale_fill_manual(values = c("red", "orange", "green")) +
  ggtitle("Risco de transbordamento por data") +
  xlab("Data") + ylab("Frequencia")

# 7. Tendencia de subida ou descida
dados <- dados %>%
  arrange(datahora) %>%
  mutate(
    diferenca = distancia_atual - lag(distancia_atual),
    tendencia = case_when(
      diferenca < 0 ~ "Subindo",
      diferenca > 0 ~ "Descendo",
      TRUE ~ "Estavel"
    )
  )

ggplot(dados, aes(x = as.Date(datahora), fill = tendencia)) +
  geom_bar() +
  ggtitle("Tendencia do nivel do rio") +
  xlab("Data") + ylab("Frequencia")

dev.off()
