# EX2:

from PIL import Image

def draw_belgian_state_flag(filename: str) -> None:

    # Define your colors, your width and your height
    (width, height) = (300, 200)
    img = Image.new("RGB", (width, height), (0,0,0))
    pixels = img.load()

    # Here, you can fill the "pixels" map
    for x in range(width//3,2*width//3):
        for y in range(height):
            pixels[x, y] = (253, 218, 36) # Yellow
    for x in range(2*width//3,width):
        for y in range(height):
            pixels[x, y] = (239, 51, 64) # Red
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(filename)

draw_belgian_state_flag("belgium.png")


# EX4