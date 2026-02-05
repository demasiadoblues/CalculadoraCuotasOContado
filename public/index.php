<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Simulador Financiero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Simulador Financiero</h1>

    <form id="simulador">
        <label>Monto: <input type="number" id="monto" value="100000"></label><br>
        <label>Cuotas: <input type="number" id="cuotas" value="12"></label><br>
        <label>Tasa cuotas (%): <input type="number" id="tasaCuotas" value="80"></label><br>
        <label>Tasa inversión (%): <input type="number" id="tasaInversion" value="85"></label><br>
        <button type="submit">Calcular</button>
    </form>

    <div id="resultado"></div>

    <button id="descargar">Descargar Excel</button>

    <script src="app.js"></script>
</body>
</html>
