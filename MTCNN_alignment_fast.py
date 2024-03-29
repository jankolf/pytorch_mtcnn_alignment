import os
import cv2
import numpy as np
from tqdm import tqdm
import argparse

from align_trans import norm_crop

from facenet_pytorch import MTCNN

mtcnn = MTCNN(select_largest=True, post_process=False, device='cuda:4')



def align_images(in_folder, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    skipped_imgs = []

    img_names = os.listdir(in_folder)
    for img_name in tqdm(img_names):
        filepath = os.path.join(in_folder, img_name)
        img = cv2.imread(filepath)

        boxes, probs, landmarks = mtcnn.detect(img, landmarks=True)

        if landmarks is None:
            skipped_imgs.append(img_name)
            continue

        facial5points = landmarks[0]

        warped_face, _ = norm_crop(img, landmark=facial5points, createEvalDB=True)
        cv2.imwrite(os.path.join(out_folder, img_name), warped_face)

    print(skipped_imgs)
    print(f"Images with no Face: {len(skipped_imgs)}")


def main():
    parser = argparse.ArgumentParser(description='MTCNN alignment')
    parser.add_argument('--in_folder', type=str, default="./out_large", help='folder with images')
    parser.add_argument('--out_folder', type=str, default="./out_aligned", help="folder to save aligned images")

    args = parser.parse_args()
    align_images(args.in_folder, args.out_folder)


if __name__ == "__main__":
    main()
