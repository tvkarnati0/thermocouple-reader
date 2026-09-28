"""
read_display.py  -  read a 7-segment temperature display from a saved crop.

Usage:   python read_display.py Box1.png
Output:  prints the value, and saves debug_overlay.png so you can SEE
         which regions are being checked (use it to tune the numbers below).
"""
import sys
import cv2
import numpy as np

# ------------------------------------------------------------------
# SETTINGS  (all x, y numbers are pixels inside the CROP, not the video frame)
# ------------------------------------------------------------------
SLANT = 0.12            # how far the display leans right at the top (0 = upright)
DECIMALS = 1            # digits after the decimal point (2.1 -> 1)
LIT_THRESHOLD = 0.45    # a segment counts as "on" if this fraction of it is dark

MINUS_BOX = (6, 74, 34, 12)          # (x, y, w, h) sitting INSIDE the "-" sign at far left

# one (x, y, w, h) box per digit position, left to right, in DESKEWED coordinates
DIGIT_BOXES = [
    (189, 31, 56, 112),
    (256, 31, 56, 112),
]

# Each segment is a rectangle inside a digit box, as fractions (x0, x1, y0, y1)
SEGMENTS = {
    "a": (0.25, 0.75, 0.02, 0.14),
    "b": (0.78, 0.98, 0.16, 0.44),
    "c": (0.78, 0.98, 0.56, 0.84),
    "d": (0.25, 0.75, 0.86, 0.98),
    "e": (0.02, 0.22, 0.56, 0.84),
    "f": (0.02, 0.22, 0.16, 0.44),
    "g": (0.25, 0.75, 0.43, 0.57),
}

# which segments are lit for each digit
PATTERNS = {
    "abcdef": "0", "bc": "1", "abged": "2", "abgcd": "3", "fgbc": "4",
    "afgcd": "5", "afgedc": "6", "abc": "7", "abcdefg": "8", "abcdfg": "9",
}
PATTERNS = {frozenset(k): v for k, v in PATTERNS.items()}


# ------------------------------------------------------------------
def get_ink(crop):
    """Return image where digit pixels = 255 and everything else = 0."""
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) if crop.ndim == 3 else crop
    _, ink = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return ink


def deskew(ink):
    """Shear the image so the leaning digits stand upright."""
    h, w = ink.shape
    y0 = h / 2
    M = np.float32([[1, SLANT, -SLANT * y0], [0, 1, 0]])
    return cv2.warpAffine(ink, M, (w, h), flags=cv2.INTER_LINEAR)


def fraction_on(ink, x0, y0, x1, y1):
    region = ink[int(y0):int(y1), int(x0):int(x1)]
    return 0.0 if region.size == 0 else region.mean() / 255


def read_digit(upright, box):
    x, y, w, h = box
    lit = set()
    for name, (fx0, fx1, fy0, fy1) in SEGMENTS.items():
        if fraction_on(upright, x + fx0 * w, y + fy0 * h, x + fx1 * w, y + fy1 * h) > LIT_THRESHOLD:
            lit.add(name)
    if not lit:
        return " "                                   # blank digit position
    return PATTERNS.get(frozenset(lit), "?")


def read_display(crop, save_overlay=None):
    """Return the temperature as a float, or None if any digit was unreadable."""
    ink = get_ink(crop)
    upright = deskew(ink)

    mx, my, mw, mh = MINUS_BOX
    negative = fraction_on(ink, mx, my, mx + mw, my + mh) > LIT_THRESHOLD

    chars = "".join(read_digit(upright, b) for b in DIGIT_BOXES).strip()
    if save_overlay:
        draw_overlay(upright, save_overlay)
    if not chars or "?" in chars or " " in chars:
        return None
    if DECIMALS:
        chars = chars[:-DECIMALS] + "." + chars[-DECIMALS:]
    value = float(chars)
    return -value if negative else value


def draw_overlay(upright, path):
    img = cv2.cvtColor(255 - upright, cv2.COLOR_GRAY2BGR)
    for (x, y, w, h) in DIGIT_BOXES:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        for (fx0, fx1, fy0, fy1) in SEGMENTS.values():
            cv2.rectangle(img, (int(x + fx0 * w), int(y + fy0 * h)),
                               (int(x + fx1 * w), int(y + fy1 * h)), (0, 0, 255), 1)
    mx, my, mw, mh = MINUS_BOX
    cv2.rectangle(img, (mx, my), (mx + mw, my + mh), (0, 160, 0), 1)
    cv2.imwrite(path, img)


if __name__ == "__main__":
    crop = cv2.imread("Box1_masked.png")
    print("Reading:", read_display(crop, save_overlay="debug_overlay.png"))