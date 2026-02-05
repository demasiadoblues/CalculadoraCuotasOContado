document.getElementById("simulador").addEventListener("submit", async function(e) {
    e.preventDefault();

    const monto = document.getElementById("monto").value;
    const cuotas = document.getElementById("cuotas").value;
    const tasaCuotas = document.getElementById("tasaCuotas").value;
    const tasaInversion = document.getElementById("tasaInversion").value;

    const res = await fetch(`http://localhost:8000/compare?monto=${monto}&cuotas=${cuotas}&tasa_cuotas=${tasaCuotas}&tasa_inversion=${tasaInversion}`);
    const data = await res.json();

    document.getElementById("resultado").innerHTML = `
        <h3>Resultados</h3>
        <p><b>${data.scenarioA.type}</b>: ${data.scenarioA.option}, Tasa: ${data.scenarioA.tasa}%, Valor final: ${data.scenarioA.valor_final}</p>
        <p><b>${data.scenarioB.type}</b>: ${data.scenarioB.option}, Tasa: ${data.scenarioB.tasa}%, Valor final: ${data.scenarioB.valor_final}</p>
        <p><b>Conclusión:</b> ${data.conclusion}</p>
    `;
});

document.getElementById("descargar").addEventListener("click", function() {
    window.location.href = "http://localhost:8000/export";
});
