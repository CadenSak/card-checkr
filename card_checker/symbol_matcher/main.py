import build_gallery
from CNNcardquery import identify_set
from pathlib import Path
import CNNcardquery
from base_symbol_setup import _normalize_card_image, _crop_out_card_symbol
from PIL import Image

path = Path("/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards")
img = Image.open("/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards/Test1.jpg")

img = _normalize_card_image(img)
img = _crop_out_card_symbol(img)
