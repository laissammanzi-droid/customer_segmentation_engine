"""Carregador de configuração do projeto - thresholds em JSON."""
import json
import os

def load_config(config_path="config.json"):
    """
    Lê os thresholds de segmentação do arquivo JSON (na raiz do projeto).
    Retorna um dicionário com os parâmetros de configuração.
    """
    # Descobre caminho absoluto do config
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, config_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar configuração: {e}")
        return {}
