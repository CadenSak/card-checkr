from PIL import Image, ImageEnhance
from pathlib import Path
from math import floor
from enum import IntEnum
import base_symbol_setup as bss
import CNNcardquery as CNN

cache = "git@github.com:CadenSak/cache/"

CONSTANT_COLORS = {
    "YELLOW":(255,255,0),
    "CYAN":(0,255,255),
    "BLUE":(0,0,255),
    #"GREY":(127,127,127)
    }

class Card:
    _x:int
    """
    Variables of Card class
    
    __img_base:Image
    _path:Path
    
    __img_modified:Image

    __border_color_x:str
    __border_color_y:str

    __img_modified_width:int
    __img_modified_height:int

    _cache_Image:Image
    _cache_Path:Path

    __id:dict

    __img_str:str
    __card_id_number:int

    _is_old:bool
    """

    _Master_Card_list = []
    """STATIC"""

    """ PRIVATE API"""

    def __init__(self, path:str):
        """ Init card object """

        self._img_base=Image.open(path)
        self._img_normal:Image.Image|None = None
        self._img_modified:Image.Image|None = None

        self._symbol_img:Image.Image|None = None

        self._path = Path(path)
        self._cache_Path:Path|str|None

        self._is_old:bool = False

        self.__img_str:str = str(self._path)[-17:]
        #print("----->",self.__img_str)

        self.__card_id_number:int = int(self.__img_str[9:12])
        #print("----->",self.__card_id_number)

        self._border_color_x = "temp"
        self._border_color_y = "temp"

        print("DEBUG : Now processing card :",self.__card_id_number)

    def _symbol_save(self):
        """ Caches symbol to be used for identification """

        self._cache_Path = cache+"cache_"+self.__img_str[:-4]+".png"
        self._cache_Image = self._img_modified
        try:
            self._img_modified.save(self._cache_Path,"PNG")
            self._cache_Path = Path(self._cache_Path)
        except Exception as e:
            print(e)

    def _check_if_old(self, gallery:dict):
        """ 
            Makes best guess at age of symbol using aspect ratio size of symbol color of symbol
            and by checking against list of known symbols
        """



        i = CNN.identify_set(self._cache_Path, gallery)

        threshold = 0.60

        if i is not None:
            d = i["distance"]
            print(f"{self.__card_id_number}: dist={d}")
        else:
            print(f"{self.__card_id_number}: dist=unknown")

        if(bss.aspectRatio(self._cache_Image) > 2):
            print("Card",self.__card_id_number,"is old! Becuase aspect ratio greater than 2")
            self._is_old = True
        elif(bss.cardTooSmall(self._cache_Image)):
            print("Card",self.__card_id_number,"is old! Becuase card is too small")
            self._is_old = True
        elif(bss.isSingleColor(self._cache_Image)):
            print("Card",self.__card_id_number,"is old! Becuase card is a single color")
            self._is_old = True
        elif(d > threshold):
            print("Card",self.__card_id_number,"is old! Because it doesn't seem to contain a symbol")
            self._is_old = True
        else:
            print("Card",self.__card_id_number,"is not old!")
            self._is_old = False
    
    """ PUBLIC API """

    def identify_set(self, gallery):
        """ Identifies set of card using the cached image path and the premade gallery """
        self._id = CNN.identify_set(self._cache_Path, gallery)

    def show(self):
        """ Shows card using PILLOW built in show function"""
        self._img_modified.show()

    # Getter Function

    def get_base_img(self):
        return self._img_base

    def get_normal_img(self):
        return self._img_normal

    def get_modified_img(self):
        return self._img_modified

    def get_border_color_y(self):
        return self._border_color_y

    def get_border_color_x(self):
        return self._border_color_x

    def get_path(self):
        return self._path

    def get_cache_path(self):
        return self._cache_Path

    def get_is_old(self):
        return self._is_old

    def get_ID(self):
        return self._id
    
    # Setter Funcitons

    def set_base_img(self, new_img_base:Image.Image):
        self._img_base = new_img_base

    def set_normal_img(self, new_img_norm:Image.Image):
        self._img_normal = new_img_norm

    def set_modified_img(self, new_img_modified:Image.Image):
        self._img_modified = new_img_modified

    def set_border_color_Y(self, color:str):
        self._border_color_y = color

    def set_border_color_X(self, color:str):
        self._border_color_x = color
