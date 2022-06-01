import cv2
import numpy as np
import sys
from tqdm import tqdm


def read_image(path: str) -> tuple[np.ndarray, int, int]:
    # 画像を読み込む
    img: np.ndarray = cv2.imread(path)

    # 画像のサイズを取得
    height: int
    width: int
    height, width = img.shape[:2]

    return img, height, width


def get_tile_size() -> tuple[int, int]:
    # タイルのサイズを入力
    print("タイルのサイズを入力してください")
    x: int = int(input("縦:"))
    y: int = int(input("横:"))

    return x, y


def compress_image() -> np.ndarray:
    # 画像の読み込み
    img : np.ndarray
    height: int
    width: int
    img, height, width = read_image(sys.argv[1])

    # タイルのサイズを取得
    x: int
    y: int
    x, y = get_tile_size()

    return tile


def output_image(img: np.ndarray) -> None:
    # もし引数が指定されていたらその名前をつけて保存
    if len(sys.argv) == 3:
        cv2.imwrite(sys.argv[2], img)
    # なければインプットされた画像のファイル名に-tileをつけて保存
    else:
        cv2.imwrite(f"{sys.argv[1]}-tile.png", img)


def main():
    # 画像をタイル圧縮
    tile: np.ndarray = compress_image()

    # 画像を出力
    # output_image(tile)


if __name__ == "__main__":
    main()
