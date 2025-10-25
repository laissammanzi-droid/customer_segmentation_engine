"""
data_loader.py
===============
Loads customer data from a CSV file or (mock) API into a Pandas DataFrame, with error handling and validation.
"""
import pandas as pd
import requests
from src.config import load_config

REQUIRED_COLUMNS = [
    'customer_id','name','email','signup_date','last_purchase_date','purchase_count',
    'total_spend','email_opens_30d','logins_30d','support_tickets','nps_score','plan_type'
]

def fetch_customer_data_from_api(api_key=None):
    """
    Busca dados de clientes simulados de uma API externa (mock HubSpot/Salesforce).
    Na prática, substitua o endpoint pelo real, ajuste headers/auth conforme necessário.
    Retorna DataFrame ou None se erro.
    """
    # Exemplo de endpoint (mude para real se for usar de verdade)
    api_url = "https://api.hubapi.com/crm/v3/objects/contacts/demo-mock"  # Simulado
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    try:
        # Mock: gerando dados localmente, simula resposta de API REST
        # Em produção, use: response = requests.get(api_url, headers=headers, timeout=10)
        # E verifique response.status_code == 200
        data = [
            {
                'customer_id':'A1', 'name':'API User','email':'apiuser@test.com','signup_date':'2023-05-01',
                'last_purchase_date':'2024-06-01','purchase_count':5, 'total_spend':2000,
                'email_opens_30d':4, 'logins_30d':8, 'support_tickets':0,'nps_score':9,'plan_type':'Premium'
            },
            {
                'customer_id':'A2', 'name':'API Maria','email':'apimaria@test.com','signup_date':'2022-07-11',
                'last_purchase_date':'2023-10-10','purchase_count':1, 'total_spend':120,
                'email_opens_30d':1, 'logins_30d':1, 'support_tickets':1,'nps_score':7,'plan_type':'Basic'
            }
        ]
        df = pd.DataFrame(data)
        # Exemplo real seria:
        # if response.status_code == 200:
        #     df = pd.DataFrame(response.json()['results'])
        # else:
        #     print(f"Erro API: {response.status_code}")
        return df
    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None

def load_customer_data(csv_path="data/sample_customers.csv", source=None):
    """
    Carrega DataFrame de clientes via CSV ou API, conforme parâmetro 'source'
    Se source=None, lê de config.json (data_source).
    """
    config = load_config()
    if source is None:
        source = config.get('data_source', 'csv')
    if source == 'api':
        print("Carregando clientes via API externa...")
        api_key = config.get('hubspot_api_key','')
        df = fetch_customer_data_from_api(api_key=api_key)
    else:
        print(f"Carregando dados do CSV: {csv_path}")
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                print(f"Error: The file at '{csv_path}' is empty.")
                return None
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                print(f"Error: Missing required columns: {missing_columns}")
                return None
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            print(f"Error: File not found at '{csv_path}'.")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: '{csv_path}' contains no data.")
            return None
        except Exception as e:
            print(f"Unexpected error loading data: {str(e)}")
            return None
    return df
