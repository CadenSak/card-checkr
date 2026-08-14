from CardClass import Card
from enum import IntEnum
from CardScanner import CardScanner
from PIL import Image, ImageEnhance
from math import floor
import base_symbol_setup as bss

scanner = CardScanner


class Dire(IntEnum):
    """
        Enum for different scan directions
    """

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

class CardChecker:

    scanner = CardScanner()

    def _modified_card_img_to_black_white(self, card:Card) -> Image.Image:
        """
            sets image to pure black and white determined by thereshold
        """

        img_copy = card.get_modified_img()
        thresh = 140
        fn = lambda x: 255 if x > thresh else 0
        img_copy = img_copy.convert('L').point(fn,mode='1')
        #img_copy.show()
        return img_copy

    def _rotate_card_for_alignment(self, card:Card):
        """
            Rotates card to so bottom edge of the card is facing downwards
        """

        width, height = card.get_base_img().size
        check_pixel_width_X = floor(width / 2)
        check_pixel_length_Y = floor(height / 2)

        threshold = 75

        for i in range(40):
            img = card.get_base_img()

            x_left_pixel = img.getpixel((i,check_pixel_length_Y))
            y_top_pixel = img.getpixel((check_pixel_width_X,i))
            x_right_pixel = img.getpixel((width - (i + 1),check_pixel_length_Y))
            y_bottom_pixel = img.getpixel((check_pixel_width_X,height - (i + 1)))

            #print(f"DEBUG : Left pixel = {x_right_pixel}")
            #print(f"DEBUG : Right pixel = {x_right_pixel}")
            #print(f"DEBUG : Top pixel = {y_top_pixel}")

            if(bss.distance(x_left_pixel, (0,0,0)) < threshold):
                print("DEBUG : card rotated 90 degrees")
                print("DEBUG : Distance was",bss.distance(x_left_pixel,(0,0,0)))
                card.set_base_img(img.rotate(90,expand=True))
                break
            elif(bss.distance(y_top_pixel, (0,0,0)) < threshold):
                print("DEBUG : card rotated 180 degrees")
                card.set_base_img(img.rotate(180,expand=True))
                break
            elif(bss.distance(x_right_pixel, (0,0,0)) < threshold):
                print("DEBUG : card rotated 270 degrees")
                card.set_base_img(img.rotate(270,expand=True))
                break
            elif(bss.distance(y_bottom_pixel, (0,0,0))):
                print("DEBUG : card was not rotated")
                break
        else:
            print("DEBUG : card was not rotated")

    def _get_localized_symbol_crop(self, card:Card):
        """
            returns symbol crop area depending on age of card
        """


        img_copy = card.get_normal_img()
        width, height = img_copy.size

        #first pass
        if(card.get_is_old()):
            crop_amount = (width-49, height - 40, width, height)
        else:
            crop_amount = (5, height - 50, 55, height-5)

        return crop_amount

    def _remove_yellow_border_from_symbol(self, card:Card):
        """
            removes any yellow border from symbol as needed to get proper crop
        """

        img_copy = card.get_modified_img()

        width, _ = img_copy.size

        bottom_crop = CardScanner._find_border_of_symbol(card,Dire.BOTTOM)

        card.set_modified_img(img_copy.crop((0,0,width,bottom_crop)))

    def _find_border_color(self, card:Card):
        """
            finds border color of current card
        """
        self.scanner._line_scan_across_img_for_border_color(card, Dire.TOP)
        self.scanner._line_scan_across_img_for_border_color(card, Dire.LEFT)

    def _find_card_picture_cords(self, card:Card) -> tuple[int,int,int,int]:
        """
            finds interior of card; must have used _find_border_color and bss.find_borders_of_card
        """


        """x1 = self.scanner._line_scan_across_img_for_card_picture(card, Dire.LEFT)
        y1 = self.scanner._line_scan_across_img_for_card_picture(card, Dire.TOP)
        x2 = self.scanner._line_scan_across_img_for_card_picture(card, Dire.RIGHT)
        y2 = self.scanner._line_scan_across_img_for_card_picture(card, Dire.BOTTOM)"""
        x1, y1, x2, y2 = bss.find_borders_of_card_picture(card.get_normal_img(),card.get_border_color_x(),card.get_border_color_y())
        return (x1, y1, x2, y2)

    def _find_borders_of_symbol(self, card:Card) -> tuple[int,int,int,int]:
        """
            determins area that card symbol takes up in modified image
        """

        x1 = self.scanner._find_border_of_symbol(card, "left")
        y1 = self.scanner._find_border_of_symbol(card, "top")
        x2 = self.scanner._find_border_of_symbol(card, "right")
        y2 = self.scanner._find_border_of_symbol(card, "bottom")

        return (x1, y1, x2, y2)
    

    def normalize(self, card:Card):
        """
            normalization pipeline for card
        """

        self._rotate_card_for_alignment(card)
        color = ImageEnhance.Color(card.get_base_img())
        img_copy = color.enhance(10)
        card.set_normal_img(img_copy)
        #img_copy.show()

        self._find_border_color(card)
        try:
            card.set_normal_img(img_copy.crop(bss.find_borders_of_card(img_copy, card.get_border_color_x(), card.get_border_color_y())))
        except Exception as e:
            card.set_normal_img(img_copy)
            print(e)
        #self.__img_modified = self.__img_modified.crop(self._find_crop())
        
    def crop_card_picture(self, card:Card):
        """
            finds and crops to interior of card as part of normalization
        """
        img_copy = card.get_normal_img()
        crop_amount = self._find_card_picture_cords(card)
        img_copy = img_copy.crop(crop_amount)
        card.set_normal_img(img_copy)
        card.set_modified_img(img_copy)

    def find_symbol_on_card(self, card:Card):
        """
            Finds and crops to symbol within normalized card
        """
        card.set_modified_img(card.get_normal_img().crop(self._get_localized_symbol_crop(card)))

        card.set_modified_img(self._modified_card_img_to_black_white(card))

        card.set_modified_img(card.get_modified_img().crop(self._find_borders_of_symbol(card)))

        card._symbol_save()

    def get_card_set(self, img_path_as_str:str, gallery:list[dict]) -> tuple[str,float]:
        """
            default card pipe line
        """

        card = Card(img_path_as_str)
        self.normalize(card)
        self.crop_card_picture(card)
        self.find_symbol_on_card(card)
        card.set_modified_img(card.get_modified_img().crop(self._find_borders_of_symbol(card)))
        card._check_if_old(gallery[0])
        if(card.get_is_old()):
            self.find_symbol_on_card(card)
            card.identify_set(gallery[1])
        else:
            card.identify_set(gallery[0])

        _id = card.get_ID()
        print("DEBUG : symbol found",_id["set"],"distance is",_id["distance"])
        return (_id["set"],_id["distance"])
        