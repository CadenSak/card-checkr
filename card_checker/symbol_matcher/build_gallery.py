from __future__ import annotations
import os as os
from pathlib import Path
from embeder import _feature_print

def build_gallery(symbol_dir: Path, out: Path):
    # symbol_dir/<set_code>.png  →  one clean reference per set
    gallery = {}
    for png in symbol_dir.glob("*.png"):
        fp = _feature_print(png)
        if fp is not None:
            gallery[png.stem] = fp  # serialize raw vector
    #out.write_bytes(pickle.dumps(gallery))
    return gallery
