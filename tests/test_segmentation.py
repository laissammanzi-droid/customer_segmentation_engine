import pytest
import pandas as pd
from src.segmentation import segment_customers_by_recency, segment_customers_by_engagement

def test_segment_customers_by_recency():
    from datetime import datetime
    hoje = datetime.today().strftime('%Y-%m-%d')
    data = {
        'customer_id': ['C01','C02'],
        'name': ['User1','User2'],
        'last_purchase_date': [hoje,'2000-01-01'],
        'purchase_count': [1,1],
        'total_spend': [10,10],
        'email_opens_30d': [1,1],
        'logins_30d': [1,1],
        'support_tickets':[0,0],
        'nps_score':[8,7],
        'plan_type': ['Basic','Free'],
        'signup_date': ['2021-01-01','2023-01-01']
    }
    df = pd.DataFrame(data)
    res = segment_customers_by_recency(df, days_active=1, days_risk=365*10)  # days_active=1 (só quem comprou hoje é 'Ativo')
    assert res.loc[0, 'recency_segment'] == 'Ativo'
    assert res.loc[1, 'recency_segment'] in ['Inativo', 'Em risco']
    
def test_segment_customers_by_engagement():
    data = {
        'customer_id': ['C01','C02'],
        'name': ['User1','User2'],
        'last_purchase_date': ['2024-06-01','2024-01-01'],
        'purchase_count': [1,1],
        'total_spend': [10,10],
        'email_opens_30d': [10,2],
        'logins_30d': [6,1],
        'support_tickets':[0,0],
        'nps_score':[8,7],
        'plan_type': ['Basic','Free'],
        'signup_date': ['2021-01-01','2023-01-01']
    }
    df = pd.DataFrame(data)
    res = segment_customers_by_engagement(df, high=15, medium=6)
    assert res.loc[0,'engagement_segment'] in ['Médio','Alto']
    assert res.loc[1,'engagement_segment'] == 'Baixo'
