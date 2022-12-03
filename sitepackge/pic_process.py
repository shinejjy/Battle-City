from PIL import Image, ImageSequence, ImageFilter


def gif_to_png():
    pillow_image = Image.open('../image/win.gif')
    for index, frame in enumerate(ImageSequence.all_frames(pillow_image)):
        frame.save(f"../image/win_png/gif{index}.png", quality=100)


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)
