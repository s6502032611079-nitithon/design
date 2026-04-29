<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pile Reaction Calculator</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0f1117;
    --surface: #181c27;
    --surface2: #1e2333;
    --border: #2a3045;
    --accent: #4f8ef7;
    --accent2: #7c5cfc;
    --danger: #f45b5b;
    --success: #3ecf8e;
    --text: #e8eaf0;
    --muted: #7a85a3;
    --mono: 'IBM Plex Mono', monospace;
    --sans: 'IBM Plex Sans Thai', sans-serif;
  }

  body {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  .wrapper {
    max-width: 820px;
    margin: 0 auto;
  }

  /* Header */
  header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
  }
  .tag {
    display: inline-block;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 4px;
    padding: 2px 8px;
    margin-bottom: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  h1 {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #e8eaf0 30%, #7a85a3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .subtitle {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.4rem;
    font-weight: 300;
  }

  /* Formula display */
  .formula-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 2rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.8;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 2rem;
  }
  .formula-bar span { color: var(--text); }
  .formula-bar .eq { color: var(--accent); }

  /* Inputs grid */
  .inputs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .field {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    transition: border-color 0.2s;
  }
  .field:focus-within {
    border-color: var(--accent);
  }
  .field label {
    display: block;
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 6px;
    font-weight: 500;
    letter-spacing: 0.03em;
  }
  .field input {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    font-family: var(--mono);
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text);
    -moz-appearance: textfield;
  }
  .field input::-webkit-outer-spin-button,
  .field input::-webkit-inner-spin-button { -webkit-appearance: none; }
  .field .unit {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 4px;
  }

  /* Pile position editor */
  .pile-editor-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }
  .section-label {
    font-size: 0.75rem;
    color: var(--muted);
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }
  .pile-row {
    display: grid;
    grid-template-columns: 60px 1fr 1fr auto;
    gap: 8px;
    align-items: center;
    margin-bottom: 6px;
  }
  .pile-row .lbl {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--muted);
  }
  .pile-row input {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 5px 8px;
    font-family: var(--mono);
    font-size: 0.85rem;
    color: var(--text);
    width: 100%;
    outline: none;
    -moz-appearance: textfield;
    transition: border-color 0.2s;
  }
  .pile-row input:focus { border-color: var(--accent); }
  .pile-row input::-webkit-outer-spin-button,
  .pile-row input::-webkit-inner-spin-button { -webkit-appearance: none; }
  .btn-rm {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--danger);
    cursor: pointer;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    transition: background 0.15s;
  }
  .btn-rm:hover { background: rgba(244,91,91,0.12); }
  .btn-add {
    margin-top: 6px;
    background: transparent;
    border: 1px dashed var(--border);
    border-radius: 6px;
    color: var(--muted);
    cursor: pointer;
    font-size: 0.8rem;
    padding: 5px 14px;
    transition: all 0.15s;
  }
  .btn-add:hover { border-color: var(--accent); color: var(--accent); }

  /* CTA */
  .btn-calc {
    width: 100%;
    padding: 0.85rem;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border: none;
    border-radius: 10px;
    color: #fff;
    font-family: var(--sans);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: opacity 0.2s, transform 0.1s;
    margin-bottom: 2rem;
  }
  .btn-calc:hover { opacity: 0.9; }
  .btn-calc:active { transform: scale(0.99); }

  /* Summary cards */
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-bottom: 1.5rem;
  }
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
  }
  .card .c-label { font-size: 0.72rem; color: var(--muted); margin-bottom: 6px; }
  .card .c-val {
    font-family: var(--mono);
    font-size: 1.3rem;
    font-weight: 500;
    color: var(--accent);
  }
  .card .c-unit { font-size: 0.7rem; color: var(--muted); margin-top: 3px; }

  /* Results */
  .results {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }
  table { width: 100%; border-collapse: collapse; }
  thead tr { background: var(--surface2); }
  th {
    padding: 10px 16px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--muted);
    text-align: right;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
  }
  th:first-child { text-align: left; }
  td {
    padding: 10px 16px;
    font-family: var(--mono);
    font-size: 0.9rem;
    text-align: right;
    border-bottom: 1px solid var(--border);
  }
  td:first-child { text-align: left; color: var(--muted); }
  tr:last-child td { border-bottom: none; }
  tr.positive .reaction-val { color: var(--success); }
  tr.negative .reaction-val { color: var(--danger); }
  tr.max-pile .reaction-val { font-weight: 600; }
  .bar-cell { padding: 8px 16px; }
  .bar-wrap { background: var(--surface2); border-radius: 4px; height: 6px; overflow: hidden; }
  .bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
  }

  /* SVG diagram */
  .diagram-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
  }
  #pile-svg { display: block; margin: 0 auto; }

  /* Hidden initially */
  #output { display: none; }
</style>
</head>
<body>
<div class="wrapper">

  <header>
    <div class="tag">Structural Engineering</div>
    <h1>Pile Reaction Calculator</h1>
    <p class="subtitle">คำนวณแรงปฏิกิริยาในกลุ่มเสาเข็มภายใต้แรงกระทำแบบนอกศูนย์</p>
  </header>

  <div class="formula-bar">
    <div>R<sub>i</sub> <span class="eq">=</span> <span>P/n</span> <span class="eq">+</span> <span>Mₓ·yᵢ / Σyᵢ²</span> <span class="eq">+</span> <span>My·xᵢ / Σxᵢ²</span></div>
    <div>Mₓ <span class="eq">=</span> <span>P·e_y</span></div>
    <div>My <span class="eq">=</span> <span>P·e_x</span></div>
  </div>

  <div class="inputs-grid">
    <div class="field">
      <label>แรงกระทำรวม P</label>
      <input type="number" id="P" value="150">
      <div class="unit">ตัน (ton)</div>
    </div>
    <div class="field">
      <label>Eccentricity eₓ</label>
      <input type="number" id="ex" value="0">
      <div class="unit">cm (แนว X)</div>
    </div>
    <div class="field">
      <label>Eccentricity e_y</label>
      <input type="number" id="ey" value="0">
      <div class="unit">cm (แนว Y)</div>
    </div>
  </div>

  <div class="pile-editor-section">
    <div class="section-label">ตำแหน่งเสาเข็ม (cm)</div>
    <div class="pile-row" style="color:var(--muted);font-size:0.72rem;margin-bottom:4px;">
      <div></div><div>X (cm)</div><div>Y (cm)</div><div></div>
    </div>
    <div id="pile-list"></div>
    <button class="btn-add" onclick="addPile()">+ เพิ่มเสาเข็ม</button>
  </div>

  <button class="btn-calc" onclick="calculate()">คำนวณแรงปฏิกิริยา</button>

  <div id="output">
    <div class="summary-grid">
      <div class="card"><div class="c-label">n (จำนวนเสาเข็ม)</div><div class="c-val" id="s-n">—</div></div>
      <div class="card"><div class="c-label">Mₓ = P·e_y</div><div class="c-val" id="s-mx">—</div><div class="c-unit">ตัน·cm</div></div>
      <div class="card"><div class="c-label">My = P·eₓ</div><div class="c-val" id="s-my">—</div><div class="c-unit">ตัน·cm</div></div>
      <div class="card"><div class="c-label">Σxᵢ²</div><div class="c-val" id="s-sx2">—</div><div class="c-unit">cm²</div></div>
      <div class="card"><div class="c-label">Σyᵢ²</div><div class="c-val" id="s-sy2">—</div><div class="c-unit">cm²</div></div>
      <div class="card"><div class="c-label">R สูงสุด</div><div class="c-val" id="s-rmax">—</div><div class="c-unit">ตัน</div></div>
    </div>

    <div class="results">
      <table>
        <thead>
          <tr>
            <th>Pile</th>
            <th>X (cm)</th>
            <th>Y (cm)</th>
            <th>P/n</th>
            <th>Mₓ·y/Σy²</th>
            <th>My·x/Σx²</th>
            <th>Reaction (ตัน)</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
      <table style="margin-top:0;">
        <tbody id="bar-body"></tbody>
      </table>
    </div>

    <div class="diagram-section">
      <div class="section-label" style="margin-bottom:0.75rem;">แผนผังตำแหน่งและแรงปฏิกิริยา</div>
      <svg id="pile-svg" viewBox="-160 -160 320 320" width="100%" style="max-height:280px;"></svg>
    </div>
  </div>

</div>

<script>
let piles = [
  {x:-60, y:95},
  {x:60,  y:95},
  {x:-60, y:-95},
  {x:60,  y:-95}
];

function renderPileList() {
  const list = document.getElementById('pile-list');
  list.innerHTML = piles.map((p, i) => `
    <div class="pile-row">
      <div class="lbl">Pile ${i+1}</div>
      <input type="number" value="${p.x}" oninput="piles[${i}].x=parseFloat(this.value)||0" placeholder="X">
      <input type="number" value="${p.y}" oninput="piles[${i}].y=parseFloat(this.value)||0" placeholder="Y">
      <button class="btn-rm" onclick="removePile(${i})" title="ลบ">×</button>
    </div>
  `).join('');
}

function addPile() {
  piles.push({x:0, y:0});
  renderPileList();
}

function removePile(i) {
  if (piles.length <= 2) { alert('ต้องมีเสาเข็มอย่างน้อย 2 ต้น'); return; }
  piles.splice(i, 1);
  renderPileList();
}

function calculate() {
  const P  = parseFloat(document.getElementById('P').value)  || 0;
  const ex = parseFloat(document.getElementById('ex').value) || 0;
  const ey = parseFloat(document.getElementById('ey').value) || 0;
  const n  = piles.length;

  // Read current pile positions from inputs
  document.querySelectorAll('#pile-list .pile-row').forEach((row, i) => {
    const inputs = row.querySelectorAll('input');
    piles[i].x = parseFloat(inputs[0].value) || 0;
    piles[i].y = parseFloat(inputs[1].value) || 0;
  });

  const Mx   = P * ey;
  const My   = P * ex;
  const sx2  = piles.reduce((s,p) => s + p.x*p.x, 0);
  const sy2  = piles.reduce((s,p) => s + p.y*p.y, 0);

  const results = piles.map((p, i) => {
    const base  = P / n;
    const termY = sy2 !== 0 ? Mx * p.y / sy2 : 0;
    const termX = sx2 !== 0 ? My * p.x / sx2 : 0;
    return { pile: i+1, x: p.x, y: p.y, base, termY, termX, R: base + termY + termX };
  });

  const Rmax  = Math.max(...results.map(r => Math.abs(r.R)));
  const Rmin  = Math.min(...results.map(r => r.R));

  // Summary
  document.getElementById('s-n').textContent   = n;
  document.getElementById('s-mx').textContent  = Mx.toFixed(2);
  document.getElementById('s-my').textContent  = My.toFixed(2);
  document.getElementById('s-sx2').textContent = sx2.toFixed(0);
  document.getElementById('s-sy2').textContent = sy2.toFixed(0);
  document.getElementById('s-rmax').textContent= Rmax.toFixed(2);

  // Table
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = results.map(r => {
    const isMax = Math.abs(r.R) === Rmax;
    const cls   = r.R < 0 ? 'negative' : 'positive';
    return `<tr class="${cls}${isMax ? ' max-pile' : ''}">
      <td>Pile ${r.pile}${isMax ? ' ★' : ''}</td>
      <td>${r.x}</td>
      <td>${r.y}</td>
      <td>${r.base.toFixed(2)}</td>
      <td>${r.termY.toFixed(2)}</td>
      <td>${r.termX.toFixed(2)}</td>
      <td class="reaction-val">${r.R.toFixed(2)}</td>
    </tr>`;
  }).join('');

  // Bar chart rows
  const barBody = document.getElementById('bar-body');
  barBody.innerHTML = results.map(r => {
    const pct   = Rmax > 0 ? (Math.abs(r.R)/Rmax*100).toFixed(1) : 0;
    const color = r.R < 0 ? '#f45b5b' : '#3ecf8e';
    return `<tr>
      <td style="color:var(--muted);width:70px;">Pile ${r.pile}</td>
      <td class="bar-cell">
        <div class="bar-wrap"><div class="bar-fill" style="width:${pct}%;background:${color};"></div></div>
      </td>
      <td style="font-family:var(--mono);font-size:0.8rem;width:80px;color:${color};">${r.R.toFixed(2)} t</td>
    </tr>`;
  }).join('');

  // SVG diagram
  drawDiagram(results, Rmax);

  document.getElementById('output').style.display = 'block';
  document.getElementById('output').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function drawDiagram(results, Rmax) {
  const svg = document.getElementById('pile-svg');

  // Auto-scale
  const xs = results.map(r => r.x), ys = results.map(r => r.y);
  const span = Math.max(
    Math.max(...xs) - Math.min(...xs),
    Math.max(...ys) - Math.min(...ys),
    1
  );
  const sc = Math.min(120 / (span / 2 + 30), 1.4);

  let h = '';

  // Grid
  h += `<line x1="-150" y1="0" x2="150" y2="0" stroke="#2a3045" stroke-width="0.8"/>`;
  h += `<line x1="0" y1="-150" x2="0" y2="150" stroke="#2a3045" stroke-width="0.8"/>`;
  h += `<text x="148" y="12" font-size="10" fill="#7a85a3" text-anchor="end">X</text>`;
  h += `<text x="6" y="-138" font-size="10" fill="#7a85a3">Y</text>`;

  // Cap outline (convex hull approximation: just lines between piles)
  const pts = results.map(r => [r.x * sc, -r.y * sc]);
  // Connect in order
  if (pts.length >= 2) {
    for (let i = 0; i < pts.length; i++) {
      const a = pts[i], b = pts[(i+1)%pts.length];
      h += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#2a3045" stroke-width="1" stroke-dasharray="4,3"/>`;
    }
  }

  results.forEach(r => {
    const cx = r.x * sc;
    const cy = -r.y * sc;
    const isMax = Math.abs(r.R) === Rmax;
    const neg = r.R < 0;
    const fill   = neg ? '#f45b5b' : (isMax ? '#4f8ef7' : '#3ecf8e');
    const radius = 13 + (Rmax > 0 ? Math.abs(r.R) / Rmax * 6 : 0);

    // Arrow showing reaction magnitude
    const arrowLen = Rmax > 0 ? 30 * Math.abs(r.R) / Rmax : 0;
    const dir = neg ? 1 : -1;
    h += `<line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy + dir*arrowLen}"
            stroke="${fill}" stroke-width="2" stroke-dasharray="${neg?'4,2':'none'}"
            marker-end="url(#arr-${neg?'down':'up'})"/>`;

    h += `<circle cx="${cx}" cy="${cy}" r="${radius}" fill="${fill}" opacity="0.9"/>`;
    h += `<text x="${cx}" y="${cy + 4}" font-size="10" text-anchor="middle" fill="#0f1117" font-weight="600">${r.pile}</text>`;
    h += `<text x="${cx + radius + 4}" y="${cy - 4}" font-size="9" fill="${fill}" font-weight="500">${r.R.toFixed(1)}t</text>`;
  });

  const defs = `<defs>
    <marker id="arr-up" markerWidth="6" markerHeight="6" refX="3" refY="6" orient="auto">
      <path d="M0,6 L3,0 L6,6" fill="none" stroke="#3ecf8e" stroke-width="1"/>
    </marker>
    <marker id="arr-down" markerWidth="6" markerHeight="6" refX="3" refY="0" orient="auto">
      <path d="M0,0 L3,6 L6,0" fill="none" stroke="#f45b5b" stroke-width="1"/>
    </marker>
  </defs>`;

  svg.innerHTML = defs + h;
}

// Init
renderPileList();
</script>
</body>
</html>
