import build_gallery
from pathlib import Path
import os, shutil
from CardClass import Card
import CardChecker

def clear_cache():
    folder = cache
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Cleared Cache")

dir = "/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards/"

cache = "git@github.com:CadenSak/cache/"

gallery_pictures = Path("git@github.com:CadenSak/card-checkr.git/set_symbols/pokemon/")
out = Path("git@github.com:CadenSak/card-checkr.git/set_symbols/out.sym")
gallery = build_gallery.build_gallery(gallery_pictures,out)
mod = CardChecker.CardChecker()


#print(gallery)
#img = Image.open("/Users/cadensak/card-checkr/git@github.com:CadenSak/Testing_cards/Test2.jpg")

card = None

for g in range(
    len(os.listdir(dir))
    ):
    img_str = str(os.listdir(dir)[g])
    if(img_str[-4:] == '.jpg'): 

        mod.get_card_set(dir+img_str, gallery)

        
with open("git@github.com:CadenSak/Testing_cards/identification.txt","w") as outfile:
    card_list = card.get_card_list()
    for card in range(len(card_list)):
        if(not (card_list[card][1] is None)):
            outfile.write(f"{card_list[card][0]}: {card_list[card][1]["set"]} : {card_list[card][1]["distance"]}\n")
        else:
            outfile.write(f"{card_list[card][0]}: unknown\n")