import build_gallery
from CNNcardquery import identify_set
from pathlib import Path
import CNNcardquery
from base_symbol_setup import _normalize_card_image, _crop_out_card_symbol, image_upscale
from PIL import Image
import os

dir = "/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards/"

img = Image.open("/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards/Test2.jpg")

for g in range(
    len(os.listdir(dir))
    ):
    img_str = str(os.listdir(dir)[g])
    if(img_str[-4:] == '.jpg'):
        img = Image.open(dir+img_str)
        img = _normalize_card_image(img)
        img = _crop_out_card_symbol(img)
        img = image_upscale(img, 4)

"""#img = Image.open(img)
img = _normalize_card_image(img)
img = _crop_out_card_symbol(img)
img = image_upscale(img, 4)"""