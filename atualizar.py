"""Busca a previsão do Open-Meteo para o Rio e grava data/dados.json."""
import json, urllib.request, datetime, os

URL = ("https://api.open-meteo.com/v1/forecast?latitude=-22.9068&longitude=-43.1729"
       "&daily=temperature_2m_max,apparent_temperature_max,precipitation_sum,"
       "precipitation_probability_max,wind_gusts_10m_max"
       "&timezone=America%2FSao_Paulo&forecast_days=6")

with urllib.request.urlopen(URL, timeout=30) as r:
    d = json.load(r)["daily"]

dias = [{
    "data": d["time"][i],
    "temp_max": d["temperature_2m_max"][i],
    "sensacao_max": d["apparent_temperature_max"][i],
    "chuva_mm": d["precipitation_sum"][i],
    "chuva_prob": d["precipitation_probability_max"][i],
    "rajada_kmh": d["wind_gusts_10m_max"][i],
} for i in range(len(d["time"]))]

agora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
saida = {"atualizado_em": agora.strftime("%Y-%m-%d %H:%M"), "fonte": "Open-Meteo", "dias": dias}

os.makedirs("data", exist_ok=True)
with open("data/dados.json", "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=1)

# histórico: guarda a previsão "de hoje" de cada execução
caminho = "data/historico.json"
hist = json.load(open(caminho, encoding="utf-8")) if os.path.exists(caminho) else []
hist = [h for h in hist if h["data"] != dias[0]["data"]] + [dias[0]]
json.dump(hist[-120:], open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", saida["atualizado_em"])
