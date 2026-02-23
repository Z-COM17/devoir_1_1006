# EX2 - EX4

from PIL import Image

def draw_belgian_state_flag(filename: str) -> None:

    # Define your colors, your width and your height
    (width, height) = (300, 200)
    img = Image.new("RGB", (width, height), (0,0,0))
    pixels = img.load()

    # Here, you can fill the "pixels" map
    for x in range(width//3,2*width//3):
        for y in range(height):
            pixels[x, y] = (255, 233, 54) # Yellow
    for x in range(2*width//3,width):
        for y in range(height):
            pixels[x, y] = (239, 15, 33) # Red
    # img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(filename)
    return img

draw_belgian_state_flag("belgium.bmp")


# EX3

def draw_belgian_state_flag(filename: str, height: int) -> None:

    # Define your colors, your width and your height
    (width, height) = (height*13//15, height)
    if (height*13)%15:
        width += 1
    print(width, height)
    img = Image.new("RGB", (width, height), (0,0,0))
    pixels = img.load()

    # Here, you can fill the "pixels" map
    for x in range(width//3,2*width//3):
        for y in range(height):
            pixels[x, y] = (255, 233, 54) # Yellow
    for x in range(2*width//3,width):
        for y in range(height):
            pixels[x, y] = (255, 15, 33) # Red
    img.save(filename)

draw_belgian_state_flag("belgium.bmp", 150)

