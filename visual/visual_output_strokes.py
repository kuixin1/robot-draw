import matplotlib.pyplot as plt
import os

def plot_all_strokes(strokes_dir, save_path=None):
    plt.figure(figsize=(6,6))
    files = sorted([f for f in os.listdir(strokes_dir) if f.endswith('.txt')])
    for file in files:
        xs, ys = [], []
        with open(os.path.join(strokes_dir, file), 'r') as f:
            for line in f:
                x, y, *_ = map(float, line.strip().split(','))
                xs.append(x)
                ys.append(y)
        plt.plot(xs, ys, '-', color='black', linewidth=1)
        plt.scatter(xs, ys, s=2, color='black')
    plt.xlim(0, 40)
    plt.ylim(0, 40)
    plt.gca().set_aspect('equal')
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.title('All Strokes')
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图片已保存为: {save_path}")
    plt.show()

# 展示并保存所有笔画
plot_all_strokes('output_strokes', save_path='visual/all_strokes.png')