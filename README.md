# Customer Segmentation Engine

A Python tool for segmenting customers based on behavior and outputting actionable lists for CRM campaigns.

## Features
- Load customer data from CSV or external API (ready for HubSpot, Salesforce, and similar CRMs)
- Segment customers by recent behavior, RFM, engagement, and more
- Output ready-to-use lists for marketing or support
- Configurable thresholds (edit config.json to customize!)
- Exports segmented customer lists to CSV automatically
- Summary dashboard: see counts/percent by segment
- Detailed logging in logs/segmentation.log
- Easy-to-add unit tests (pytest)

## How to Use
1. Clone this repo: `git clone ...`
2. (Optional) Set up a virtual environment: `python -m venv venv`
3. Activate virtualenv and install dependencies: `pip install -r requirements.txt`
4. Edit `config.json` to change segmentation criteria (ex: days since last purchase, engagement cuts, etc)
5. Run: `python examples/basic_usage.py`
6. Results:
    - Segment summaries printed
    - Segmented CSVs in `data/output/`
    - Logs in `logs/segmentation.log`

## Dashboard/Segment Summaries
The main script prints segment counts and percent, example output:

```
Resumo do segmento 'recency_segment':
- Ativo: 8 clientes (32.0%)
- Em risco: 6 clientes (24.0%)
- Inativo: 11 clientes (44.0%)

Resumo do segmento 'rfm_segment':
- Campeão: 5 clientes (20.0%)
- Potencial: 8 clientes (32.0%)
- Em risco: 12 clientes (48.0%)

Resumo do segmento 'engagement_segment':
- Alto: 7 clientes (...%)
- Médio: ...
- Baixo: ...
```

## Logging
- All major events and exports are logged in `logs/segmentation.log`.
- Example:
```
2024-06-07 19:03:22,106 - INFO - Segmentação por recência realizada.
2024-06-07 19:03:22,108 - INFO - Exportou 8 clientes Ativos para CSV.
```

## Testing (Pytest)
Run all tests:
```bash
pytest tests/
```

## Example Usage
Run the script:
```bash
python examples/basic_usage.py
```
Edit `config.json` to change thresholds for advanced testing!

## API Integration (HubSpot/Salesforce Example)
You can fetch customer data from an external API as well as local CSVs! Out-of-the-box, the system provides a mock for quick learning/testing.

How to use:
- Set "data_source": "api" in config.json
- Provide your API key in "hubspot_api_key" (or use your real CRM token)

Example config.json:
```json
{
  "data_source": "api",
  "hubspot_api_key": "coloque-aqui-o-seu-token-api-se-tiver",
  ...rest of config...
}
```

The loader will fetch (mock) customer data via API. To connect a real HubSpot or Salesforce endpoint, replace the endpoint and headers in `src/data_loader.py` (function `fetch_customer_data_from_api`) and adjust JSON parsing if needed.

---
**Learning Project for Laissa Manzi.**
