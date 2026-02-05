from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="Simulador Financiero Final")

# Permitir llamadas desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés restringir a ["http://midominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_rates():
    df_wallets = pd.read_csv("../data/wallets.csv")
    df_fixed = pd.read_csv("../data/fixed.csv")
    top_wallets = df_wallets.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    top_fixed = df_fixed.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    return top_wallets, top_fixed

@app.get("/")
def home():
    return {"message": "Backend funcionando!"}

@app.get("/top-wallets")
def top_wallets():
    wallets, _ = load_rates()
    return wallets

@app.get("/top-fixed")
def top_fixed():
    _, fixed = load_rates()
    return fixed

@app.get("/compare")
def compare(monto: float, cuotas: int, tasa_cuotas: float, tasa_inversion: float):
    valor_cuotas = monto * (1 + tasa_cuotas/100)
    valor_inversion = monto * (1 + tasa_inversion/100)

    scenarioA = {"type": "Pago en cuotas", "option": f"{cuotas} cuotas", "tasa": tasa_cuotas, "valor_final": round(valor_cuotas, 2)}
    scenarioB = {"type": "Inversión", "option": "Billetera/Plazo fijo", "tasa": tasa_inversion, "valor_final": round(valor_inversion, 2)}

    conclusion = "Conviene invertir" if valor_inversion > valor_cuotas else "Conviene pagar en cuotas"

    return {"scenarioA": scenarioA, "scenarioB": scenarioB, "conclusion": conclusion}

@app.get("/export")
def export(monto: float = 100000, cuotas: int = 12, tasa_cuotas: float = 80.0, tasa_inversion: float = 85.0):
    valor_cuotas = monto * (1 + tasa_cuotas/100)
    valor_inversion = monto * (1 + tasa_inversion/100)

    data = {
        "Escenario": ["Pago en cuotas", "Inversión"],
        "Tasa": [tasa_cuotas, tasa_inversion],
        "Valor final": [valor_cuotas, valor_inversion]
    }
    df = pd.DataFrame(data)
    filename = "simulacion.xlsx"
    df.to_excel(filename, index=False)
    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)
