"""
basic_usage.py
==============
Exemplo de como carregar dados, segmentar clientes (recência, RFM, engajamento) e exportar segmentos em CSV.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_customer_data
from src.segmentation import (
    segment_customers_by_recency, segment_customers_by_rfm, segment_customers_by_engagement)
from src.utils import (
    save_segment_to_csv, print_segment_summary, setup_logger)
from src.config import load_config

if __name__ == "__main__":
    # Inicializa logger
    logger = setup_logger()
    logger.info("Iniciando fluxo de segmentação e exportação de clientes...")
    config = load_config()
    print("Thresholds de segmentação carregados do config.json:")
    print(config)
    print(f"\nFonte de dados definida: {config.get('data_source','csv').upper()}\n")

    # Carrega de CSV ou API conforme config
    df = load_customer_data(source=config.get('data_source','csv'))
    if df is not None:
        print(f"Dados carregados ({len(df)} clientes). Leia o código/data_loader.py para ver como adaptar para API real!")
        logger.info("Dados carregados com sucesso. Executando segmentações...")
        # Recência
        df_segmented = segment_customers_by_recency(df)
        logger.info("Segmentação por recência realizada.")
        print("\nClientes com segmento de recência:")
        print(df_segmented[["name", "last_purchase_date", "recency_segment"]].head())
        print_segment_summary(df_segmented, "recency_segment")

        # RFM
        df_rfm = segment_customers_by_rfm(df)
        logger.info("Segmentação RFM realizada.")
        print("\nClientes com segmento RFM:")
        print(df_rfm[["name", "rfm_score", "rfm_segment"]].head())
        print_segment_summary(df_rfm, "rfm_segment")

        # Engajamento
        df_eng = segment_customers_by_engagement(df)
        logger.info("Segmentação por engajamento realizada.")
        print("\nClientes com segmento de engajamento (score= email_opens_30d + logins_30d; limiares do config.json):")
        print(df_eng[["name", "email_opens_30d", "logins_30d", "engagement_score", "engagement_segment"]].head())
        print_segment_summary(df_eng, "engagement_segment")

        # Exporta exemplos
        ativos = df_segmented[df_segmented["recency_segment"] == "Ativo"]
        save_segment_to_csv(ativos, "recency_ativos")
        logger.info(f"Exportou {len(ativos)} clientes Ativos para CSV.")
        campeoes = df_rfm[df_rfm["rfm_segment"] == "Campeão"]
        save_segment_to_csv(campeoes, "rfm_campeoes")
        logger.info(f"Exportou {len(campeoes)} clientes Campeões para CSV.")
        engajados = df_eng[df_eng["engagement_segment"] == "Alto"]
        save_segment_to_csv(engajados, "engajamento_alto")
        logger.info(f"Exportou {len(engajados)} clientes Altamente Engajados para CSV.")

        print("\nPara alterar critérios de segmentação, basta editar o arquivo 'config.json' e rodar novamente!")
        logger.info("Processo completo com sucesso!")
    else:
        logger.error("Falha ao carregar dados do CSV. Segmentar impossível.")
        print("Customer data could not be loaded.")
