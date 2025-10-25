"""Utilities for Customer Segmentation Engine."""
import os
from datetime import datetime
import logging

def save_segment_to_csv(df, segment_name, output_dir="data/output"):
    """
    Salva um DataFrame segmentado em um arquivo CSV dentro de data/output.
    O nome do arquivo inclui o segmento e a data/hora para evitar sobrescrever arquivos antigos.

    Parâmetros:
    ------------
    df : pandas.DataFrame
        DataFrame para exportar
    segment_name : str
        Nome do segmento (ex: "ativos", "rfm_campeoes")
    output_dir : str
        Caminho para a pasta onde salvar os arquivos (padrão: data/output)
    """
    # Cria a pasta de output caso ainda não exista
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{segment_name}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Salva o DataFrame em CSV
    df.to_csv(filepath, index=False)
    print(f"Segmento '{segment_name}' exportado para: {filepath}")

def print_segment_summary(df, column, print_result=True):
    """
    Imprime um resumo com contagem, percentual e estatísticas para cada valor único de um segmento.
    
    Parâmetros:
    ------------
    df : pandas.DataFrame
    column : str
        Nome da coluna dos segmentos
    print_result : bool
        Decide se imprime na tela (True padrão)
    
    Retorno:
    ---------
    str : resumo formatado para uso em README ou outputs
    """
    total = len(df)
    summary = df[column].value_counts(dropna=False).sort_index()
    res = f"Resumo do segmento '{column}':\n"
    for cat, count in summary.items():
        perc = (count / total) * 100
        res += f"- {cat}: {count} clientes ({perc:.1f}%)\n"
    if print_result:
        print(res)
    return res

def setup_logger(log_file="logs/segmentation.log"):
    """
    Cria (e retorna) um logger configurado para console e arquivo.
    Logará ações-chave do projeto.
    """
    import os
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("segmentation_logger")
    logger.setLevel(logging.INFO)
    # Evita logging duplicado ao rodar várias vezes
    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
