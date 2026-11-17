"""Builds custom_components/ourhome3d/furniture/ourhome_main.json: furniture made for our main floor and garage.

Same conventions as build_furniture.py: parts in metres (x left-right, z back(-)/front(+), y up from the floor,
or from the mount point for wall / ceiling items), converted to fractions of the item size.
Run: python3 tools/build_furniture_main.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "custom_components/ourhome3d/furniture/ourhome_main.json"

WHITE, OFFWHITE, BLACK, DARK, METAL, STEEL = "#f4f4f2", "#eeeeea", "#1c1c1c", "#2b2b2b", "#8a8d90", "#b8bcbf"
WALNUT, BRASS, GLASS = "#5a3520", "#b08d57", "glass"


class Item:
    def __init__(self, iid, name, size, **opts):
        self.id, self.name, self.size, self.opts, self.parts = iid, name, size, opts, []

    def part(self, shape, x0, x1, z0, z1, y0, y1, color, **extra):
        W, D, H = self.size
        p = {
            "shape": shape,
            "x": round((x0 + x1) / 2 / W, 4), "z": round((z0 + z1) / 2 / D, 4),
            "w": round((x1 - x0) / W, 4), "d": round((z1 - z0) / D, 4),
            "y": round(y0 / H, 4), "h": round((y1 - y0) / H, 4), "color": color,
        }
        if "top" in extra and isinstance(extra["top"], tuple):
            tx0, tx1, tz0, tz1 = extra.pop("top")
            p.update(tx=round((tx0 + tx1) / 2 / W, 4), tz=round((tz0 + tz1) / 2 / D, 4),
                     tw=round((tx1 - tx0) / W, 4), td=round((tz1 - tz0) / D, 4))
        p.update(extra)
        self.parts.append(p)
        return self

    def box(self, *a, **k):
        return self.part("box", *a, **k)

    def cyl(self, *a, **k):
        return self.part("cyl", *a, **k)

    def loft(self, *a, **k):
        return self.part("loft", *a, **k)

    def json(self):
        d = {"id": self.id, "name": {"en": self.name}, "size": list(self.size), "parts": self.parts}
        d.update(self.opts)
        return d


items = []


def item(*a, **k):
    it = Item(*a, **k)
    items.append(it)
    return it


# ---------------------------------------------------------------- nursery
W, D, H = 1.4, 0.76, 1.0
cr = item("crib", "Crib (white, slatted)", (W, D, H), group="kids", room=["nursery"], tags=["crib", "cot", "baby", "nursery"])
for x in (-W/2, W/2 - 0.05):
    for z in (-D/2, D/2 - 0.05):
        cr.box(x, x + 0.05, z, z + 0.05, 0, 0.98, WHITE)                    # corner posts
for x in (-W/2 + 0.05, W/2 - 0.07):
    cr.box(x, x + 0.02, -D/2 + 0.01, D/2 - 0.01, 0.12, 1.0, WHITE)          # head and foot panels
cr.box(-W/2 + 0.07, W/2 - 0.07, -D/2 + 0.05, D/2 - 0.05, 0.05, 0.27, "#f6f2f2")   # skirt
cr.box(-W/2 + 0.07, W/2 - 0.07, -D/2 + 0.05, D/2 - 0.05, 0.27, 0.42, "#f2c4cf")   # pink mattress
for z0 in (-D/2, D/2 - 0.03):
    cr.box(-W/2 + 0.05, W/2 - 0.05, z0, z0 + 0.03, 0.12, 0.16, WHITE)       # bottom rails
    cr.box(-W/2 + 0.05, W/2 - 0.05, z0, z0 + 0.03, 0.82, 0.86, WHITE)       # top rails
n = 16
for i in range(n):
    x = -W/2 + 0.1 + i * (W - 0.2) / (n - 1)
    for z0 in (-D/2 + 0.005, D/2 - 0.025):
        cr.box(x - 0.012, x + 0.012, z0, z0 + 0.02, 0.16, 0.82, WHITE)     # slats front and back

# ---------------------------------------------------------------- closets
COATS = ["#7f8fa6", "#2f3640", "#c23b3b", "#e5e5e0", "#6c7a5a", "#e9a3b3", "#3b5b92", "#bfa98a", "#4a4a4a", "#f2d0d6",
         "#5c6b73", "#9e2a2b"]
for vid, vname, double in (("closet_rod_double", "Closet rod & shelf (double hang)", True),
                           ("closet_rod_single", "Closet rod & shelf (long hang)", False)):
    W, D, H = 1.2, 0.5, 2.15
    cl = item(vid, vname, (W, D, H), group="storage", family="closet_rod", room=["closet", "bedroom"],
              variant={"en": "double hang" if double else "long hang"}, tags=["closet", "rod", "clothes", "wardrobe"])
    cl.box(-W/2, W/2, -D/2, -D/2 + 0.36, 2.05, 2.08, WHITE, fix="h")      # top shelf
    rods = (1.95, 1.0) if double else (1.95,)
    for y in rods:
        cl.cyl(-W/2, W/2, -0.04, -0.01, y - 0.015, y + 0.015, STEEL, axis="x", fix="dh")
    k = 12
    for r, y in enumerate(rods):
        bottom = y - (0.72 if double else 1.05)
        for i in range(k):
            x = -W/2 + 0.05 + i * (W - 0.1) / k
            col = COATS[(i * 5 + r * 3) % len(COATS)]
            cl.box(x, x + (W - 0.1) / k * 0.8, -0.2, 0.18, bottom, y - 0.03, col)

# ---------------------------------------------------------------- walls: mirrors, art, backsplash
rm = item("round_mirror", "Round mirror (black frame)", (0.9, 0.03, 0.9), mount="wall", wall_y=1.3, group="decor",
          room=["hallway", "entry", "bathroom"], tags=["mirror", "round"])
rm.cyl(-0.45, 0.45, -0.015, 0.005, 0, 0.9, BLACK, axis="z").cyl(-0.43, 0.43, 0.0, 0.015, 0.02, 0.88, GLASS, axis="z")

va = item("wall_art_canvas", "Landscape canvas (hanging)", (1.04, 0.03, 0.66), mount="wall", wall_y=1.25,
          group="decor", room=["dining", "living"], tags=["art", "painting", "canvas"])
va.box(-0.5, 0.5, -0.015, 0.0, 0.03, 0.63, "#7d8b6a")
va.box(-0.48, 0.48, 0.0, 0.004, 0.42, 0.62, "#b9c4c9").box(-0.48, 0.48, 0.0, 0.004, 0.08, 0.26, "#6f8f8f")
va.box(-0.52, 0.52, -0.015, 0.015, 0.62, 0.66, WALNUT).box(-0.52, 0.52, -0.015, 0.015, 0.0, 0.04, WALNUT)

fr = item("frames_row3", "Framed photos (3 in a row)", (1.9, 0.03, 0.62), mount="wall", wall_y=1.35, group="decor",
          room=["bedroom", "living"], tags=["photo", "frame", "picture", "wedding"])
for x in (-0.95, -0.3, 0.35):
    fr.box(x, x + 0.6, -0.015, 0.015, 0, 0.62, BLACK).box(x + 0.05, x + 0.55, 0.0, 0.017, 0.05, 0.57, "#f4f1ea")
    fr.box(x + 0.1, x + 0.5, 0.0, 0.019, 0.1, 0.52, "#6d7d63")

ng = item("nursery_gallery", "Storybook gallery wall", (1.6, 0.03, 1.3), mount="wall", wall_y=1.0, group="decor",
          room=["nursery"], tags=["art", "gallery", "storybook", "nursery"])
ART = ["#cfc2a8", "#d9c9e6", "#c9dbe8", "#f0c9d6", "#d8c9e8", "#e8dfc2", "#c4dcc4", "#2f3b55"]
for i, (x, y) in enumerate(((-0.8, 0.55), (-0.45, 0.82), (0.05, 0.82), (0.45, 0.6), (-0.8, 0.05), (-0.45, -0.05),
                            (0.05, -0.05), (0.45, 0.1))):
    ng.box(x + 0.0, x + 0.3, -0.01, 0.01, y + 0.12, y + 0.44, ART[i])
for x0, x1, y0, y1 in ((-0.38, 0.32, 0.62, 0.7), (-0.25, 0.2, 0.42, 0.5)):
    ng.box(x0, x1, -0.01, 0.012, y0, y1, "#fbfaf7")                           # "Once upon a time"

bs = item("backsplash", "Tile backsplash (dark)", (1.0, 0.012, 0.48), mount="wall", wall_y=0.92, group="kitchen",
          room=["kitchen"], tags=["backsplash", "tile", "kitchen"])
bs.box(-0.5, 0.5, -0.006, 0.006, 0, 0.48, "#2c2f33")
for y in (0.12, 0.24, 0.36):
    bs.box(-0.5, 0.5, 0.005, 0.007, y - 0.004, y + 0.004, "#45494e")

# ---------------------------------------------------------------- living
W, D, H = 1.9, 0.25, 3.0
fp = item("stone_fireplace", "Stone fireplace with mantel", (W, D, H), group="living", room=["living"],
          tags=["fireplace", "stone", "mantel", "hearth"], electric=True)
fp.box(-W/2, W/2, -D/2, -D/2 + 0.06, 0, H, "#c9c3b5", edges="faint")       # stone facing
for y in (0.2, 0.45, 1.05, 1.6, 1.85, 2.1, 2.35, 2.6, 2.85):
    fp.box(-W/2, W/2, -D/2 + 0.06, -D/2 + 0.065, y, y + 0.012, "#a9a294")    # mortar courses
fp.box(-0.55, 0.55, -D/2 + 0.06, -D/2 + 0.08, 0.45, 0.95, "#111111")       # electric insert
fp.box(-0.45, 0.45, -D/2 + 0.08, -D/2 + 0.085, 0.5, 0.56, "#e8742c")       # flame bed
fp.box(-0.95, 0.95, -D/2 + 0.06, D/2, 1.28, 1.43, "#5b5e60")               # mantel beam

W, D, H = 0.9, 0.9, 0.47
ct = item("coffee_table_farmhouse", "Farmhouse coffee table", (W, D, H), group="living", room=["living"],
          tags=["coffee table", "table", "farmhouse"], surface=True)
ct.box(-W/2, W/2, -D/2, D/2, 0.42, 0.47, "#6e655c", fix="h")
ct.box(-W/2 + 0.03, W/2 - 0.03, -D/2 + 0.03, D/2 - 0.03, 0.06, 0.42, BLACK)
ct.box(-W/2 + 0.04, W/2 - 0.04, -D/2 + 0.04, D/2 - 0.04, 0.0, 0.06, BLACK)
for s in (-1, 1):
    ct.loft(-0.35, 0.35, s * (D/2 - 0.03) - 0.006, s * (D/2 - 0.03) + 0.006, 0.08, 0.4, "#2a2a2a",
            top=(-0.05, 0.05, s * (D/2 - 0.03) - 0.006, s * (D/2 - 0.03) + 0.006))      # barn-door X look

W, D, H = 0.55, 0.35, 2.1
gc = item("grandfather_clock", "Grandfather clock", (W, D, H), group="decor", room=["dining", "living", "hallway"],
          tags=["clock", "grandfather", "pendulum"])
gc.box(-W/2, W/2, -D/2, D/2, 0, 0.35, WALNUT)
gc.box(-W/2 + 0.04, W/2 - 0.04, -D/2 + 0.02, D/2 - 0.02, 0.35, 1.45, WALNUT)
gc.box(-W/2 + 0.08, W/2 - 0.08, D/2 - 0.03, D/2 - 0.01, 0.4, 1.4, GLASS)
gc.cyl(-0.012, 0.012, 0.0, 0.02, 0.6, 1.3, BRASS).cyl(-0.08, 0.08, 0.02, 0.06, 0.6, 0.76, BRASS, axis="z")
gc.box(-W/2, W/2, -D/2, D/2, 1.45, 1.95, WALNUT)
gc.cyl(-0.17, 0.17, D/2 - 0.02, D/2 + 0.0, 1.53, 1.87, "#e3cf8f", axis="z")
gc.loft(-W/2, W/2, -D/2, D/2, 1.95, 2.1, "#4a2a18", top=(-W/2 + 0.12, W/2 - 0.12, -D/2 + 0.05, D/2 - 0.05))

W, D, H = 1.0, 1.0, 2.1
tr = item("christmas_tree", "Christmas tree", (W, D, H), group="decor", room=["living"],
          tags=["christmas", "tree", "holiday", "seasonal"])
tr.cyl(-0.4, 0.4, -0.4, 0.4, 0, 0.05, "#a21d2a").cyl(-0.05, 0.05, -0.05, 0.05, 0.05, 0.25, "#5a3a22")
for y0, y1, r in ((0.2, 0.75, 0.5), (0.6, 1.15, 0.41), (1.0, 1.5, 0.32), (1.35, 1.8, 0.22), (1.65, 1.98, 0.12)):
    tr.loft(-r, r, -r, r, y0, y1, "#2f5a34", top=(-0.03, 0.03, -0.03, 0.03))
ORN = [("#c4202d", 0.42), ("#e8e8e8", 0.37), ("#c4202d", 0.31), ("#c0c4c8", 0.27), ("#e8e8e8", 0.22), ("#c4202d", 0.17)]
import math
for i in range(12):
    col, r = ORN[i % len(ORN)]
    y = 0.4 + (i % 6) * 0.24
    a = i * 2.4
    x, z = r * 0.85 * math.cos(a), r * 0.85 * math.sin(a)
    tr.cyl(x - 0.04, x + 0.04, z - 0.04, z + 0.04, y, y + 0.08, col)
tr.loft(-0.1, 0.1, -0.1, 0.1, 1.92, 2.08, "#c4202d", top=(0.06, 0.1, -0.02, 0.02)).box(-0.1, 0.1, -0.1, 0.1, 1.92, 1.96, "#f4f4f2")

# ---------------------------------------------------------------- hallway / entry
W, D, H = 1.05, 0.3, 0.8
cn = item("console_x", "Console table (black metal, grey shelves)", (W, D, H), group="living",
          room=["hallway", "entry", "living"], tags=["console", "table", "entry"], surface=True)
cn.box(-W/2, W/2, -D/2, D/2, 0.76, 0.8, "#8a8986", fix="h").box(-W/2 + 0.02, W/2 - 0.02, -D/2 + 0.01, D/2 - 0.01, 0.12, 0.15, "#8a8986", fix="h")
for x in (-W/2, W/2 - 0.025):
    for z in (-D/2, D/2 - 0.025):
        cn.box(x, x + 0.025, z, z + 0.025, 0, 0.76, BLACK, fix="wd")
cn.box(-W/2, W/2, D/2 - 0.025, D/2, 0.72, 0.76, BLACK, fix="h")

W, D, H = 1.1, 0.45, 2.3
mu = item("mudroom_locker", "Mudroom bench with hooks and cubbies", (W, D, H), group="storage", room=["entry", "hallway"],
          tags=["mudroom", "locker", "bench", "hooks", "cubby"])
for x in (-W/2, W/2 - 0.04):
    mu.box(x, x + 0.04, -D/2, D/2, 0, H, WHITE, fix="w")                    # sides
mu.box(-W/2 + 0.04, W/2 - 0.04, -D/2, -D/2 + 0.02, 0, H, OFFWHITE)          # beadboard back
mu.box(-W/2, W/2, -D/2, D/2, H - 0.04, H, WHITE, fix="h")                   # top
mu.box(-W/2 + 0.04, W/2 - 0.04, -D/2, D/2, 1.85, 1.89, WHITE, fix="h")      # cubby shelf
mu.box(-0.02, 0.02, -D/2, D/2, 1.89, H - 0.04, WHITE, fix="w")              # cubby divider
mu.box(-W/2 + 0.04, W/2 - 0.04, -D/2, D/2, 0.45, 0.5, WHITE, fix="h")       # bench seat
mu.box(-W/2 + 0.04, W/2 - 0.04, -D/2, D/2, 0.0, 0.08, WHITE, fix="h")       # plinth
mu.box(-W/2 + 0.04, W/2 - 0.04, -D/2 + 0.02, -D/2 + 0.05, 1.55, 1.62, WHITE, fix="h")   # hook rail
for i in range(5):
    x = -0.4 + i * 0.2
    mu.box(x - 0.012, x + 0.012, -D/2 + 0.05, -D/2 + 0.1, 1.52, 1.6, BLACK)
for x0, x1, col in ((-0.45, -0.2, "#1f1f22"), (-0.18, 0.05, "#3a3a3d"), (0.12, 0.32, "#202024")):
    mu.box(x0, x1, -D/2 + 0.04, -D/2 + 0.2, 0.75, 1.55, col)                # coats and bags

# ---------------------------------------------------------------- lights (hanging from the ceiling)
W, D, H = 0.45, 0.45, 1.6
la = item("lantern_pendant", "Lantern pendant (black cage)", (W, D, H), mount="ceiling", group="lights",
          room=["hallway", "entry"], tags=["pendant", "lantern", "chandelier", "foyer"], electric=True, light="pendant")
la.cyl(-0.015, 0.015, -0.015, 0.015, 0.45, H, BLACK).box(-0.08, 0.08, -0.08, 0.08, H - 0.02, H, BLACK)
for x in (-W/2, W/2 - 0.02):
    for z in (-D/2, D/2 - 0.02):
        la.box(x, x + 0.02, z, z + 0.02, 0, 0.45, BLACK)
for y in (0, 0.43):
    la.box(-W/2, W/2, -D/2, -D/2 + 0.02, y, y + 0.02, BLACK).box(-W/2, W/2, D/2 - 0.02, D/2, y, y + 0.02, BLACK)
    la.box(-W/2, -W/2 + 0.02, -D/2, D/2, y, y + 0.02, BLACK).box(W/2 - 0.02, W/2, -D/2, D/2, y, y + 0.02, BLACK)
for x, z in ((-0.08, 0), (0.08, 0), (0, -0.08), (0, 0.08)):
    la.cyl(x - 0.02, x + 0.02, z - 0.02, z + 0.02, 0.12, 0.2, BLACK).cyl(x - 0.018, x + 0.018, z - 0.018, z + 0.018, 0.2, 0.28, "white", glow=True)

W, D, H = 0.22, 0.22, 1.0
cp = item("cylinder_pendant", "Glass cylinder pendant", (W, D, H), mount="ceiling", group="lights",
          room=["kitchen", "dining"], tags=["pendant", "island", "glass"], electric=True, light="pendant")
cp.cyl(-0.012, 0.012, -0.012, 0.012, 0.3, H, BLACK).cyl(-0.06, 0.06, -0.06, 0.06, H - 0.02, H, BLACK)
cp.cyl(-0.11, 0.11, -0.11, 0.11, 0.27, 0.3, BLACK).cyl(-0.11, 0.11, -0.11, 0.11, 0.0, 0.27, GLASS)
cp.cyl(-0.11, 0.11, -0.11, 0.11, 0.0, 0.015, BLACK).cyl(-0.035, 0.035, -0.035, 0.035, 0.08, 0.2, "white", glow=True)

W, D, H = 0.75, 0.32, 1.4
dp = item("linear_cage_pendant", "Linear cage pendant (black and brass)", (W, D, H), mount="ceiling", group="lights",
          room=["dining", "kitchen"], tags=["pendant", "chandelier", "dining"], electric=True, light="pendant")
for x in (-0.25, 0.25):
    dp.cyl(x - 0.008, x + 0.008, -0.008, 0.008, 0.3, H, BRASS)
dp.box(-0.3, 0.3, -0.05, 0.05, H - 0.02, H, BRASS)
for y, w, d in ((0.0, W, D), (0.28, W - 0.12, D - 0.1)):
    dp.box(-w/2, w/2, -d/2, -d/2 + 0.015, y, y + 0.015, BLACK).box(-w/2, w/2, d/2 - 0.015, d/2, y, y + 0.015, BLACK)
    dp.box(-w/2, -w/2 + 0.015, -d/2, d/2, y, y + 0.015, BLACK).box(w/2 - 0.015, w/2, -d/2, d/2, y, y + 0.015, BLACK)
for x in (-0.24, -0.08, 0.08, 0.24):
    dp.cyl(x - 0.025, x + 0.025, -0.025, 0.025, 0.08, 0.2, "white", glow=True)

# ---------------------------------------------------------------- garage
def vehicle(vid, name, size, body, roof_from, hood_to, glass="#1f262b", trim=BLACK, rails=False, bed=False):
    W, D, H = size
    v = item(vid, name, size, group="vehicles", room=["garage"], tags=["car", "vehicle"], vehicle=True)
    for z in (-D/2 + 0.85, D/2 - 0.95):                                     # wheels
        for x0 in (-W/2, W/2 - 0.26):
            v.cyl(x0, x0 + 0.26, z - 0.38, z + 0.38, 0.0, 0.76, "#1a1a1a", axis="x")
            v.cyl(x0 + (0.0 if x0 < 0 else 0.2) - 0.005, x0 + (0.06 if x0 < 0 else 0.265), z - 0.22, z + 0.22, 0.16, 0.6, "#8f9499", axis="x")
    v.box(-W/2 + 0.04, W/2 - 0.04, -D/2, D/2, 0.3, 1.02, body)               # lower body
    v.box(-W/2 + 0.06, W/2 - 0.06, D/2 - 0.04, D/2, 0.38, 0.75, trim)        # grille / bumper
    v.box(-W/2 + 0.12, -W/2 + 0.4, D/2 - 0.03, D/2 + 0.0, 0.8, 0.9, "#e9eef2").box(W/2 - 0.4, W/2 - 0.12, D/2 - 0.03, D/2, 0.8, 0.9, "#e9eef2")
    v.loft(-W/2 + 0.06, W/2 - 0.06, roof_from, hood_to, 1.02, H, body,
           top=(-W/2 + 0.16, W/2 - 0.16, roof_from + 0.15, hood_to - 0.55))  # cab / greenhouse
    v.loft(-W/2 + 0.05, W/2 - 0.05, roof_from + 0.1, hood_to - 0.12, 1.08, H - 0.08, glass,
           top=(-W/2 + 0.15, W/2 - 0.15, roof_from + 0.22, hood_to - 0.6))   # windows band
    ins = 0.3 if rails else 0.15
    v.box(-W/2 + ins, W/2 - ins, roof_from + 0.12, hood_to - 0.6, H - 0.06, H, body)   # roof skin
    v.box(-W/2 - 0.02, -W/2 + 0.04, hood_to - 0.45, hood_to - 0.3, 1.02, 1.15, trim)    # mirrors
    v.box(W/2 - 0.04, W/2 + 0.02, hood_to - 0.45, hood_to - 0.3, 1.02, 1.15, trim)
    if rails:
        for x in (-W/2 + 0.22, W/2 - 0.28):
            v.box(x, x + 0.06, roof_from + 0.3, hood_to - 0.75, H - 0.07, H, "#c0c4c8")   # roof rails
    if bed:
        v.box(-W/2 + 0.08, W/2 - 0.08, -D/2 + 0.05, roof_from - 0.05, 0.98, 1.02, "#202020")   # bed liner
        v.box(-W/2 + 0.04, W/2 - 0.04, -D/2, -D/2 + 0.06, 1.02, 1.3, body)                     # tailgate
        v.box(-W/2 + 0.04, -W/2 + 0.12, -D/2, roof_from, 1.02, 1.3, body).box(W/2 - 0.12, W/2 - 0.04, -D/2, roof_from, 1.02, 1.3, body)
    return v


vehicle("pickup_truck", "Pickup truck (white, crew cab)", (1.9, 5.6, 1.85), "#f3f3f1", roof_from=-0.55,
        hood_to=1.85, bed=True)
vehicle("suv", "SUV (black, 3-row)", (1.98, 5.0, 1.78), "#1c1d20", roof_from=-2.35, hood_to=1.25,
        glass="#0f1215", trim="#2a2b2e", rails=True)

for vid, vname, body, lid in (("wheelie_bin_green", "Wheelie bin (green)", "#2e8b6e", "#1d1d1d"),
                              ("wheelie_bin_recycling", "Wheelie bin (black, yellow lid)", "#232323", "#f2c230")):
    W, D, H = 0.62, 0.75, 1.1
    b = item(vid, vname, (W, D, H), group="garage", family="wheelie_bin", variant={"en": vname.split("(")[1][:-1]},
             room=["garage"], tags=["trash", "bin", "recycling", "garbage"])
    b.loft(-0.26, 0.26, -0.3, 0.32, 0.06, 1.02, body, top=(-0.3, 0.3, -0.36, 0.36))
    b.box(-0.31, 0.31, -0.37, 0.375, 1.02, 1.1, lid).box(-0.2, 0.2, -0.38, -0.33, 0.92, 1.0, body)
    b.cyl(-0.3, -0.22, -0.36, -0.2, 0.0, 0.16, "#151515", axis="x").cyl(0.22, 0.3, -0.36, -0.2, 0.0, 0.16, "#151515", axis="x")

W, D, H = 2.6, 0.62, 2.1
wb = item("workbench_pegboard", "Workbench with pegboard and shelf", (W, D, H), group="garage", room=["garage"],
          tags=["workbench", "pegboard", "tools", "bench"], surface=True)
wb.box(-W/2, W/2, -D/2 + 0.02, D/2, 0.86, 0.9, "#c9a46a", fix="h")
wb.box(-W/2 + 0.04, W/2 - 0.04, -D/2 + 0.04, D/2 - 0.04, 0.3, 0.33, "#c9a46a", fix="h")
wb.box(-W/2, W/2, D/2 - 0.04, D/2, 0.76, 0.86, "#6e6e6e", fix="h")
for x in (-W/2, -0.02, W/2 - 0.06):
    for z in (-D/2 + 0.04, D/2 - 0.08):
        wb.box(x, x + 0.06, z, z + 0.04, 0, 0.86, "#6e6e6e", fix="w")
wb.box(-W/2, W/2, -D/2, -D/2 + 0.02, 0.9, 1.9, "#f0efe9", fix="h")          # pegboard
wb.box(-W/2, W/2, -D/2, -D/2 + 0.32, 1.9, 1.93, "#c9a46a", fix="h")         # upper shelf
for x0, x1, col in ((-1.25, -0.85, "#1e1e1e"), (-0.8, -0.55, "#3d8bd6"), (-0.5, -0.12, "#4a4d50"),
                    (-0.05, 0.38, "#5e6063"), (0.42, 0.85, "#3a3c3f")):
    wb.box(x0, x1, -D/2 + 0.03, -D/2 + 0.3, 1.93, 2.1 if col != "#3d8bd6" else 2.08, col)   # coolers on the shelf
for x0, x1, y0, y1, col in ((-1.1, -0.9, 1.25, 1.45, "#2a62b8"), (-0.6, -0.45, 1.2, 1.5, "#1f1f1f"),
                            (-0.2, 0.2, 1.15, 1.35, "#2b2b2b"), (0.6, 0.9, 1.0, 1.35, "#3a7a3a")):
    wb.box(x0, x1, -D/2 + 0.02, -D/2 + 0.05, y0, y1, col)                     # tools on the pegboard
for x0, x1, col in ((-1.1, -0.85, "#d6d6d6"), (-0.8, -0.6, "#c03030"), (-0.55, -0.35, "#2b5fa8")):
    wb.box(x0, x1, -0.2, 0.05, 0.33, 0.55, col)                               # paint cans below

po = item("post_column", "Support post (white)", (0.15, 0.15, 3.2), group="structure", room=["garage", "basement"],
          tags=["post", "column", "pillar"])
po.box(-0.075, 0.075, -0.075, 0.075, 0, 3.2, WHITE, fix="wd")

pack = {
    "format": "fp3dpack", "version": 1, "id": "ourhome.main", "name": "Our main floor",
    "publisher": "Our Home 3D", "release": 1,
    "description": "Furniture made for our main floor and garage: nursery, closets, living room, lights and vehicles.",
    "items": [i.json() for i in items],
}
for it in pack["items"]:
    assert len(it["parts"]) <= 60, (it["id"], len(it["parts"]))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(pack, indent=1) + "\n", encoding="utf-8")
print(f"{len(items)} items, {sum(len(i.parts) for i in items)} parts -> {OUT}")
for i in items:
    print(f"  {i.id}: {len(i.parts)} parts")
