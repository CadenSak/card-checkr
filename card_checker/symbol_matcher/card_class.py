from PIL import Image, ImageEnhance
from pathlib import Path
from math import floor
import base_symbol_setup as bss
import CNNcardquery as CNN

cache = "git@github.com:CadenSak/cache/"


CONSTANT_COLORS = {"YELLOW":(255,255,0),"CYAN":(0,255,255),"BLUE":(0,50,255)}




class Card:
    """ PRIVATE VARIABLES"""
    __img_base:Image
    _path:Path
    
    __img_modified:Image
    __border_color:str

    __img_modified_width:int
    __img_modified_height:int

    _cache_Image:Image
    _cache_Path:Path

    __id:dict

    __img_str:str
    __card_id_number:int

    __is_old:bool

    __Master_Card_list = []
    """STATIC"""

    """ PRIVATE API"""

    def __init__(self, path:str):
        self.__img_base=Image.open(path)
        self._path = Path(path)
        self.__is_old = False

        self.__img_str = str(self._path)[-17:]
        #print("----->",self.__img_str)
        self.__card_id_number = int(self.__img_str[9:12])
        #print("----->",self.__card_id_number)

    def _localize_symbol(self):
        width = self.__img_modified_width
        height = self.__img_modified_height
        img_copy = self.__img_modified

        #first pass
        if(self.__is_old):
             crop_amount = (width-75, height - 70, width-30, height - 18)
        else:
             crop_amount = (40, height - 70, 85, height - 28)

        self.__img_modified = img_copy.crop(crop_amount)
        #self.__img_modified.show()

        self._set_new_img_size()

    def _set_new_img_size(self):
        self.__img_modified_width, self.__img_modified_height = self.__img_modified.size

    def _img_to_black_white(self):
        img_copy = self.__img_modified
        thresh = 140
        fn = lambda x: 255 if x > thresh else 0
        img_copy = img_copy.convert('L').point(fn,mode='1')
        #img_copy.show()

        self.__img_modified = img_copy
        self._set_new_img_size()

    def _symbol_crop(self):
        img_copy = self.__img_modified
    
        #Find borders of symbol
        crop = self._find_crop()

        crop_amount = (crop[0], crop[1], crop[2], self.__img_modified_height)
        self.__img_modified = img_copy.crop(crop_amount)
        print(crop_amount)

    def _find_border_of_symbol(self, side:str) -> int:
        """
            Direction
            0 = LEFT
            1 = UP
            2 = RIGHT
            3 = DOWN
        """
        allowed_sides = ["left", "right", "top", "bottom"]
        if(side not in allowed_sides):
            return 0

        img = self.__img_modified

        width, height = self.__img_modified.size

        border_found = False
        crop = None
        crount = 0

        #Movement direction is direction the pixel check moves relative to image
        if(side == "left" or side == "right"):
            movement_direction = "up/down"
            line_length = height #length of the line
            line = floor(width / 2) # Line Start Positiion
        else:#side == "top" or side == "bottom"
            line = floor(height / 2)
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
                    (crount == 1 and side == "bottom") or
                    crount == 4):

                    if(side == "right" or side == "bottom"):
                        crop = line - 3
                    else:
                        crop = line + 3

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

    def _find_crop(self) -> tuple[int,int,int,int]:
        right_crop = self._find_border_of_symbol("right")
        left_crop = self._find_border_of_symbol("left")
        top_crop = self._find_border_of_symbol("top")
        bottom_crop = self._find_border_of_symbol("bottom")

        return (left_crop, top_crop, right_crop, bottom_crop)
    
    def size(self):
        return self.__img_modified_width, self.__img_modified_height

    def _symbol_save(self):
        self._cache_Path = cache+"cache_"+self.__img_str[:-4]+".png"
        self._cache_Image = self.__img_modified
        try:
            self.__img_modified.save(self._cache_Path,"PNG")
        except Exception as e:
            print(e)

    def _check_if_old(self, gallery):
        i = CNN.identify_set(self._cache_Path, gallery)
        if i is not None:
            d = i["distance"]
            print(f"{self.__card_id_number}: dist={d}")
        else:
            print(f"{self.__card_id_number}: dist=unknown")

        if(
            bss.aspectRatio(self._cache_Image) > 2 or
            bss.cardTooSmall(self._cache_Image) or
            bss.isSingleColor(self._cache_Image)
        ):
            print("Card",self.__card_id_number,"is old!")
            self.__is_old = True
        elif(d > 0.70):
            self.__is_old = True
        else:
            False

    def _remove_yellow_border_from_symbol(self):
        img_copy = self.__img_modified

        bottom_crop = self._find_border_of_symbol("bottom")

        self.__img_modified = img_copy.crop((0,0,self.__img_modified_width,bottom_crop))

        self._set_new_img_size()

    def _find_border_color(self):
        Threshold = 30
        color = ImageEnhance.Color(self.__img_base)
        img_copy = color.enhance(10)
        width, height = img_copy.size
        check_pixel_width_X = floor(width / 2)
        check_pixel_length_Y = floor(height / 2)
        x = 1
        y = 1
        color_found = False

        while(not color_found and x < width - 1):
            pixel_color = img_copy.getpixel((x,check_pixel_length_Y))
            color , d = bss.find_border_color(pixel_color, CONSTANT_COLORS)
            if(d < Threshold):
                print(f"Found border color it's {color}")
                self.__border_color = color
            else:
                x += 1
            


    
    """ PUBLIC API """

    def normalize(self):
        color = ImageEnhance.Color(self.__img_base)
        img_copy = color.enhance(10)
        img_copy.show()
        self.__img_modified = img_copy.crop(bss.find_borders_of_card(img_copy))
        #self.__img_modified = self.__img_modified.crop(self._find_crop())
        self._set_new_img_size()

    def identify_set(self, gallery):
        self.__id = CNN.identify_set(self._cache_Path, gallery)
        self.__Master_Card_list += [[self.__card_id_number,self.__id]]
        self.__Master_Card_list = sorted(self.__Master_Card_list,key=lambda x: x[0])

    def get_card_list(self):
        return self.__Master_Card_list

    def find_symbol(self, gallery):

        self._localize_symbol()
        self._img_to_black_white()
        self._remove_yellow_border_from_symbol()
        self._symbol_crop()
        self._symbol_crop()
        self._symbol_save()
        self._check_if_old(gallery)

        if(self.__is_old):
            self.normalize()
            self._localize_symbol()
            self._img_to_black_white()
            self._remove_yellow_border_from_symbol()
            self._symbol_crop()
            self._symbol_save()

    def show(self):
        self.__img_modified.show()

    def remove_yellow_border(self):
        img_copy = self.__img_modified
        self.__img_modified = img_copy.crop(bss.find_borders_of_card_picture(img_copy))
        self._set_new_img_size()