from CardClass import Card
from enum import IntEnum
from math import floor
import base_symbol_setup as bss


class Dire(IntEnum):
    """
        Enum for different scan directions
    """

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

class Scan_Type(IntEnum):
    """
        Enum for different scan types
    """
    FIND_BORDER_COLOR = 0
    FIND_CARD_BORDER = 1
    FIND_CARD_PICTURE = 2
    FIND_BORDER_OF_SYMBOL = 3



CC = {
    "YELLOW":(255,255,0),
    "CYAN":(0,255,255),
    "BLUE":(0,0,255),
    #"GREY":(127,127,127)
    }


class CardScanner:
    def _setup_scan(self, card:Card, direction:int, type:int):
        """
            sets nessesary variables for scans to work
        """


        if(direction > 3):
            raise ValueError("Direction not supported, Direction must be left, right, top, or bottom")

        if(type > 5):
            raise ValueError("Type not supported")
        

        if(type == Scan_Type.FIND_BORDER_COLOR or type == Scan_Type.FIND_CARD_PICTURE):
            img_copy = card.get_normal_img()
        elif(type == Scan_Type.FIND_CARD_BORDER):
            img_copy = card.get_modified_img()
        elif(type == Scan_Type.FIND_BORDER_OF_SYMBOL):
            img_copy = card.get_modified_img()

        width, height = img_copy.size

        #Sets the check pixel length to correct value depending of scan type and card age
        if(type == Scan_Type.FIND_BORDER_OF_SYMBOL):
            check_pixel_length_Y = floor(height / 2)
            check_pixel_length_X = floor(width / 2)
        else:
            check_pixel_length_Y = floor(5 * height / 6)
            if(card.get_is_old()):
                check_pixel_length_X = floor(3 * width / 4)
            else:
                check_pixel_length_X = floor(width / 4)


        match(direction):
            case Dire.LEFT:

                self._check_pixel = check_pixel_length_Y
                self._check_color = card.get_border_color_y()
                self._stop_at = width - 1
                self._movement = 1
                self._Left_Top = True

            case Dire.RIGHT:

                self._check_pixel = check_pixel_length_Y
                self._check_color = card.get_border_color_y()
                self._stop_at = 1
                self._movement = -1
                self._Left_Top = False

            case Dire.TOP:

                self._check_pixel = check_pixel_length_X
                self._check_color = card.get_border_color_x()
                self._stop_at = height - 1
                self._movement = 1
                self._Left_Top = True

            case Dire.BOTTOM:

                self._check_pixel = check_pixel_length_X
                self._check_color = card.get_border_color_x()
                self._stop_at = 1
                self._movement = -1
                self._Left_Top = False
        return

    def _line_scan_across_img_for_border_color(self, card:Card, direction:int):
        """
            scans across img in a set line to determine border color of card
        """


        Threshold = 30 #Changes how sensitive the range for determining border color is

        self._setup_scan(card, direction, Scan_Type.FIND_BORDER_COLOR)

        img_copy = card.get_normal_img()
        crount = 0
        color_found = False
        if(direction == Dire.LEFT or direction == Dire.TOP):
            i = 0
        elif(direction == Dire.RIGHT):
            i = img_copy.width - 1
        else:
            i = img_copy.height - 1

        while(not color_found and(
            (i < self._stop_at and self._Left_Top) or
            (i > self._stop_at and not self._Left_Top)
            )):
            if(direction == Dire.LEFT or direction == Dire.RIGHT):
                pixel_color = img_copy.getpixel((i,self._check_pixel))
            else:
                pixel_color = img_copy.getpixel((self._check_pixel,i))

            color, d = bss.find_border_color(pixel_color, CC)

            #print(f"DEBUG : distance to color {color} is = {d}")

            if(d < Threshold):
                if(not color_found):
                    crount += 1
                    i += self._movement
                    if(crount > 3):
                        print(f"Found border color it's {color}")
                        color_found = True
            else:
                crount = 0
                i += self._movement

        if(direction == Dire.LEFT or direction == Dire.RIGHT):
            card.set_border_color_Y(color)
        else:
            card.set_border_color_X(color)
            
        return

    def _line_scan_across_img_for_card_picture(self, card:Card, direction:int) -> int:
        """
            Scans across image to find inner edge of card border to denote interior of card
            \nPre: To run this border color of card must be found first and card must be cropped to exterior border
        """

        Threshold = 30 # Changes how sensitive the range for determining border color is

        xy = 0

        img_copy = card.get_normal_img()

        self._setup_scan(card, direction, Scan_Type.FIND_CARD_PICTURE)

        if(direction == Dire.LEFT or direction == Dire.TOP):
            i = 0
        elif(direction == Dire.RIGHT):
            i = img_copy.width - 1
        else:
            i = img_copy.height - 1

        picture_found = False
        crount = 0
        count = 0

        for i in range(40):
            if(direction == Dire.LEFT or direction == Dire.TOP):
                xy = i
            elif(direction == Dire.RIGHT):
                xy = img_copy.width - i - 1
            else:
                xy = img_copy.height - i - 1
            if(direction == Dire.LEFT or direction == Dire.RIGHT):
                pixel_color = img_copy.getpixel((xy,self._check_pixel))
            else:
                pixel_color = img_copy.getpixel((self._check_pixel,xy))

            d = bss.distance(pixel_color, CC[self._check_color])
            if(d > Threshold):
                break
            else:
                crount = 0
        else:
            print("DEBUG : Returning 27 from edge")
            if(direction == Dire.LEFT or direction == Dire.TOP):
                return 27
            elif(direction == Dire.RIGHT):
                return img_copy.width - 27
            else:
                return img_copy.height - 27
            
        return xy # Returns x / y value of interior picture

    def _line_scan_across_img_for_card_border(self, card:Card, direction:int) -> int:
        """
            Scans in a set line across card to locate outer edge of card
        """

        Threshold = 30 # Changes how sensitive the range for determining border color is
    
        img_copy = card.get_modified_img()

        self._setup_scan(card,direction,Scan_Type.FIND_CARD_BORDER)

        if(direction == Dire.LEFT or direction == Dire.TOP):
            i = 0
        elif(direction == Dire.RIGHT):
            i = img_copy.width
        else:
            i = img_copy.height

        border_found = False

        while(not border_found and(
            (i < self._stop_at and self._Left_Top) or
            (i > self._stop_at and not self._Left_Top)
            )):

            if(direction == Dire.LEFT or direction == Dire.RIGHT):
                pixel_color = img_copy.getpixel((i,self._check_pixel))
            else:
                pixel_color = img_copy.getpixel((self._check_pixel,i))

            d = bss.distance(pixel_color, self._check_color)

            if(d < Threshold):
                border_found = True
            else:
                i += self._movement

        return i # Returns x / y value of interior picture

    def _find_border_of_symbol(self, card:Card, side:str) -> int:
        """
            Finds the edges of symbol in cropped out area by searching in lines across the image until
            4 lines of solid color apear in a row
        """

        """
            Direction
            0 = LEFT
            1 = UP
            2 = RIGHT
            3 = DOWN
        """
        allowed_sides = ["left", "right", "top", "bottom"]
        if(side not in allowed_sides):
            raise ValueError("Not an allowed direction")

        img = card.get_modified_img()

        width, height = card.get_modified_img().size

        border_found = False
        crop = None
        crount = 0

        #Movement direction is direction the pixel check moves relative to image
        if(side == "left" or side == "right"):
            movement_direction = "up/down"
            line_length = height #length of the line
            line = floor(width / 2) # Line Start Positiion
        else:#side == "top" or side == "bottom"
            movement_direction = "left/right"
            line_length = width #length of the line
            line = floor(height / 2) # Line Start Positiion

        #What number should the algorith stop at if no border is found
        if(side == "left" or side == "top"):
            stop_number = 0 #position line should stop moving at
            move_line = -1 #direction line moves
        elif(side == "right"):
            stop_number = width #position line should stop moving at
            move_line = 1 #direction line moves
        else:
            line = floor(2 * height / 3)
            stop_number = height #position line should stop moving at
            move_line = 1 #direction line moves

        while(not border_found):
            odd_pixel_found = False
            if(movement_direction == "up/down"):
                xy = (line, 0)
            else:
                xy = (0, line)

            first_pixel = img.getpixel((xy))

            for i in range(line_length): #Checks in a line across the image
                if(movement_direction == "up/down"):
                    xy = (line, i)
                else:
                    xy = (i, line)
                
                test_pixel = img.getpixel(xy)

                if(test_pixel != first_pixel):
                    odd_pixel_found = True
                    crount = 0

                if(odd_pixel_found):
                    line += move_line
                    break

            else:
                crount += 1
                line += move_line
                if(
                    (crount == 5 and side == "bottom") or
                    (crount == 5 and side != "bottom")):

                    if(side == "right" or side == "bottom"):
                        crop = line - 1
                    else:
                        crop = line + 1

                    border_found = True

                    """match (direction):
                        case 0:
                            print("left", end="")
                        case 1:
                            print("top", end="")
                        case 2:
                            print("right", end="")
                        case 3:
                            print("bottom", end="")
                    print(f"_crop found : {crop}")"""

            if(line == stop_number):
                border_found = True

        return stop_number if crop is None else crop