import cv2
import numpy as np
import sys
from tqdm import tqdm


def read_image(path: str) -> tuple[np.ndarray, int, int]:
    # 画像を読み込む
    img: np.ndarray = cv2.imread(path)

    # 画像のサイズを取得
    height: int = img.shape[0]
    width: int = img.shape[1]

    return img, height, width


def get_mosaic_size() -> tuple[int, int]:
    # モザイクの大きさを入力
    print("モザイクの大きさを入力してください")
    x: int = int(input("縦:"))
    y: int = int(input("横:"))

    return x, y


def monochrome_or_color() -> bool:
    print("モノクロなら\t1\nカラーなら\t2\tを選んでください")

    try:
        choice: int = int(input("選択:"))
    except ValueError:
        print("===数字を入力してください===")
        return monochrome_or_color()

    if not (choice == 1 or choice == 2):
        print("===正しい数字を入力してください===")
        return monochrome_or_color()

    if choice == 1:
        return True
    elif choice == 2:
        return False

    return False

def mosaic_image() -> np.ndarray:
    # 初期化
    pixel_list: list = []
    mean_list: list = []

    # 画像の読み込み
    img: np.ndarray
    height: int
    width: int
    img, height, width = read_image(sys.argv[1])

    # モザイクの大きさを取得
    x: int
    y: int
    x, y = get_mosaic_size()

    # モノクロかカラーかを選ぶ
    is_monochrome: bool = monochrome_or_color()
    if is_monochrome:
        # モノクロでモザイク化
        img = monochrome(img, height, width, x, y, pixel_list, mean_list)
    else:
        # カラーでモザイク化
        img = color(img, height, width, x, y, pixel_list, mean_list)

    print(
        "height({}) // x({}) = {} ... {}\nwidth({}) // y({}) = {} ...{}".format(
            height, x, height // x, height % x, width, y, width // y, width % y
        )
    )

    return img


def monochrome(
    img: np.ndarray,
    height: int,
    width: int,
    x: int,
    y: int,
    pixel_list: list,
    mean_list: list,
) -> np.ndarray:
    # 割り切れる部分をモザイク化
    for i in tqdm((range(height // x))):
        for j in range((width // y)):
            # 各画素を取得
            pixel_list.append(img[i * y : i * y + y, j * x : j * x + x].reshape(-1))
            # 各画素の平均値を計算
            mean_list.append(np.mean(img[i * y : i * y + y, j * x : j * x + x]))
            # 計算した平均値を画像に反映
            img[i * y : i * y + y, j * x : j * x + x] = np.mean(
                img[i * y : i * y + y, j * x : j * x + x]
            )

    return img


def color(
    img: np.ndarray,
    height: int,
    width: int,
    x: int,
    y: int,
    pixel_list: list,
    mean_list: list,
) -> np.ndarray:
    # 割り切れる部分をモザイク化
    for i in tqdm((range(height // x))):
        for j in range((width // y)):
            for k in range(3):
                # 各画素を取得
                pixel_list.append(
                    img[i * y : i * y + y, j * x : j * x + x, k].reshape(-1)
                )
                # 各画素の平均値を計算
                mean_list.append(np.mean(img[i * y : i * y + y, j * x : j * x + x, k]))
                # 計算した平均値を画像に反映
                img[i * y : i * y + y, j * x : j * x + x, k] = np.mean(
                    img[i * y : i * y + y, j * x : j * x + x, k]
                )

                # リセット
                pixel_list.clear()
                mean_list.clear()

    return img


def output_image(img: np.ndarray) -> None:
    # もし引数が指定されていたらその名前をつけて保存
    if len(sys.argv) == 3:
        cv2.imwrite(sys.argv[2], img)
    # なければインプットされた画像のファイル名に-mosaicをつけて保存
    else:
        cv2.imwrite(f"{(sys.argv[1][:-4])}-mosaic.png", img)


def main():
    # 画像をモザイク化
    img: np.ndarray = mosaic_image()

    # 画像を出力
    output_image(img)


if __name__ == "__main__":
    main()
