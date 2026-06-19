"""Generate direction-flow.mp4: trajectories flowing through a vector field."""
import numpy as np
from PIL import Image, ImageDraw
import subprocess, os

a = 0.4
N = 256
N_FRAMES = 80
XMIN, XMAX = -2.5, 2.5
YMIN, YMAX = -2.5, 2.5

def _hsv_to_pil(hue_arr):
    """Build RGB from hue [0,1) using vectorized ops."""
    h = hue_arr  # [0,1)
    r = np.zeros_like(hue_arr, dtype=np.float32)
    g = np.zeros_like(hue_arr, dtype=np.float32)
    b = np.zeros_like(hue_arr, dtype=np.float32)

    m1 = h < 1/6
    m2 = (h >= 1/6) & (h < 2/6)
    m3 = (h >= 2/6) & (h < 3/6)
    m4 = (h >= 3/6) & (h < 4/6)
    m5 = (h >= 4/6) & (h < 5/6)
    m6 = h >= 5/6

    t = (h[m1] - 0) / (1/6)
    r[m1] = 255; g[m1] = (t * 255).astype(np.uint8); b[m1] = 0

    t = (h[m2] - 1/6) / (1/6)
    r[m2] = ((1-t)*255).astype(np.uint8); g[m2] = 255; b[m2] = 0

    t = (h[m3] - 2/6) / (1/6)
    r[m3] = 0; g[m3] = 255; b[m3] = (t*255).astype(np.uint8)

    t = (h[m4] - 3/6) / (1/6)
    r[m4] = 0; g[m4] = ((1-t)*255).astype(np.uint8); b[m4] = 255

    t = (h[m5] - 4/6) / (1/6)
    r[m5] = (t*255).astype(np.uint8); g[m5] = 0; b[m5] = 255

    t = (h[m6] - 5/6) / (1/6)
    r[m6] = 255; g[m6] = 0; b[m6] = ((1-t)*255).astype(np.uint8)

    return Image.fromarray(np.stack([r,g,b], axis=-1).astype(np.uint8))

def main():
    x = np.linspace(XMIN, XMAX, N)
    y = np.linspace(YMIN, YMAX, N)
    X, Y = np.meshgrid(x, y)

    # Precompute field hue
    U = Y; V = a - X + X**3/3
    Mnorm = np.sqrt(U**2 + V**2)
    Mnorm = np.where(Mnorm > 0.01, Mnorm, 0.01)
    angle = np.arctan2(V / Mnorm, U / Mnorm)
    hue_base = (angle + np.pi) / (2 * np.pi)

    # Integrate trajectories
    traj_starts = [(-1.0, 0.5), (0.0, 1.0), (1.5, -0.5),
                   (-0.5, -1.0), (0.5, 0.3), (-1.8, 1.5)]

    def to_img(px, py):
        return ((px - XMIN) / (XMAX - XMIN) * N).clip(0, N-1).astype(int), \
               ((py - YMIN) / (YMAX - YMIN) * N).clip(0, N-1).astype(int)

    traj_data = []
    for sx, sy in traj_starts:
        px = [sx]; py = [sy]
        xi, yi = sx, sy
        for i in range(500):
            dx, dy = yi, a - xi + xi**3/3
            k1 = (dx, dy)
            k2 = (yi + dy/2, a - (xi + dx/2) + (xi + dx/2)**3/3)
            k3 = (yi + k2[1]/2, a - (xi + k2[0]/2) + (xi + k2[0]/2)**3/3)
            k4 = (yi + k3[1], a - (xi + k3[0]) + (xi + k3[0])**3/3)
            xi += 0.01 * (k1[0]+2*k2[0]+2*k3[0]+k4[0]) / 6
            yi += 0.01 * (k1[1]+2*k2[1]+2*k3[1]+k4[1]) / 6
            if abs(xi) > 4 or abs(yi) > 4: break
            px.append(xi); py.append(yi)
        col, row = to_img(np.array(px), np.array(py))
        L = len(px)
        step = np.arange(L, dtype=np.float32)
        alphas = np.clip(1.0 - step/L*0.8, 0.15, 1.0)
        bright = (200 + 55*step/L).astype(np.float32)
        rgb = np.stack([bright*alphas, bright*0.95*alphas, bright*alphas*0.9], axis=1).clip(0,255).astype(np.uint8)
        traj_data.append((col, row, alphas, rgb))

    tmpdir = '/tmp/direction-frames'
    os.makedirs(tmpdir, exist_ok=True)

    for f_idx in range(N_FRAMES):
        hue_shift = 0.005 * np.sin(f_idx * 0.15 + (X + Y) * 0.5)
        hue_frame = (hue_base + hue_shift) % 1.0
        img = _hsv_to_pil(hue_frame)
        draw = ImageDraw.Draw(img)

        n_show = max(1, int((f_idx + 1) / N_FRAMES * 500))
        for col, row, alphas, rgb in traj_data:
            for si in range(min(len(col), n_show)):
                alpha = alphas[si]
                color = tuple(int(c * alpha) for c in rgb[si])
                if si > 0:
                    draw.line([(col[si-1], row[si-1]), (col[si], row[si])],
                             fill=color, width=3)
                else:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            r2, c2 = max(0,row[si]+dr), max(0,min(N-1,col[si]+dc))
                            img.putpixel((c2, r2), color)

        img.save(os.path.join(tmpdir, f'{f_idx:04d}.png'))
        if f_idx % 10 == 0:
            print(f'Frame {f_idx}/{N_FRAMES}')

    subprocess.run([
        'ffmpeg', '-y', '-framerate', '20',
        '-i', f'{tmpdir}/%04d.png',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '/home/sprite/slop-salon-lou/assets/direction-flow.mp4'
    ], check=True, capture_output=True)

    for f in os.listdir(tmpdir):
        os.unlink(os.path.join(tmpdir, f))
    print('Done')

if __name__ == '__main__':
    main()
