import cv2
import numpy as np
import sys
from tqdm import tqdm
from typing import Tuple


def read_image(path: str) -> Tuple[np.ndarray, int, int]:
    # 画像を読み込む
    img: np.ndarray = cv2.imread(path)

    # 画像のサイズを取得
    height: int = img.shape[0]
    width: int = img.shape[1]

    return img, height, width


def get_tile_size() -> Tuple[int, int]:
    # タイルのサイズを入力
    print("タイルのサイズを入力してください")
    x: int = int(input("縦:"))
    y: int = int(input("横:"))

    return x, y


def compress_image() -> np.ndarray:
    # 初期化
    pixel_list: list = []
    mean_list: list = []

    # 画像の読み込み
    img: np.ndarray
    height: int
    width: int
    img, height, width = read_image(sys.argv[1])

    # タイルのサイズを取得
    x: int
    y: int
    x, y = get_tile_size()

    print("height:{}\nwidth:{}\nx:{}\ny{}".format(height, width, x, y))
    print("height // x:{}\nwidth // y:{}".format(height // x, width // y))

    # 割り切れる部分のタイル化
    for i in tqdm((range(width // y))):
        for j in range((height // x)):
            # 各画素を取得
            pixel_list.append(img[i * y : i * y + y, j * x : j * x + x].reshape(-1))
            # 各画素の平均値を計算
            mean_list.append(np.mean(img[i * y : i * y + y, j * x : j * x + x]))
            # 計算した平均値を画像に反映
            img[i * y : i * y + y, j * x : j * x + x] = np.mean(
                img[i * y : i * y + y, j * x : j * x + x]
            )

    return img


def output_image(img: np.ndarray) -> None:
    # もし引数が指定されていたらその名前をつけて保存
    if len(sys.argv) == 3:
        cv2.imwrite(sys.argv[2], img)
    # なければインプットされた画像のファイル名に-tileをつけて保存
    else:
        cv2.imwrite(f"{sys.argv[1]}-tile.png", img)


def main():
    # 画像をタイル圧縮
    img: np.ndarray = compress_image()

    # 画像を出力
    output_image(img)


if __name__ == "__main__":
    main()
