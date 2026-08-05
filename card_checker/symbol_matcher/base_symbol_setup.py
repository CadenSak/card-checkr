import os
from PIL import Image, ImageEnhance
from math import floor

YELLOW = (255, 255, 0)
COLOR_BLACK = 0
COLOR_WHITE = 255

def find_borders_of_card(img:Image) -> tuple[int, int, int, int]:
    width, height = img.size
    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(height / 2)

    #Finds the left edge of the card
    x1 = 1
    x2 = width - 1
    y1 = 1
    y2 = height - 1
    while(img.getpixel((x1,check_pixel_length_Y)) != YELLOW and x1 < width):
        x1 += 1
    while(img.getpixel((x2,check_pixel_length_Y)) != YELLOW and x2 > 0):
        x2 -= 1
    while(img.getpixel((check_pixel_width_X,y1)) != YELLOW and y1 < height):
        y1 += 1
    while(img.getpixel((check_pixel_width_X,y2)) != YELLOW and y2 > 0):
        y2 -= 1

    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(height / 2)

    while(img.getpixel((x1,check_pixel_length_Y)) == YELLOW and x1 < width):
        x1 += 1
    while(img.getpixel((x2,check_pixel_length_Y)) == YELLOW and x2 > 0):
        x2 -= 1
    while(img.getpixel((check_pixel_width_X,y1)) == YELLOW and y1 < height):
        y1 += 1
        y2 -= 1

    return (x1, y1, x2, y2)





def aspectRatio(img:Image) -> int:
    width, height = img.size

    #divide by 0 catcher
    if width == 0 or height == 0:
        return 999

    return width / height

def isSingleColor(img:Image) -> bool:
    width, height = img.size
    check_color = img.getpixel((0,0))
    number_of_odd_pixels = 0

    for j in range(height):
        for i in range(width):
            if img.getpixel((i,j)) != check_color:
                number_of_odd_pixels += 1
                if(number_of_odd_pixels > 9):
                    return False
    else:
        return True

def cardTooSmall(img:Image) -> bool:
    width, height = img.size
    if width <= 10 or height <= 10:
        return True
    else:
        return False