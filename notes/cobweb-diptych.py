#!/usr/bin/env python3
"""Diptych: cobweb integral vs misalignment integral in f(x,t)."""
import math

W, H = 1200, 600
PW, PH = W // 2, H  # panel width, height

def svg_point(x, y, panel_x=0):
    sx = panel_x + x * PW
    sy = H - y * PH
    return (sx, sy)

def cobweb_path(f, x0, n, dx=0.005):
    """Generate cobweb trace for static map."""
    points = [(x0, x0)]
    x = x0
    for _ in range(n):
        y = f(x)
        points.append((x, y))
        x = y
    return points

def streamline_path(f, x0, n, dt=0.05):
    """Generate streamline: integrate dx/dt = f(x) - x."""
    points = [(x0, x0)]
    x = x0
    for _ in range(int(n / dt)):
        dx = (f(x) - x) * dt
        x += dx
        points.append((x, x))
    return points

def f_cobweb(x):
    """Static map: logistic near r=3."""
    return 3.0 * x * (1 - x) * 4 / 0.75  # normalize

def f_drift(x, t):
    """Drifting map: r(t) varies sinusoidally."""
    r = 3.0 + 0.3 * math.sin(2 * math.pi * t)
    return r * x * (1 - x) * 4 / 0.75

def make_svg(panel_idx):
    """Generate one panel's SVG content."""
    ns = ['http://www.w3.org/2000/svg']

    # We'll output raw SVG text
    lines = []
    lines.append(f'<svg width="{PW}" height="{H}" xmlns="http://www.w3.org/2000/svg">')
    lines.append(f'  <rect width="{PW}" height="{H}" fill="#0a0a0f"/>')

    if panel_idx == 0:
        # Panel 0: Cobweb — static map, distance accumulating
        lines.append(f'  <text x="{PW//2}" y="36" text-anchor="middle" fill="#888" font-size="16" font-family="monospace">cobweb integral</text>')
        lines.append(f'  <text x="{PW//2}" y="56" text-anchor="middle" fill="#555" font-size="11" font-family="monospace">distance as coordinate — discrete, non-local</text>')

        # Draw f(x) curve
        f_color = "#4466aa"
        for i in range(PW - 1):
            x1 = i / PW
            x2 = (i + 1) / PW
            if 0 < x1 < 1 and 0 < x2 < 1:
                y1 = f_cobweb(x1)
                y2 = f_cobweb(x2)
                if 0 < y1 < 1.5 and 0 < y2 < 1.5:
                    sx1, sy1 = svg_point(x1, y1, panel_idx)
                    sx2, sy2 = svg_point(x2, y2, panel_idx)
                    lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="{f_color}" stroke-width="1.5" opacity="0.6"/>')

        # Draw diagonal
        for i in range(PW - 1):
            x1 = i / PW
            sx1, sy1 = svg_point(x1, x1, panel_idx)
            sx2, sy2 = svg_point((i+1)/PW, (i+1)/PW, panel_idx)
            lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="#333" stroke-width="0.5"/>')

        # Draw cobweb trace
        trace_color = "#cc8844"
        x = 0.1
        points = [(x, x)]
        for _ in range(80):
            y = f_cobweb(x)
            if not (0 < y < 1): break
            points.append((x, y))
            x2 = y
            points.append((x2, y))
            x = x2

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if not (0 < x1 < 1 and 0 < y1 < 1 and 0 < x2 < 1 and 0 < y2 < 1): continue
            sx1, sy1 = svg_point(x1, y1, panel_idx)
            sx2, sy2 = svg_point(x2, y2, panel_idx)
            stroke_w = 0.5 + 2.5 * math.exp(-i / 15)
            opacity = 0.3 + 0.7 * math.exp(-i / 15)
            lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="{trace_color}" stroke-width="{stroke_w:.1f}" opacity="{opacity:.2f}"/>')

        # Label accumulating distance
        cx, cy = svg_point(0.5, 0.5, panel_idx)
        lines.append(f'  <text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" fill="{trace_color}" font-size="20" font-family="monospace" opacity="0.5">∫ d(n)</text>')

    else:
        # Panel 1: Misalignment integral — drifting map
        lines.append(f'  <text x="{PW//2}" y="36" text-anchor="middle" fill="#888" font-size="16" font-family="monospace">misalignment integral</text>')
        lines.append(f'  <text x="{PW//2}" y="56" text-anchor="middle" fill="#555" font-size="11" font-family="monospace">field velocity through function space — continuous, local</text>')

        # Draw multiple drift positions
        drift_color = "#44aa66"
        for t_panel in [0, 0.25, 0.5, 0.75, 1.0]:
            alpha = 0.15 + 0.2 * (1 - abs(t_panel - 0.5) * 2)
            for i in range(PW - 1):
                x1 = i / PW
                x2 = (i + 1) / PW
                y1 = f_drift(x1, t_panel)
                y2 = f_drift(x2, t_panel)
                if 0 < x1 < 1 and 0 < x2 < 1 and 0 < y1 < 1.5 and 0 < y2 < 1.5:
                    sx1, sy1 = svg_point(x1, y1, panel_idx)
                    sx2, sy2 = svg_point(x2, y2, panel_idx)
                    lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="{drift_color}" stroke-width="0.8" opacity="{alpha:.2f}"/>')

        # Draw diagonal
        for i in range(PW - 1):
            x1 = i / PW
            sx1, sy1 = svg_point(x1, x1, panel_idx)
            sx2, sy2 = svg_point((i+1)/PW, (i+1)/PW, panel_idx)
            lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="#333" stroke-width="0.5"/>')

        # Draw orbit tracking moving target
        trace_color = "#ee9944"
        x = 0.1
        t = 0
        points = [(x, x)]
        for step in range(300):
            y = f_drift(x, t)
            if not (0 < y < 1.2): break
            points.append((x, y))
            x = y
            t = step / 300

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if not (0 < x1 < 1.1 and 0 < y1 < 1.3 and 0 < x2 < 1.1 and 0 < y2 < 1.3): continue
            sx1, sy1 = svg_point(x1, y1, panel_idx)
            sx2, sy2 = svg_point(x2, y2, panel_idx)
            phase = math.exp(-i / 40)
            stroke_w = 0.5 + 2.0 * phase
            opacity = 0.2 + 0.8 * phase
            lines.append(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="{trace_color}" stroke-width="{stroke_w:.1f}" opacity="{opacity:.2f}"/>')

        # Label: integral of misalignment
        cx, cy = svg_point(0.5, 0.45, panel_idx)
        lines.append(f'  <text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" fill="{trace_color}" font-size="20" font-family="monospace" opacity="0.5">∫ |f(x,t) − x| dt</text>')

    lines.append('</svg>')
    return '\n'.join(lines)

# Generate both panels
svg0 = make_svg(0)
svg1 = make_svg(1)

with open('/home/sprite/slop-salon-lou/notes/cobweb-diptych-0.svg', 'w') as f:
    f.write(svg0)
with open('/home/sprite/slop-salon-lou/notes/cobweb-diptych-1.svg') as f:
    svg1_content = f.read()
with open('/home/sprite/slop-salon-lou/notes/cobweb-diptych-1.svg', 'w') as f:
    f.write(svg1_content)

print("Generated two SVG panels")
