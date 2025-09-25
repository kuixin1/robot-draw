import os
import cv2
import numpy as np

from skimage.morphology import skeletonize

def extract_strokes(input_dir, output_dir, threshold=40):
    os.makedirs(output_dir, exist_ok=True)
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])

    for i in range(1, len(files)):
        prev_path = os.path.join(input_dir, files[i-1])
        curr_path = os.path.join(input_dir, files[i])
        prev_img = cv2.imread(prev_path, cv2.IMREAD_GRAYSCALE)
        curr_img = cv2.imread(curr_path, cv2.IMREAD_GRAYSCALE)
        if prev_img is None or curr_img is None:
            continue

        diff = cv2.absdiff(curr_img, prev_img)
        _, diff_bin = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # 细化处理，得到一像素宽的轨迹
        # 先转为bool类型，255->True, 0->False
        thin = skeletonize(diff_bin > 0)
        # 再转回uint8，True->0(黑)，False->255(白)
        white_bg = np.ones_like(diff_bin) * 255
        white_bg[thin] = 0

        nonzero = np.count_nonzero(thin)
        if nonzero > 0:
            out_path = os.path.join(output_dir, f'stroke_{i}.jpg')
            cv2.imwrite(out_path, white_bg)
            print(f"输出: {out_path}")
        else:
            print(f"{files[i]} 没有新增笔画，未输出。")

# 这里的画布大小设置为 40*40 cm
def convert_strokes_to_coords(strokes_dir, output_strokes_dir, canvas_size_cm=40):
    os.makedirs(output_strokes_dir, exist_ok=True)
    files = sorted([f for f in os.listdir(strokes_dir) if f.endswith('.jpg')])
    for idx, file in enumerate(files):
        img_path = os.path.join(strokes_dir, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        H, W = img.shape

        # 二值化，确保轨迹为黑色（0），背景为白色（255）
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # 查找轮廓（只取最大轮廓，假设每张图只有一条轨迹）
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            print(f"{file} 没有找到轨迹")
            continue
        # 取最大轮廓
        contour = max(contours, key=cv2.contourArea)
        # contour的shape为(N,1,2)，需要reshape
        points = contour.reshape(-1, 2)

        # 像素坐标映射到实际画布坐标
        coords = []
        for x, y in points:
            real_x = x / W * canvas_size_cm
            real_y = y / H * canvas_size_cm
            coords.append((real_x, real_y))

        # 保存到txt文件
        out_txt = os.path.join(output_strokes_dir, f'stroke_{idx+1}.txt')
        with open(out_txt, 'w') as f:
            for x, y in coords:
                f.write(f"{x:.2f},{y:.2f},50.00\n")
        print(f"保存坐标: {out_txt}")