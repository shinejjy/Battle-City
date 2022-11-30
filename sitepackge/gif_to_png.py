from PIL import Image, ImageSequence

pillow_image = Image.open('./image/loading2.gif')
for index, frame in enumerate(ImageSequence.all_frames(pillow_image)):
    frame.save(f"./image/loading2_png/gif{index}.png", quality=100)
