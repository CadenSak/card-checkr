import os
from PIL import Image, ImageEnhance
from math import floor

YELLOW = (255, 255, 0)


def normalize_card_images(directory_string:Image) -> Image:
    for g in range(len(os.listdir(directory_string))):
        img_str = str(os.listdir(directory_string)[g])
        img = Image.open(directory_string+img_str)
        final_img = _normalize_card_image(img)

def _normalize_card_image(img:Image) -> Image:

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(10)

    final_img = img.crop(find_boarders_of_card(img))

    final_img = final_img.convert("L")
    return final_img

def find_boarders_of_card(img:Image) -> tuple[int, int, int, int]:
    width, height = img.size
    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(height / 2)

    #Finds the left edge of the card
    x1 = 1
    while(img.getpixel((x1,check_pixel_length_Y)) != YELLOW and x1 < width):

        print(x1,':',img.getpixel((x1,check_pixel_length_Y)))
        x1 += 1

    #Finds the right edge of the card
    x2 = width - 1
    while(img.getpixel((x2,check_pixel_length_Y)) != YELLOW and x2 > 0):
        x2 -= 1

    #Finds the top edge of the card
    y1 = 1
    while(img.getpixel((check_pixel_width_X,y1)) != YELLOW and y1 < height):
        y1 += 1

    #Find the bottom edge of the card
    y2 = height - 1
    print(y2)
    while(img.getpixel((check_pixel_width_X,y2)) != YELLOW and y2 > 0):
        y2 -= 1

    return (x1, y1, x2, y2)

def _crop_out_card_symbol(img:Image) -> Image:
    localize_card_symbol(img)


def localize_card_symbol(img:Image) -> tuple:
    enhancer = ImageEnhance.Brightness(img)
    enhancer.enhance(10).show("test")
    img = enhancer.enhance(10)


    True

