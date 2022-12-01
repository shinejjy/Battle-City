from PIL import Image, ImageSequence

pillow_image = Image.open('../image/win.gif')
for index, frame in enumerate(ImageSequence.all_frames(pillow_image)):
    frame.save(f"../image/win_png/gif{index}.png", quality=100)
