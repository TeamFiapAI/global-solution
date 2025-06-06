from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DadosWokwi(Base):
    __tablename__ = 'dados_wokwi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    distancia_atual_cm = Column(Float)
    distancia_anterior_cm = Column(Float)
    temperatura = Column(Float)
    umidade = Column(Float)
    vento_velocidade_ms = Column(Float)
    insolacao_h = Column(Float)
    evaporacao_piche_mm = Column(Float)
    precipitacao_mm = Column(Float)
    data_recebimento = Column(DateTime, default=datetime.utcnow)

class Predicao(Base):
    __tablename__ = 'predicoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dados_id = Column(Integer, ForeignKey('dados_wokwi.id'))
    vazao_prevista = Column(Float)
    risco = Column(String(20))
    explicabilidade = Column(Text)  # pode ser um JSON serializado
    data_predicao = Column(DateTime, default=datetime.utcnow)

class AlertaTelegram(Base):
    __tablename__ = 'alertas_telegram'
    id = Column(Integer, primary_key=True, autoincrement=True)
    predicao_id = Column(Integer, ForeignKey('predicoes.id'))
    mensagem = Column(Text)
    data_envio = Column(DateTime, default=datetime.utcnow)
