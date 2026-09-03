import json
from fontTools.ttLib import TTFont
from glob import glob

def build_ranges(font):
    chars = set()
    for table in font["cmap"].tables:
        if table.isUnicode():
            chars.update(table.cmap.keys())

    ranges = []
    start = prev = None
    for c in sorted(chars):
        if start is None:
            start = prev = c
        elif c == prev + 1:
            prev = c
        else:
            ranges.append((start, prev))
            start = prev = c
    if start is not None:
        ranges.append((start, prev))
    return ranges

def fmt(cp):
    if cp < 0x10000:
        return f"U+{cp:04X}"
    return f"U+{cp:05X}"

fonts = []
for path in glob('fonts/*'):
    font = TTFont(path)
    out = [f"{fmt(s)}-{fmt(e).replace('U+', '')}" if s != e else fmt(s)
           for s, e in build_ranges(font)]
            
    fonts.append({
        "url": path,
        "unicode-range": out,
    })

with open('fontFaces.json', 'w') as f:
    json.dump({'Noto Sans Regular': fonts}, f, indent=2);

