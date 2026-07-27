from __future__ import annotations
from pathlib import Path
import Quartz, Vision
from Foundation import NSData

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
    ok, dist, _ = b.computeDistanceToObservation_error_(a, None)   # returns float; smaller = more similar
    return float(dist) if ok else float("inf")

res = _feature_print("/Users/cadensak/Desktop/cropped/cel25.png_final.png")
print(res.data())