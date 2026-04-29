<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>คำนวณแรงปฏิกิริยาเสาเข็มเยื้องศูนย์</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Sarabun', sans-serif;
    background: #f5f4f0;
    color: #2C2C2A;
    min-height: 100vh;
    padding: 1.5rem;
  }
  h1 {
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 0.25rem;
    color: #2C2C2A;
  }
  .subtitle {
    font-size: 13px;
    color: #5F5E5A;
    margin-bottom: 1.5rem;
  }
  .section {
    background: #fff;
    border: 0.5px solid rgba(0,0,0,0.15);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
  }
  .sec-title {
    font-size: 13px;
    font-weight: 500;
    color: #5F5E5A;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin-bottom: 1rem;
  }
  .row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
  }
  .row label {
    font-size: 13px;
    color: #5F5E5A;
    min-width: 200px;
  }
  .row input[type=number] {
    width: 100px;
    padding: 6px 8px;
    font-size: 13px;
    border: 0.5px solid rgba(0,0,0,0.3);
    border-radius: 8px;
    background: #F1EFE8;
    color: #2C2C2A;
  }
  .row input[type=range] {
    flex: 1;
    max-width: 200px;
  }
  .row span {
    font-size: 14px;
    font-weight: 500;
    min-width: 36px;
  }
  .pile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px;
    margin-bottom: 1rem;
  }
  .pile-card {
    background: #F1EFE8;
    border: 0.5px solid rgba(0,0,0,0.15);
    border-radius: 8px;
    padding: .75rem;
  }
  .pile-head {
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 8px;
    color: #2C2C2A;
  }
  .field-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
  }
  .field-row span {
    font-size: 12px;
    color: #5F5E5A;
    width: 28px;
  }
  .field-row input {
    width: 68px;
    font-size: 12px;
    padding: 3px 6px;
    border: 0.5px solid rgba(0,0,0,0.25);
    border-radius: 8px;
    background: #fff;
    color: #2C2C2A;
  }
  .field-label {
    font-size: 12px;
    color: #5F5E5A;
  }
  .canvas-wrap {
    background: #F1EFE8;
    border: 0.5px solid rgba(0,0,0,0.15);
    border-radius: 12px;
    padding: .75rem;
    margin-bottom: 1rem;
    overflow: hidden;
  }
  canvas { display: block; margin: auto; }
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
    margin-bottom: 1rem;
  }
  .metric {
    background: #F1EFE8;
    border-radius: 8px;
    padding: .75rem;
  }
  .metric .lbl { font-size: 12px; color: #5F5E5A; margin-bottom: 4px; }
  .metric .val { font-size: 18px; font-weight: 500; color: #2C2C2A; }
  .metric .sub { font-size: 11px; color: #888780; }
  .pile-result-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 0.5px solid rgba(0,0,0,0.15);
    flex-wrap: wrap;
    gap: 6px;
  }
  .badge {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 8px;
    font-weight: 500;
  }
  .ok   { background: #EAF3DE; color: #27500A; }
  .warn { background: #FAEEDA; color: #633806; }
  .over { background: #FCEBEB; color: #501313; }
  .calc-btn {
    width: 100%;
    padding: 11px;
    font-size: 14px;
    font-weight: 500;
    background: #fff;
    border: 0.5px solid rgba(0,0,0,0.3);
    border-radius: 8px;
    cursor: pointer;
    color: #2C2C2A;
    transition: background .15s;
    margin-bottom: 1rem;
  }
  .calc-btn:hover { background: #F1EFE8; }
  .info-note {
    font-size: 12px;
    color: #185FA5;
    background: #E6F1FB;
    border: 0.5px solid #B5D4F4;
    border-radius: 8px;
    padding: .6rem .9rem;
    margin-bottom: 1rem;
  }
</style>
</head>
<body>

<h1>คำนวณแรงปฏิกิริยาเสาเข็มเมื่อเกิดการเยื้องศูนย์</h1>
<p class="subtitle">อ้างอิงสูตร: Bakhoum (1992) — มยผ.1106-64</p>

<div class="section">
  <div class="sec-title">พารามิเตอร์หลัก</div>
  <div class="row">
    <label>น้ำหนักบรรทุก Q (ตัน)</label>
    <input type="number" id="Q" value="100" min="1" max="9999" step="1">
  </div>
  <div class="row">
    <label>น้ำหนักปลอดภัยเสาเข็ม (ตัน/ต้น)</label>
    <input type="number" id="Qsafe" value="40" min="1" max="999" step="1">
  </div>
  <div class="row">
    <label>จำนวนเสาเข็ม (n)</label>
    <input type="range" id="nPiles" min="2" max="6" value="4" step="1">
    <span id="nPilesOut">4 ต้น</span>
  </div>
  <div class="row">
    <label>ระยะห่างเสาเข็ม S (cm)</label>
    <input type="number" id="S" value="120" min="30" max="500" step="5">
  </div>
</div>

<div class="section">
  <div class="sec-title">ระยะเยื้องศูนย์แต่ละต้น (cm)</div>
  <div class="info-note">
    วัดจากตำแหน่งออกแบบ: +eₓ = เยื้องขวา, −eₓ = เยื้องซ้าย, +e_y = เยื้องขึ้น, −e_y = เยื้องลง
  </div>
  <div class="pile-grid" id="pileInputs"></div>
</div>

<button class="calc-btn" onclick="calculate()">คำนวณแรงปฏิกิริยา</button>

<div id="diagram-wrap" class="canvas-wrap" style="display:none">
  <canvas id="diagramCanvas" width="660" height="340"></canvas>
</div>

<div id="resultsSection" style="display:none">
  <div class="section">
    <div class="sec-title">จุด Centroid ใหม่ และโมเมนต์ที่เกิดขึ้น</div>
    <div class="results-grid" id="centroidCards"></div>
  </div>
  <div class="section">
    <div class="sec-title">แรงปฏิกิริยาแต่ละต้น (เทียบกับน้ำหนักปลอดภัย)</div>
    <div id="pileResults"></div>
  </div>
</div>

<script>
const nSlider = document.getElementById('nPiles');
const nOut    = document.getElementById('nPilesOut');

nSlider.addEventListener('input', () => {
  nOut.textContent = nSlider.value + ' ต้น';
  buildPileInputs();
});

function buildPileInputs() {
  const n = parseInt(nSlider.value);
  const grid = document.getElementById('pileInputs');
  grid.innerHTML = '';
  for (let i = 0; i < n; i++) {
    const div = document.createElement('div');
    div.className = 'pile-card';
    div.innerHTML = `
      <div class="pile-head">เสาเข็มที่ ${i + 1}</div>
      <div class="field-row">
        <span>eₓ</span>
        <input type="number" id="ex${i}" value="0" step="0.5">
        <span class="field-label">cm</span>
      </div>
      <div class="field-row">
        <span>e_y</span>
        <input type="number" id="ey${i}" value="0" step="0.5">
        <span class="field-label">cm</span>
      </div>`;
    grid.appendChild(div);
  }
}
buildPileInputs();

/* ตำแหน่งมาตรฐาน layout เสาเข็ม */
function getPilePositions(n, S) {
  const pos = [];
  if (n === 2) {
    pos.push([-S/2, 0], [S/2, 0]);
  } else if (n === 3) {
    const h = S * Math.sqrt(3) / 2;
    pos.push([-S/2, -h/3], [S/2, -h/3], [0, 2*h/3]);
  } else if (n === 4) {
    pos.push([-S/2, -S/2], [S/2, -S/2], [S/2, S/2], [-S/2, S/2]);
  } else if (n === 5) {
    pos.push([-S/2, -S/2], [S/2, -S/2], [S/2, S/2], [-S/2, S/2], [0, 0]);
  } else if (n === 6) {
    pos.push([-S, -S/2], [0, -S/2], [S, -S/2], [-S, S/2], [0, S/2], [S, S/2]);
  }
  return pos;
}

function calculate() {
  const Q      = parseFloat(document.getElementById('Q').value)     || 100;
  const Qsafe  = parseFloat(document.getElementById('Qsafe').value) || 40;
  const n      = parseInt(nSlider.value);
  const S      = parseFloat(document.getElementById('S').value)     || 120;

  const nomPos = getPilePositions(n, S);
  const exArr  = [], eyArr = [];
  for (let i = 0; i < n; i++) {
    exArr.push(parseFloat(document.getElementById('ex' + i).value) || 0);
    eyArr.push(parseFloat(document.getElementById('ey' + i).value) || 0);
  }

  /* ตำแหน่งจริงหลังเยื้อง */
  const actualX = nomPos.map((p, i) => p[0] + exArr[i]);
  const actualY = nomPos.map((p, i) => p[1] + eyArr[i]);

  /* Centroid ใหม่ */
  const Xbar = actualX.reduce((a, b) => a + b, 0) / n;
  const Ybar = actualY.reduce((a, b) => a + b, 0) / n;

  /* โมเมนต์ที่เกิดจากการเยื้อง */
  const Mx = Q * Ybar;
  const My = Q * Xbar;

  /* พิกัดใหม่จาก Centroid ใหม่ */
  const xi = actualX.map(x => x - Xbar);
  const yi = actualY.map(y => y - Ybar);

  const sumX2  = xi.reduce((a, b) => a + b * b, 0);
  const sumY2  = yi.reduce((a, b) => a + b * b, 0);
  const sumXY  = xi.reduce((a, v, i) => a + v * yi[i], 0);
  const denom  = sumX2 * sumY2 - sumXY * sumXY;

  let Pi = [];
  if (Math.abs(sumXY) < 1e-9 || Math.abs(denom) < 1e-9) {
    /* กรณีแกนหลักตรงกัน (สมมาตร) */
    Pi = xi.map((x, i) =>
      Q / n
      + (sumX2 > 1e-9 ? My * x / sumX2 : 0)
      + (sumY2 > 1e-9 ? Mx * yi[i] / sumY2 : 0)
    );
  } else {
    /* กรณีทั่วไป — Bakhoum (1992) */
    const m  = (My * sumY2 - Mx * sumXY) / denom;
    const nv = (Mx * sumX2 - My * sumXY) / denom;
    Pi = xi.map((x, i) => Q / n + m * x + nv * yi[i]);
  }

  drawDiagram(n, nomPos, actualX, actualY, Xbar, Ybar, exArr, eyArr, S, xi, yi);

  /* แสดง Centroid cards */
  document.getElementById('centroidCards').innerHTML = `
    <div class="metric"><div class="lbl">X̄ (Centroid แกน X)</div><div class="val">${Xbar.toFixed(2)}</div><div class="sub">cm</div></div>
    <div class="metric"><div class="lbl">Ȳ (Centroid แกน Y)</div><div class="val">${Ybar.toFixed(2)}</div><div class="sub">cm</div></div>
    <div class="metric"><div class="lbl">Mₓ = Q × Ȳ</div><div class="val">${Mx.toFixed(1)}</div><div class="sub">ตัน-cm</div></div>
    <div class="metric"><div class="lbl">My = Q × X̄</div><div class="val">${My.toFixed(1)}</div><div class="sub">ตัน-cm</div></div>
    <div class="metric"><div class="lbl">Σx²</div><div class="val">${sumX2.toFixed(1)}</div><div class="sub">cm²</div></div>
    <div class="metric"><div class="lbl">Σy²</div><div class="val">${sumY2.toFixed(1)}</div><div class="sub">cm²</div></div>
    <div class="metric"><div class="lbl">Σxy</div><div class="val">${sumXY.toFixed(1)}</div><div class="sub">cm²</div></div>`;

  /* แสดงแรงแต่ละต้น */
  const resDiv = document.getElementById('pileResults');
  resDiv.innerHTML = '';
  Pi.forEach((p, i) => {
    const pct = p / Qsafe * 100;
    let cls = 'ok', txt = 'ปลอดภัย';
    if (pct > 100) { cls = 'over'; txt = 'เกินขีดจำกัด!'; }
    else if (pct > 80) { cls = 'warn'; txt = 'เฝ้าระวัง'; }
    resDiv.innerHTML += `
      <div class="pile-result-row">
        <div style="font-size:13px;font-weight:500">เสาเข็มที่ ${i + 1}</div>
        <div style="font-size:12px;color:#5F5E5A">x=${xi[i].toFixed(1)}, y=${yi[i].toFixed(1)} cm</div>
        <div style="font-size:16px;font-weight:500">${p.toFixed(2)} ตัน</div>
        <div style="font-size:12px;color:#5F5E5A">${pct.toFixed(0)}% ของ P_allow</div>
        <span class="badge ${cls}">${txt}</span>
      </div>`;
  });

  document.getElementById('diagram-wrap').style.display = 'block';
  document.getElementById('resultsSection').style.display = 'block';
  document.getElementById('diagram-wrap').scrollIntoView({ behavior: 'smooth' });
}

/* ---------- วาดแผนภาพ ---------- */
function drawDiagram(n, nomPos, actualX, actualY, Xbar, Ybar, exArr, eyArr, S, xi, yi) {
  const canvas = document.getElementById('diagramCanvas');
  const ctx    = canvas.getContext('2d');
  const W = 660, H = 340;
  canvas.width = W; canvas.height = H;
  ctx.clearRect(0, 0, W, H);

  const textC  = '#2C2C2A';
  const borderC = 'rgba(0,0,0,0.12)';
  const nomC   = '#378ADD';
  const actC   = '#D85A30';
  const centC  = '#1D9E75';
  const arrowC = '#EF9F27';

  /* หา scale */
  const allX = [...nomPos.map(p => p[0]), ...actualX, Xbar];
  const allY = [...nomPos.map(p => p[1]), ...actualY, Ybar];
  const minX = Math.min(...allX) - S * 0.9;
  const maxX = Math.max(...allX) + S * 0.9;
  const minY = Math.min(...allY) - S * 0.9;
  const maxY = Math.max(...allY) + S * 0.9;
  const rangeX = maxX - minX || S * 2;
  const rangeY = maxY - minY || S * 2;
  const scale  = Math.min((W - 120) / rangeX, (H - 80) / rangeY);

  const cx = x => (x - minX) * scale + 60;
  const cy = y => H - ((y - minY) * scale + 40);

  /* พื้นที่ฐานราก (outline) */
  const bx1 = Math.min(...actualX), bx2 = Math.max(...actualX);
  const by1 = Math.min(...actualY), by2 = Math.max(...actualY);
  const pad = S * 0.38;
  ctx.fillStyle = 'rgba(55,138,221,0.05)';
  ctx.strokeStyle = borderC;
  ctx.lineWidth = 0.5;
  ctx.beginPath();
  ctx.roundRect(cx(bx1 - pad), cy(by2 + pad),
    (bx2 - bx1 + 2 * pad) * scale,
    (by2 - by1 + 2 * pad) * scale, 6);
  ctx.fill(); ctx.stroke();

  /* แกน XY */
  const ox = cx(0), oy = cy(0);
  ctx.strokeStyle = 'rgba(0,0,0,0.2)';
  ctx.lineWidth = 0.5;
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(ox, cy(minY)); ctx.lineTo(ox, cy(maxY)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx(minX), oy); ctx.lineTo(cx(maxX), oy); ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = '#888780'; ctx.font = '11px sans-serif';
  ctx.textAlign = 'center'; ctx.fillText('Y', ox, cy(maxY) - 4);
  ctx.textAlign = 'left';   ctx.fillText('X', cx(maxX) + 4, oy + 4);

  /* ตำแหน่งออกแบบ (วงกลมประ) */
  nomPos.forEach(p => {
    ctx.beginPath(); ctx.arc(cx(p[0]), cy(p[1]), 12, 0, Math.PI * 2);
    ctx.strokeStyle = nomC; ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 3]); ctx.stroke(); ctx.setLineDash([]);
  });

  /* เส้นเยื้อง */
  nomPos.forEach((p, i) => {
    if (exArr[i] !== 0 || eyArr[i] !== 0) {
      ctx.beginPath();
      ctx.moveTo(cx(p[0]), cy(p[1]));
      ctx.lineTo(cx(actualX[i]), cy(actualY[i]));
      ctx.strokeStyle = arrowC; ctx.lineWidth = 1.5; ctx.stroke();
    }
  });

  /* ตำแหน่งจริง */
  actualX.forEach((ax, i) => {
    const ay = actualY[i];
    ctx.beginPath(); ctx.arc(cx(ax), cy(ay), 13, 0, Math.PI * 2);
    ctx.fillStyle = actC + '30'; ctx.fill();
    ctx.beginPath(); ctx.arc(cx(ax), cy(ay), 13, 0, Math.PI * 2);
    ctx.strokeStyle = actC; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = textC; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText(i + 1, cx(ax), cy(ay));
    ctx.font = '11px sans-serif';
    if (exArr[i] !== 0 || eyArr[i] !== 0) {
      ctx.fillStyle = arrowC;
      const ex = exArr[i] >= 0 ? '+' + exArr[i] : '' + exArr[i];
      const ey = eyArr[i] >= 0 ? '+' + eyArr[i] : '' + eyArr[i];
      ctx.fillText(`(${ex},${ey})`, cx(ax), cy(ay) - 20);
    }
  });

  /* Centroid ใหม่ */
  if (Math.abs(Xbar) > 0.01 || Math.abs(Ybar) > 0.01) {
    const cgx = cx(Xbar), cgy = cy(Ybar);
    ctx.beginPath();
    ctx.moveTo(cgx - 8, cgy); ctx.lineTo(cgx + 8, cgy);
    ctx.moveTo(cgx, cgy - 8); ctx.lineTo(cgx, cgy + 8);
    ctx.strokeStyle = centC; ctx.lineWidth = 2.5; ctx.stroke();
    ctx.beginPath(); ctx.arc(cgx, cgy, 5, 0, Math.PI * 2);
    ctx.fillStyle = centC; ctx.fill();
    ctx.fillStyle = centC; ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
    ctx.font = '11px sans-serif';
    ctx.fillText(`Centroid ใหม่ (${Xbar.toFixed(2)}, ${Ybar.toFixed(2)})`, cgx + 8, cgy - 4);
  }

  /* Centroid เดิม (0,0) */
  ctx.beginPath(); ctx.arc(ox, oy, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#888780'; ctx.fill();
  ctx.fillStyle = '#888780'; ctx.font = '11px sans-serif';
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
  ctx.fillText('O (0,0)', ox + 6, oy - 4);

  /* Legend */
  const legends = [
    { c: nomC,   t: 'ตำแหน่งออกแบบ', dash: true },
    { c: actC,   t: 'ตำแหน่งจริง (เยื้อง)' },
    { c: arrowC, t: 'ระยะเยื้อง' },
    { c: centC,  t: 'Centroid ใหม่' },
  ];
  let lx = 10;
  ctx.textBaseline = 'middle';
  legends.forEach(l => {
    ctx.beginPath();
    if (l.dash) ctx.setLineDash([5, 3]);
    ctx.moveTo(lx, 14); ctx.lineTo(lx + 20, 14);
    ctx.strokeStyle = l.c; ctx.lineWidth = 2; ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = textC; ctx.textAlign = 'left';
    ctx.font = '11px sans-serif';
    ctx.fillText(l.t, lx + 24, 14);
    lx += ctx.measureText(l.t).width + 44;
  });
}
</script>
</body>
</html>
