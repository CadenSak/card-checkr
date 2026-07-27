from pathlib import Path
import embeder

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