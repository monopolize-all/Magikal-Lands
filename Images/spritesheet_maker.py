from PIL import Image

WIDTH, HEIGHT = 64, 64

x_start, y_start = 0, 0

sprites = []

while True:
    image_path = input("Enter image path:").replace("'", "")
    
    if not image_path: break

    elif image_path == "next":
        y_start += HEIGHT
        x_start = 0

    else:
        image = Image.open(image_path)

        image_resized = image.resize((WIDTH, HEIGHT), resample=Image.BOX)

        sprites.append([x_start, y_start, image_resized])

        x_start += WIDTH


spritesheet = new_im = Image.new('RGBA', (x_start, y_start + HEIGHT))

for x, y, sprite in sprites:
    spritesheet.paste(sprite, (x, y))

save_name = input("Enter save name: ")

spritesheet.save(save_name)
