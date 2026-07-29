import os
from PIL import Image, ImageEnhance
from math import floor

YELLOW = (255, 255, 0)
COLOR_BLACK = 0
COLOR_WHITE = 255


def normalize_card_images(directory_string:Image) -> Image:
    for g in range(len(os.listdir(directory_string))):
        img_str = str(os.listdir(directory_string)[g])
        img = Image.open(directory_string+img_str)
        final_img = _normalize_card_image(img)

def _normalize_card_image(img:Image) -> Image:
    color = ImageEnhance.Color(img)
    img2 = color.enhance(10)
    


    final_img = img2.crop(find_boarders_of_card(img2))

    #final_img = final_img.convert("1")

    return final_img

def find_boarders_of_card(img:Image) -> tuple[int, int, int, int]:
    width, height = img.size
    check_pixel_width_X = floor(width / 2)
    check_pixel_length_Y = floor(height / 2)

    #Finds the left edge of the card
    x1 = 1
    while(img.getpixel((x1,check_pixel_length_Y)) != YELLOW and x1 < width):
        #print(x1,':',img.getpixel((x1,check_pixel_length_Y)))
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
    while(img.getpixel((check_pixel_width_X,y2)) != YELLOW and y2 > 0):
        y2 -= 1

    return (x1, y1, x2, y2)

def _crop_out_card_symbol(img:Image) -> Image:
    #img.crop(localize_card_symbol(img)).show()
    img = img.crop(localize_card_symbol(img))
    #img.show()
    img = image_to_Black_and_White(img)
    #img.show()
    img = remove_yellow_border_from_image(img)
    img.crop(finalize_crop(img)).show()
    img = img.crop(finalize_crop(img))
    return img


def localize_card_symbol(img:Image) -> tuple[int, int, int, int]:
    enhancer = ImageEnhance.Brightness(img)
    img_copy = enhancer.enhance(10)

    _, height = img.size
    #fist pass
    crop_amount = (40, height - 70, 85, height - 28)
    
    return crop_amount
    
def finalize_crop(img:Image) -> tuple[int,int,int,int]:
    
    width, height = img.size
    left_border_found = False

    center = floor(width / 2)
    line = center

    left_crop = 0
    right_crop = width
    top_crop = 0

    #Find left boarder of symbol
    while(not left_border_found):
        odd_pixel_found = False
        top_pixel = img.getpixel((line,0))

        for i in range(height): #Checks in a line down the image
            if(top_pixel == COLOR_BLACK):
                if(img.getpixel((line,i))):
                    odd_pixel_found = True
            else:
                if(not img.getpixel((line,i))):
                    odd_pixel_found = True
            if(odd_pixel_found):
                line -= 1
                break
        else:
            left_crop = line
            print("Left crop found",':',left_crop)
            left_border_found = True
        if(line == 0):
            left_border_found = True

    #Finds right border of symbol
    right_border_found = False
    line = center
    while(not right_border_found):
        odd_pixel_found = False
        top_pixel = img.getpixel((line,0))

        for i in range(height): #Checks in a line down the image
            if(top_pixel == COLOR_BLACK):
                if(img.getpixel((line,i))):
                    odd_pixel_found = True
            else:
                if(not img.getpixel((line,i))):
                    odd_pixel_found = True
            if(odd_pixel_found):
                line += 1
                break
        else:
            right_crop = line
            right_border_found = True
            print("Right crop found",':',right_crop)
        if(line == width):
            right_border_found = True

    top_border_found = False
    line = center
    while(not top_border_found):
        odd_pixel_found = False
        left_pixel = img.getpixel((0,line))

        for i in range(width): #Checks in a line across the image
            if(left_pixel == COLOR_BLACK):
                if(img.getpixel((i,line))):
                    odd_pixel_found = True
            else:
                if(not img.getpixel((i,line))):
                    odd_pixel_found = True
            if(odd_pixel_found):
                line -= 1
                break
        else:
            top_crop = line
            top_border_found = True
            print("Right crop found",':',top_crop)   
        if(line == 0):
            top_border_found = True


    crop_amount = (left_crop, top_crop, right_crop, height)
    print(crop_amount)
    return crop_amount

def image_upscale(img:Image,amount:int) -> Image:
    width, height = img.size
    new_size = (width * amount, height * amount)
    img.resize(new_size, Image.Resampling.LANCZOS)

def image_to_Black_and_White(img:Image) -> Image:
    img_copy = img
    thresh = 140
    fn = lambda x: 255 if x > thresh else 0
    img_copy = img_copy.convert('L').point(fn,mode='1')
    #img_copy.show()
    return img_copy

def remove_yellow_border_from_image(img:Image) -> Image:
    width, height = img.size

    center = floor(height / 2)
    bottom_crop = height

    bottom_border_found = False
    line = center
    while(not bottom_border_found):
        odd_pixel_found = False
        top_pixel = img.getpixel((0,line))

        for i in range(width): #Checks in a line across the image
            if(top_pixel == COLOR_BLACK):
                if(img.getpixel((i,line))):
                    odd_pixel_found = True
            else:
                if(not img.getpixel((i,line))):
                    odd_pixel_found = True
            if(odd_pixel_found):
                line += 1
                break
        else:
            bottom_crop = line
            bottom_border_found = True
            print("Right crop found",':',bottom_crop)   
        if(line == height):
            bottom_border_found = True

    img_copy = img.crop((0,0,width,bottom_crop))

    return img_copy