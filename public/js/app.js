async function cargarOpciones() {
  const walletsRes = await fetch("http://localhost:8000/top-wallets");
  const wallets = await walletsRes.json();

  const fixedRes = await fetch("http://localhost:8000/top-fixed");
  const fixed = await fixedRes.json();

  let html = "<h3>Billeteras Virtuales</h3><ul>";
  wallets.forEach(w => {
    html += `<li>${w.nombre}: ${w.tasa}%</li>`;
  });
  html += "</ul><h3>Plazos Fijos</h3><ul>";
  fixed.forEach(f => {
    html += `<li>${f.banco}: ${f.tasa}%</li>`;
  });
  html += "</ul>";

  document.getElementById("mejoresOpciones").innerHTML = html;
}

window.onload = cargarOpciones;

async function calcular(columna) {
  let monto, cuotas, tasa;
  if (columna === 'A') {
    monto = document.getElementById('montoA').value;
    cuotas = document.getElementById('cuotasA').value;
    tasa = document.getElementById('tasaA').value;
  } else {
    monto = document.getElementById('montoB').value;
    cuotas = 1;
    tasa = document.getElementById('tasaB').value;
  }

  const response = await fetch(`http://localhost:8000/compare?monto=${monto}&cuotas=${cuotas}&tasa_cuotas=${tasa}&tasa_inversion=${tasa}`);
  const data = await response.json();

  if (columna === 'A') {
    document.getElementById('resultadoA').innerHTML = `
      <strong>${data.scenarioA.type}</strong><br>
      Opción: ${data.scenarioA.option}<br>
      Tasa: ${data.scenarioA.tasa}%<br>
      Valor final: $${data.scenarioA.valor_final.toFixed(2)}
    `;
  } else {
    document.getElementById('resultadoB').innerHTML = `
      <strong>${data.scenarioB.type}</strong><br>
      Opción: ${data.scenarioB.option}<br>
      Tasa: ${data.scenarioB.tasa}%<br>
      Valor final: $${data.scenarioB.valor_final.toFixed(2)}<br>
      <em>${data.conclusion}</em>
    `;
  }
}

async function exportarExcel() {
  const response = await fetch("http://localhost:8000/export");
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "simulacion.xlsx";
  document.body.appendChild(a);
  a.click();
  a.remove();
}
