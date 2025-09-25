import os
import matplotlib.pyplot as plt

stroke_dir = 'output_strokes'          # 目录路径
fig, ax = plt.subplots(figsize=(6, 6))

# 按文件名数字顺序排列，避免 1,10,11,2… 的顺序
files = sorted(os.listdir(stroke_dir),
               key=lambda s: int(s.split('_')[1].split('.')[0]))

for idx, fname in enumerate(files):
    if not fname.endswith('.txt'):
        continue
    path = os.path.join(stroke_dir, fname)
    coords = []
    with open(path, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split(','))
            coords.append((x, y))
    if not coords:
        continue
    x, y = zip(*coords)
    ax.plot(x, y, marker='o', label=fname)

ax.set_title('All strokes')
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.axis('equal')
ax.grid(True)
ax.legend()
plt.show()