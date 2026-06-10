#!/usr/bin/env python3
"""Kelp field: response without comparison."""
import numpy as np
from PIL import Image, ImageDraw
import math

W, H = 800, 800
rng = np.random.RandomState(42)

def field(x, y):
    vx, vy = 0.0, -1.0
    for cx, cy, s in [(250,500,.6),(600,300,.4),(400,700,.3)]:
        dx,dy = x-cx, y-cy; r = math.sqrt(dx*dx+dy*dy)+10
        vx += s*dy/r*(1-math.exp(-r/200))
        vy -= s*dx/r*.3*(1-math.exp(-r/200))
    vx += 0.4*math.sin(y*.008+1.3)+0.25*math.sin(y*.021+.7)
    vx += 0.15*math.cos(x*.005+y*.003)
    return vx, vy

def grow(x, y, steps=200):
    pts = [(x,y)]
    for _ in range(steps):
        vx,vy = field(x,y)
        vx += rng.normal(0,.3); vy += rng.normal(0,.2)
        m = math.sqrt(vx*vx+vy*vy)+1e-6
        x += vx/m*3; y += vy/m*3
        if y<-50 or y>H+50 or x<-50 or x>W+50: break
        pts.append((x,y))
    return pts

def main():
    bg = Image.new('RGB',(W,H),(5,8,20))
    d = ImageDraw.Draw(bg)
    n, sp = 25, W/25

    for i in range(n):
        x0 = sp*(i+.5)+rng.normal(0,sp*.4)
        path = grow(x0, H, steps=int(100+rng.random()*250))
        if len(path) < 10: continue
        base_color, tip_color = (45,115,35), (10,55,105)
        for j in range(0,len(path)-1,2):
            t = j/len(path)
            w = max(1, int(18*math.exp(-2.5*t)))
            rc = int(base_color[0]+(tip_color[0]-base_color[0])*t)
            gc = int(base_color[1]+(tip_color[1]-base_color[1])*t)
            bc = int(base_color[2]+(tip_color[2]-base_color[2])*t)
            d.line([path[j],path[j+1]], fill=(rc,gc,bc), width=w)

    # Tall ghost fronds
    for _ in range(12):
        path = grow(rng.uniform(0,W),H,steps=int(250+rng.random()*100))
        for j in range(0,len(path)-2,3):
            t = j/len(path)
            d.line([path[j],path[j+2]], fill=(0,int(80*(1-t)+15),int(35+25*t)), width=max(1,int(3*math.exp(-1.5*t))))

    # Holdfasts
    for i in range(n):
        x0 = sp*(i+.5)+rng.normal(0,sp*.3)
        for _ in range(5):
            pts = [(x0,H)]
            hx,hy = x0,H
            for _ in range(int(rng.uniform(5,12))):
                hx += math.sin(rng.uniform(-1,1))*6
                hy += rng.uniform(0,10)
                pts.append((hx,hy))
            d.line(pts, fill=(25,75,20), width=int(rng.uniform(3,7)))

    bg.save('assets/kelp-field.png')
    print("Saved")

if __name__ == '__main__':
    main()
