import os
import cv2
import numpy as np

def extract_strokes(input_dir, output_dir, threshold=20):
    os.makedirs(output_dir, exist_ok=True)
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])
    # print(f"找到图片文件: {files}")

    for i in range(1, len(files)):
        prev_path = os.path.join(input_dir, files[i-1])
        curr_path = os.path.join(input_dir, files[i])
        prev_img = cv2.imread(prev_path, cv2.IMREAD_GRAYSCALE)
        curr_img = cv2.imread(curr_path, cv2.IMREAD_GRAYSCALE)
        if prev_img is None or curr_img is None:
            # print(f"读取图片失败: {prev_path} 或 {curr_path}")
            continue

        diff = cv2.absdiff(curr_img, prev_img)
        _, diff_bin = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        white_bg = np.ones_like(diff_bin) * 255
        white_bg[diff_bin > 0] = 0

        nonzero = np.count_nonzero(diff_bin)
        # print(f"{files[i]} 新增像素点数: {nonzero}")

        if nonzero > 0:
            out_path = os.path.join(output_dir, f'stroke_{i}.jpg')
            cv2.imwrite(out_path, white_bg)
            print(f"输出: {out_path}")
        else:
            print(f"{files[i]} 没有新增笔画，未输出。")