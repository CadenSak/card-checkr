import os
from PIL import Image, ImageEnhance
from math import floor, sqrt

YELLOW = (255, 255, 0)
COLOR_BLACK = 0
COLOR_WHITE = 255

CONSTANT_COLORS = {"YELLOW":(255,255,0),"CYAN":(0,255,255),"BLUE":(0,50,255)}

def find_borders_of_card(img:Image, color_x:str, color_y:str) -> tuple[int, int, int, int]:
    width, height = img.size
    Threshold = 30
    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(height / 2)
    check_color = CONSTANT_COLORS[color_x]
    #Finds the left edge of the card
    x1 = 1
    x2 = width - 1
    y1 = 1
    y2 = height - 1
    #print("x1 :")
    while(distance(img.getpixel((x1,check_pixel_length_Y)), check_color) > Threshold and x1 < width - 1):
        x1 += 1
        #if x1 < 100:
            #print(img.getpixel((x1,check_pixel_length_Y)))

    while(distance(img.getpixel((x2,check_pixel_length_Y)), check_color) > Threshold and x2 > 1):
        x2 -= 1

    check_color = CONSTANT_COLORS[color_y]
    #print("y1 :")
    while((distance(img.getpixel((check_pixel_width_X,y1)), check_color) > Threshold and y1 < height - 1)):
        y1 += 1
        #if y1 < 100:
           # print(img.getpixel((check_pixel_width_X,y1)))

    while(distance(img.getpixel((check_pixel_width_X,y2)), check_color) > Threshold and y2 > 1):
        y2 -= 1

    return (x1, y1, x2, y2)

def find_borders_of_card_picture(img:Image, color_x:str, color_y:str) -> tuple[int,int,int,int]:
    width, height = img.size
    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(5 * height / 6)
    check_color_x = CONSTANT_COLORS[color_x]
    check_color_y = CONSTANT_COLORS[color_y]
    if(color_x == "YELLOW"):
        check_pixel_width_X = floor(width / 8)
        check_pixel_length_Y = floor(5 * height / 6)
    threshold = 50
    crount_amount = 3

    x1_crount = 0
    x2_crount = 0

    y1_crount = 0
    y2_crount = 0

    x1 = 1
    left_break = False
    x2 = width - 1
    right_break = False
    y1 = 1
    top_break = False
    y2 = height - 1
    bottom_break = False

    for i in range(50):
        x1_color = img.getpixel((x1,check_pixel_length_Y))
        if(distance(x1_color, check_color_x) < threshold and not left_break):
            x1 += 1
            x1_crount = 0
        elif(y2_crount < crount_amount):
            x1 += 1
            x1_crount += 1
        else:
            if(not left_break):
                print(f"DEBUG : Distance to x1 color = {distance(x1_color, check_color_x)}")
                print(f"DEBUG : Found picture left edge : x1 = {x1} : color = {x1_color}")
            left_break = True


        x2_color = img.getpixel((x2,check_pixel_length_Y))
        if(distance(x2_color, check_color_x) < threshold and not right_break):
            x2 -= 1
            x2_crount = 0
        elif(y2_crount < crount_amount):
            x2 -= 1
            x2_crount += 1
        else:
            if(not right_break):
                print(f"DEBUG : Distance to x2 color = {distance(x2_color, check_color_x)}")
                print(f"DEBUG : Found picture right edge : x2 = {x2} : color = {x2_color}")
                crount = 0
            right_break = True


        y1_color = img.getpixel((check_pixel_width_X,y1))
        if(distance(y1_color, check_color_y) < threshold and not top_break):
            y1 += 1
            y1_crount = 0
        elif(y2_crount < crount_amount):
            y1 += 1
            y1_crount += 1
        else:
            if(not top_break):
                print(f"DEBUG : Distance to y1 color = {distance(y1_color, check_color_y)}")
                print(f"DEBUG : Found picture top edge : y1 = {y1} : color = {y1_color}")
                crount = 0
            top_break = True


        y2_color = img.getpixel((check_pixel_width_X,y2))
        if(distance(y2_color, check_color_y) < threshold and not bottom_break):
            y2 -= 1
            y2_crount = 0
        elif(y2_crount < crount_amount):
            y2 -= 1
            y2_crount += 1
        else:
            if(not bottom_break):
                print(f"DEBUG : Distance to y2 color = {distance(y2_color, check_color_y)}")
                print(f"DEBUG : Found picture bottom edge : y2 = {y2} : color = {y2_color}")
                crount = 0
            bottom_break = True

        if(left_break and right_break and top_break and bottom_break):
            break

    else:
        print("Card might be yellow type : defaulting to norm 27 all sides")
        x1 = 27
        y1 = 27
        x2 = width - 27
        y2 = height - 27

    return (x1,y1,x2,y2)



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

def distance(a:tuple[int,...],b:tuple[int,...]) -> int:
    """
        Finds distance between to equal length vector
    """
    if(len(a) != len(b)):
        raise ValueError("length of a and b vectors are not equal")

    total_sum = 0
    for i in range(len(a)):
        diff = a[i] - b[i]
        total_sum += pow(diff,2)
    final = sqrt(total_sum)
    return final

def find_border_color(a:tuple[int,...],b:dict):
    for k, v in b.items():
        d = distance(a,v)
        if(d < 30):
            return k, d
    else:
        return "YELLOW", 255
