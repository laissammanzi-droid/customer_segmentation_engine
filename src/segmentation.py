"""
segmentation.py
===============

Funções para segmentação de clientes.
"""
import pandas as pd
from datetime import datetime

def segment_customers_by_recency(df, days_active=None, days_risk=None):
    """
    Segmenta os clientes pela recência da última compra com thresholds customizáveis.
    Se não passar, sugerir uso do config externo.
    """
    from src.config import load_config
    if days_active is None or days_risk is None:
        config = load_config()
        days_active = config.get("recency_active_days", 30)
        days_risk = config.get("recency_risk_days", 90)
    df = df.copy()
    today = datetime.today().date()
    
    # Garante que a coluna esteja no formato data
    df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date']).dt.date

    # Calcula quantos dias desde a última compra
    df['days_since_last_purchase'] = df['last_purchase_date'].apply(lambda d: (today - d).days)

    # Função interna para classificar segmento
    def classify(days):
        if days <= days_active:
            return 'Ativo'
        elif days_active < days <= days_risk:
            return 'Em risco'
        else:
            return 'Inativo'

    df['recency_segment'] = df['days_since_last_purchase'].apply(classify)
    return df

def segment_customers_by_rfm(df,
                           recency_threshold=None,
                           frequency_threshold=None,
                           monetary_threshold=None):
    """
    RFM com thresholds lidos do config se não definidos na chamada.
    """
    from src.config import load_config
    config = load_config()
    if recency_threshold is None:
        recency_threshold = config.get("rfm_recency_threshold", 30)
    if frequency_threshold is None:
        frequency_threshold = config.get("rfm_frequency_threshold", 5)
    if monetary_threshold is None:
        monetary_threshold = config.get("rfm_monetary_threshold", 1000)
    df = df.copy()
    today = datetime.today().date()
    # Calcula Recency
    df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date']).dt.date
    df['rfm_recency'] = df['last_purchase_date'].apply(lambda d: (today - d).days)
    # Classifica em 0 ou 1: Recente = 1 se dentro do threshold
    df['R'] = df['rfm_recency'].apply(lambda x: 1 if x <= recency_threshold else 0)
    # Frequency
    df['F'] = df['purchase_count'].apply(lambda x: 1 if x >= frequency_threshold else 0)
    # Monetary
    df['M'] = df['total_spend'].apply(lambda x: 1 if x >= monetary_threshold else 0)

    # Gera um score para facilitar a classificação
    df['rfm_score'] = df['R'].astype(str) + df['F'].astype(str) + df['M'].astype(str)

    # Mapear segmentos
    def map_segment(row):
        if row['rfm_score'] == '111':
            return 'Campeão'
        elif row['rfm_score'] in ['110', '101', '011']:
            return 'Potencial'
        else:
            return 'Em risco'
    df['rfm_segment'] = df.apply(map_segment, axis=1)
    return df

def segment_customers_by_engagement(df, high=None, medium=None, low=None):
    """
    Segmenta clientes pelo engajamento, somando aberturas de e-mail e logins nos últimos 30 dias.
    Usa thresholds do config.json se não passar argumento.

    Parâmetros:
    -------------
    df: pandas.DataFrame
    high: int | None
        Ponto de corte para "Alto Engajamento"
    medium: int | None
        Ponto de corte para "Médio Engajamento"
    low: int | None
        Ponto de corte para "Baixo Engajamento"
    
    Retorna: DataFrame com nova coluna 'engagement_segment'.
    """
    from src.config import load_config
    config = load_config()
    if high is None:
        high = config.get("engagement_high", 15)
    if medium is None:
        medium = config.get("engagement_medium", 6)
    if low is None:
        low = config.get("engagement_low", 0)
    
    df = df.copy()
    # Calcula score de engajamento (exemplo: aberturas de email + logins)
    df['engagement_score'] = df['email_opens_30d'] + df['logins_30d']
    def classify_engagement(score):
        if score >= high:
            return 'Alto'
        elif medium <= score < high:
            return 'Médio'
        else:
            return 'Baixo'
    df['engagement_segment'] = df['engagement_score'].apply(classify_engagement)
    return df
