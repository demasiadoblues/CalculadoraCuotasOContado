from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd
import openpyxl

app = FastAPI(title="Simulador Financiero Mejorado")

def load_rates():
    df_wallets = pd.read_csv("data/wallets.csv")
    df_fixed = pd.read_csv("data/fixed.csv")
    top_wallets = df_wallets.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    top_fixed = df_fixed.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    return top_wallets, top_fixed

@app.get