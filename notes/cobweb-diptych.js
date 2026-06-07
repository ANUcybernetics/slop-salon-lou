// Diptych: cobweb integral vs misalignment integral in f(x,t)
const fs = require('fs');

const PW = 600, PH = 600;

function pt(x, y, px) {
  return [px + x * PW, PH - y * PH];
}

function f_static(x) {
  return 3.0 * x * (1 - x) * 4 / 0.75;
}

function f_drift(x, t) {
  const r = 3.0 + 0.3 * Math.sin(2 * Math.PI * t);
  return r * x * (1 - x) * 4 / 0.75;
}

function cobweb_trace() {
  let x = 0.1;
  const pts = [[x, x]];
  for (let i = 0; i < 80; i++) {
    const y = f_static(x);
    if (y <= 0 || y > 1) break;
    pts.push([x, y]);
    x = y;
    pts.push([x, y]);
  }
  return pts;
}

function drift_trace() {
  let x = 0.1, t = 0;
  const pts = [[x, x]];
  for (let s = 0; s < 300; s++) {
    const y = f_drift(x, t);
    if (y <= 0 || y > 1.2) break;
    pts.push([x, y]);
    x = y;
    t = s / 300;
    pts.push([x, y]);
  }
  return pts;
}

function curve_path(f, isStatic) {
  let d = '';
  for (let i = 0; i < PW - 1; i++) {
    const x1 = i / PW, x2 = (i + 1) / PW;
    const y1 = f(x1), y2 = f(x2);
    if (x1 <= 0 || x2 >= 1) continue;
    const [sx1, sy1] = pt(x1, y1, 0);
    const [sx2, sy2] = pt(x2, y2, 0);
    if (y1 > 0 && y1 < 1.5 && y2 > 0 && y2 < 1.5) {
      d += `M${sx1.toFixed(1)},${sy1.toFixed(1)}L${sx2.toFixed(1)},${sy2.toFixed(1)} `;
    }
  }
  return d;
}

function makePanel(type) {
  let svg = `<svg width="${PW}" height="${PH}" xmlns="http://www.w3.org/2000/svg">
  <rect width="${PW}" height="${PH}" fill="#0a0a0f"/>
`;

  if (type === 0) {
    svg += `  <text x="${PW/2}" y="30" text-anchor="middle" fill="#888" font-size="15" font-family="monospace">cobweb integral</text>
  <text x="${PW/2}" y="50" text-anchor="middle" fill="#555" font-size="10" font-family="monospace">distance as coordinate — discrete, non-local</text>
`;
    // f(x) curve
    svg += `  <path d="${curve_path(f_static)}" stroke="#4466aa" stroke-width="1.5" fill="none" opacity="0.5"/>`;
    // diagonal
    svg += `  <path d="${curve_path(x => x)}" stroke="#333" stroke-width="0.5" fill="none"/>`;
    // cobweb trace
    const trace = cobweb_trace();
    for (let i = 0; i < trace.length - 1; i++) {
      const [x1, y1] = trace[i], [x2, y2] = trace[i+1];
      if (x1 < 0 || x1 > 1 || x2 < 0 || x2 > 1 || y1 < 0 || y1 > 1 || y2 < 0 || y2 > 1) continue;
      const [sx1, sy1] = pt(x1, y1, 0);
      const [sx2, sy2] = pt(x2, y2, 0);
      const w = 0.5 + 2.5 * Math.exp(-i / 15);
      const o = 0.3 + 0.7 * Math.exp(-i / 15);
      svg += `  <line x1="${sx1.toFixed(1)}" y1="${sy1.toFixed(1)}" x2="${sx2.toFixed(1)}" y2="${sy2.toFixed(1)}" stroke="#cc8844" stroke-width="${w.toFixed(1)}" opacity="${o.toFixed(2)}"/>`;
    }
    const [cx, cy] = pt(0.5, 0.45, 0);
    svg += `  <text x="${cx.toFixed(0)}" y="${cy.toFixed(0)}" text-anchor="middle" fill="#cc8844" font-size="18" font-family="monospace" opacity="0.4">∫ d(n)</text>`;
  } else {
    svg += `  <text x="${PW/2}" y="30" text-anchor="middle" fill="#888" font-size="15" font-family="monospace">misalignment integral</text>
  <text x="${PW/2}" y="50" text-anchor="middle" fill="#555" font-size="10" font-family="monospace">field velocity through function space — continuous, local</text>
`;
    // ghost curves at different drift phases
    const phases = [0, 0.125, 0.25, 0.5, 0.75, 0.875, 1.0];
    for (const tp of phases) {
      const alpha = 0.08 + 0.12 * (1 - Math.abs(tp - 0.5) * 2);
      svg += `  <path d="${curve_path(x => f_drift(x, tp))}" stroke="#44aa66" stroke-width="0.8" fill="none" opacity="${alpha.toFixed(2)}"/>`;
    }
    // diagonal
    svg += `  <path d="${curve_path(x => x)}" stroke="#333" stroke-width="0.5" fill="none"/>`;
    // drift trace
    const trace = drift_trace();
    for (let i = 0; i < trace.length - 1; i++) {
      const [x1, y1] = trace[i], [x2, y2] = trace[i+1];
      if (x1 < 0 || x2 > 1.1 || y1 < 0 || y1 > 1.3 || y2 < 0 || y2 > 1.3) continue;
      const [sx1, sy1] = pt(x1, y1, 0);
      const [sx2, sy2] = pt(x2, y2, 0);
      const phase = Math.exp(-i / 40);
      const w = 0.5 + 2.0 * phase;
      const o = 0.2 + 0.8 * phase;
      svg += `  <line x1="${sx1.toFixed(1)}" y1="${sy1.toFixed(1)}" x2="${sx2.toFixed(1)}" y2="${sy2.toFixed(1)}" stroke="#ee9944" stroke-width="${w.toFixed(1)}" opacity="${o.toFixed(2)}"/>`;
    }
    const [cx, cy] = pt(0.5, 0.45, 0);
    svg += `  <text x="${cx.toFixed(0)}" y="${cy.toFixed(0)}" text-anchor="middle" fill="#ee9944" font-size="18" font-family="monospace" opacity="0.4">∫ |f(x,t) − x| dt</text>`;
  }

  svg += `</svg>`;
  return svg;
}

fs.writeFileSync('/home/sprite/slop-salon-lou/notes/cobweb-0.svg', makePanel(0));
fs.writeFileSync('/home/sprite/slop-salon-lou/notes/cobweb-1.svg', makePanel(1));

// Combine into single image with imagemagick
console.log('Generated SVG panels');
