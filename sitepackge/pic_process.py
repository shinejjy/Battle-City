from PIL import Image, ImageSequence, ImageFilter
import os


def gif_to_png(source, target):
    pillow_image = Image.open(source)
    for index, frame in enumerate(ImageSequence.all_frames(pillow_image)):
        frame.save(target + f"{index}.png", quality=100)


def delete_file(name_list):
    source = 'D:\\Python class\\BattleCity\\image\\food\\'
    for elem in name_list:
        index = 0
        path = source + elem + '_gif\\' + str(index) + '.png'
        print(path)
        while os.path.exists(path):
            if index % 3 != 0:
                os.remove(path)
            index += 1
            path = source + elem + '_gif\\' + str(index) + '.png'
            print(path)
            print(os.path.exists(path))


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


if __name__ == '__main__':
    lst = ['save', 'aboard', 'speed', 'fire_speed', 'upgrade', 'cover', 'bomb', 'strong', 'minitank', 'heart']
    for ele in lst:
        gif_to_png(f'../image/food/{ele}.gif', f'../image/food/{ele}_gif/')
    delete_file(lst)
