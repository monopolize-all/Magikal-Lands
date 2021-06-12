from PIL import Image

image_path = input("Enter image path:").replace("'", "")

image = Image.open(image_path)

width, height = image.size

image = image.resize((width*4, height*4), resample=Image.BOX)

#image.save("test.png")
image.save(image_path)
