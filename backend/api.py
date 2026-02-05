from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI(title="Simulador Financiero Mejorado")

def load_rates():
    df_wallets = pd.read_csv("data/wallets.csv")
    df_fixed = pd.read_csv("data/fixed.csv")
    top_wallets = df_wallets.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    top_fixed = df_fixed.sort_values("tasa", ascending=False).head(3).to_dict(orient="records")
    return top_wallets, top_fixed

@app.get("/")   # ✅ Ruta principal
def home():
    return {"message": "Backend funcionando!"}

@app.get("/top-wallets")   # ✅ Devuelve las 3 mejores billeteras
def top_wallets():
    wallets, _ = load_rates()
    return wallets

@app.get("/top-fixed")   # ✅ Devuelve los 3 mejores plazos fijos
def top_fixed():
    _, fixed = load_rates()
    return fixed

@app.get("/compare")   # ✅ Comparación entre pago e inversión
def compare(monto: float = 100000, cuotas: int = 12, tasa_cuotas: float = 80.0, tasa_inversion: float = 85.0):
    valor_cuotas = monto * (1 + tasa_cuotas/100)
    valor_inversion = monto * (1 + tasa_inversion/100)

    scenarioA = {"type": "Pago en cuotas", "option": f"{cuotas} cuotas", "tasa": tasa_cuotas, "valor_final": valor_cuotas}
    scenarioB = {"type": "Inversión", "option": "Billetera/Plazo fijo", "tasa": tasa_inversion, "valor_final": valor_inversion}

    conclusion = "Conviene invertir" if valor_inversion > valor_cuotas else "Conviene pagar en cuotas"

    return {"scenarioA": scenarioA, "scenarioB": scenarioB, "conclusion": conclusion}

@app.get("/export")   # ✅ Exporta resultados a Excel
def export():
    data = {
        "Escenario": ["Pago en cuotas", "Inversión"],
        "Tasa": [80, 85],
        "Valor final": [100000 * 1.8, 100000 * 1.85]
    }
    df = pd.DataFrame(data)
    filename = "simulacion.xlsx"
    df.to_excel(filename, index=False)
    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)
