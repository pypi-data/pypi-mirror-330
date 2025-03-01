import glob
from PIL import Image


class GifConverter:
    """_summary_
    GIF 이미지 변환 클래스
    """

    def __init__(self, path_in=None, path_out=None, resize=(320, 240)):
        """_summary_

        Args:
            path_in: 원본 이미지 경로(예: "images/*.png")
            path_out: 결과 이미지 경로(예: "image_out/result.gif")
            resize: 리사이즈 크기(예: (320, 240))
        """
        self.path_in = path_in or "./images/*.png"
        self.path_out = path_out or "./image_out/result.gif"
        self.resize = resize

    def convert_gif(self):
        """_summary_
        GIF 이미지 변환 메서드
        """
        img, *imgs = [
            Image.open(f).resize(self.resize) for f in sorted(glob.glob(self.path_in))
        ]

        try:
            img.save(
                fp=self.path_out,
                format="GIF",
                append_images=imgs,
                save_all=True,
                duration=500,
                loop=0,
            )
            print("GIF 이미지 변환 완료")

        except IOError:
            print("Cannot convert", img)


if __name__ == "__main__":
    # 클래스
    c = GifConverter("./images/*.png", "./image_out/result.gif", (320, 240))

    # 변환
    c.convert_gif()
