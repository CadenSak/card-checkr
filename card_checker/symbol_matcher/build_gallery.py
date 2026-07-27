from __future__ import annotations
import os as os
import pickle
from pathlib import Path
from PIL import Image
import Quartz, Vision
from Foundation import NSData

CROP_DIR = "/Users/cadensak/Desktop/CROP_DIR/"


def build_gallery(symbol_dir: Path, out: Path):
    # symbol_dir/<set_code>.png  →  one clean reference per set
    gallery = {}
    for png in symbol_dir.glob("*.png"):
        fp = _feature_print(png)
        if fp is not None:
            gallery[png.stem] = fp  # serialize raw vector
    #out.write_bytes(pickle.dumps(gallery))
    return gallery
    
def _feature_print(image_path: Path) -> "Vision.VNFeaturePrintObservation | None":
    data = NSData.dataWithContentsOfFile_(str(image_path))
    src = Quartz.CGImageSourceCreateWithData(data, None)
    if src is None:
        return None
    cg = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)
    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cg, None)
    req = Vision.VNGenerateImageFeaturePrintRequest.alloc().init()
    # Optional: req.setImageCropAndScaleOption_(Vision.VNImageCropAndScaleOptionScaleFill)
    ok, _ = handler.performRequests_error_([req], None)
    results = req.results()
    return results[0] if ok and results else None

def distance(a, b) -> float:
    dist = b.computeDistanceToFeaturePrintObservation_error_(a, None)   # returns float; smaller = more similar
    return float(dist)

def identify_set(card_crop: Path, gallery, k: int = 3, threshold: float = 20.0):
    q = _feature_print(card_crop)
    if q is None:
        return None
    scored = sorted(((name, distance(q, ref)) for name, ref in gallery.items()),
                    key=lambda x: x[1])
    best_name, best_dist = scored[0]
    if best_dist > threshold:          # open-set rejection: not confidently any known set
        return None
    return {"set": best_name, "distance": best_dist, "top_k": scored[:k]}

def normalize_card_images(directory_string):
    for g in range(
    len(os.listdir(directory_string))
    ):
        img_str = str(os.listdir(directory_string)[g])
        img = Image.open(directory_string+img_str)

        width, height = img.size
        crop_width_percentage = 0.14
        crop_height_percentage = 0.09

        CROP_AMOUNT = (60,int(height - height * crop_height_percentage),110,int(height-30))

        final_img = img.crop(CROP_AMOUNT)

        final_img = final_img.convert("L")
        
        final_img.save(CROP_DIR+img_str[:-4]+"_edited.png")

dir = Path("/Users/cadensak/Desktop/pokemon")
directory_string = "/Users/cadensak/Desktop/CC14-1_lp/"
out = "/Users/cadensak/Desktop/out.pkl"

gallery = build_gallery(dir, out)
"""data = out.read_bytes()
gallery = pickle.loads(data)"""

normalize_card_images(directory_string)

with open("/Users/cadensak/Desktop/cards.txt", 'w') as outfile:
    for g in range(
    len(os.listdir(CROP_DIR))
    ):
        img_str = str(os.listdir(CROP_DIR)[g])
        img = Path(CROP_DIR + img_str)
        identification = identify_set(img, gallery)
        print(identify_set(img, gallery))
        outfile.write(img_str + " = " + identification["set"] + '\n')