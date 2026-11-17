"""Builds custom_components/ourhome3d/furniture/ourhome_basement.json.

Parts are written in metres (x0, x1 left-right; z0, z1 back-front, front = +z; y0, y1 up from the floor or mount)
and converted to the pack format (fractions of the item size). Run: python3 tools/build_furniture.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "custom_components/ourhome3d/furniture/ourhome_basement.json"

BLACK, DARK, METAL, STEEL = "#1c1c1c", "#2b2b2b", "#8a8d90", "#b8bcbf"


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


# ---------------------------------------------------------------- office
t = item("treadmill", "Treadmill", (0.85, 1.9, 1.4), group="fitness", room=["office", "basement"],
         tags=["treadmill", "fitness", "exercise"], electric=True)
W, D = 0.85, 1.9
t.box(-W/2, W/2, -0.95, 0.95, 0, 0.13, DARK, fix="h")                     # deck frame
t.box(-0.3, 0.3, -0.8, 0.9, 0.13, 0.145, BLACK, fix="h")                  # belt
for s in (-1, 1):
    t.box(s*0.3, s*0.41, -0.8, 0.9, 0.13, 0.15, METAL, fix="h")           # side rails (mirrored below)
t.parts[-2]["x"], t.parts[-2]["w"] = round(-0.355/W, 4), round(0.11/W, 4)
t.parts[-1]["x"], t.parts[-1]["w"] = round(0.355/W, 4), round(0.11/W, 4)
for s in (-1, 1):                                                         # slanted uprights
    t.loft(s*0.36-0.035, s*0.36+0.035, -0.78, -0.70, 0.13, 1.1, METAL, top=(s*0.36-0.03, s*0.36+0.03, -0.92, -0.86))
t.box(-0.42, 0.42, -0.95, -0.70, 1.1, 1.22, DARK)                         # console
t.box(-0.15, 0.15, -0.86, -0.80, 1.18, 1.3, "#5d6166")                    # display
for s in (-1, 1):
    t.box(s*0.3-0.02, s*0.3+0.02, -0.82, -0.55, 1.0, 1.05, BLACK)         # handlebars
t.parts[-2]["x"] = round(-0.3/W, 4); t.parts[-1]["x"] = round(0.3/W, 4)

c = item("dog_crate", "Dog crate (wire)", (1.07, 0.71, 0.76), group="pets", room=["basement", "office"],
         tags=["dog", "crate", "kennel", "pet"])
W, D, H = 1.07, 0.71, 0.76
c.box(-W/2, W/2, -D/2, D/2, 0, 0.03, BLACK)                               # tray
c.box(-W/2, W/2, -D/2, D/2, H-0.02, H, BLACK, edges="faint")              # top frame (solid look from above)
for x in (-W/2, W/2-0.02):
    for z in (-D/2, D/2-0.02):
        c.box(x, x+0.02, z, z+0.02, 0, H, BLACK)                          # corner posts
n = 9
for i in range(1, n):
    x = -W/2 + i*W/n
    c.box(x-0.004, x+0.004, D/2-0.008, D/2, 0.03, H-0.02, BLACK)          # front bars
    c.box(x-0.004, x+0.004, -D/2, -D/2+0.008, 0.03, H-0.02, BLACK)        # back bars
m = 6
for i in range(1, m):
    z = -D/2 + i*D/m
    c.box(-W/2, -W/2+0.008, z-0.004, z+0.004, 0.03, H-0.02, BLACK)
    c.box(W/2-0.008, W/2, z-0.004, z+0.004, 0.03, H-0.02, BLACK)
for y in (0.25, 0.5):
    c.box(-W/2, W/2, D/2-0.01, D/2, y, y+0.012, BLACK)
    c.box(-W/2, W/2, -D/2, -D/2+0.01, y, y+0.012, BLACK)

for vid, vname, col in (("dog_cot_grey", "Raised dog cot (grey)", "#8f9396"), ("dog_cot_black", "Raised dog cot (black)", "#262626")):
    d = item(vid, vname, (1.07, 0.81, 0.2), group="pets", family="dog_cot", variant={"en": vname.split("(")[1][:-1]},
             room=["basement", "office"], tags=["dog", "bed", "cot", "pet"])
    W, D, H = 1.07, 0.81, 0.2
    d.box(-W/2+0.03, W/2-0.03, -D/2+0.03, D/2-0.03, 0.15, 0.17, col)       # mesh
    for x0, x1, z0, z1 in ((-W/2, W/2, -D/2, -D/2+0.03), (-W/2, W/2, D/2-0.03, D/2), (-W/2, -W/2+0.03, -D/2, D/2), (W/2-0.03, W/2, -D/2, D/2)):
        d.box(x0, x1, z0, z1, 0.15, 0.18, BLACK)                          # frame tubes
    for x in (-W/2+0.05, W/2-0.08):
        for z in (-D/2+0.05, D/2-0.08):
            d.box(x, x+0.03, z, z+0.03, 0, 0.15, BLACK)                   # legs

p = item("printer", "Printer", (0.45, 0.4, 0.25), group="office", room=["office"], tags=["printer"], electric=True)
p.box(-0.225, 0.225, -0.2, 0.2, 0, 0.22, DARK).box(-0.18, 0.18, 0.12, 0.2, 0.06, 0.08, BLACK).box(-0.2, 0.2, -0.18, 0.15, 0.22, 0.25, "#3a3a3a")

# ---------------------------------------------------------------- bedroom / bathroom
mr = item("floor_mirror", "Standing mirror", (0.45, 0.05, 1.6), group="decor", room=["bedroom", "guest_bedroom"],
          tags=["mirror"])
mr.box(-0.225, 0.225, -0.025, 0.025, 0, 1.6, BLACK, fix="w").box(-0.2, 0.2, 0.0, 0.03, 0.03, 1.57, "glass")

wm = item("wall_mirror", "Wall mirror", (0.9, 0.02, 1.0), mount="wall", wall_y=0.98, group="decor",
          room=["bathroom"], tags=["mirror", "bathroom"])
wm.box(-0.45, 0.45, -0.01, 0.01, 0, 1.0, "#d6dbde", edges="faint").box(-0.44, 0.44, 0.0, 0.012, 0.01, 0.99, "glass")

vl = item("vanity_light", "Vanity light (3 shades)", (0.75, 0.16, 0.22), mount="wall", wall_y=1.95, group="lights",
          room=["bathroom"], tags=["light", "vanity", "bathroom"], electric=True, light="wall")
vl.box(-0.375, 0.375, -0.08, -0.05, 0.16, 0.19, BLACK)
for x in (-0.25, 0.0, 0.25):
    vl.box(x-0.01, x+0.01, -0.08, 0.02, 0.16, 0.18, BLACK)
    vl.cyl(x-0.05, x+0.05, -0.03, 0.07, 0.0, 0.15, "white", glow=True)

# ---------------------------------------------------------------- living area
ls = item("shelf_floor_lamp", "Shelf floor lamp", (0.3, 0.3, 1.6), group="lights", room=["basement", "living"],
          tags=["lamp", "floor lamp", "etagere"], electric=True, light="floor")
for x in (-0.15, 0.13):
    for z in (-0.15, 0.13):
        ls.box(x, x+0.02, z, z+0.02, 0, 1.28, BLACK)
for y in (0.02, 0.38, 0.72, 1.05):
    ls.box(-0.15, 0.15, -0.15, 0.15, y, y+0.02, BLACK)
ls.box(-0.14, 0.14, -0.14, 0.14, 1.28, 1.6, "white", glow=True)

ss = item("speaker_stand", "Speaker on stand", (0.26, 0.26, 1.08), group="media", room=["basement", "living"],
          tags=["speaker", "stand", "surround"], electric=True)
ss.box(-0.13, 0.13, -0.13, 0.13, 0, 0.02, BLACK).cyl(-0.02, 0.02, -0.02, 0.02, 0.02, 0.92, BLACK)
ss.box(-0.1, 0.1, -0.08, 0.08, 0.92, 1.08, "#202020")

ap = item("air_purifier", "Air purifier", (0.22, 0.22, 0.36), group="appliances", room=["basement", "bedroom", "living"],
          tags=["air purifier", "purifier"], electric=True)
ap.cyl(-0.11, 0.11, -0.11, 0.11, 0, 0.34, "#f2f2f2").cyl(-0.09, 0.09, -0.09, 0.09, 0.34, 0.36, DARK)

ld = item("wall_ledge", "Wall ledge (chair rail shelf)", (3.0, 0.1, 0.06), mount="wall", wall_y=0.93, group="decor",
          room=["basement", "bedroom", "office"], tags=["ledge", "shelf", "chair rail", "trim"])
ld.box(-1.5, 1.5, -0.05, 0.05, 0.03, 0.05, "#f4f4f1", fix="d").box(-1.5, 1.5, -0.05, -0.03, 0.0, 0.06, "#f4f4f1", fix="d")

for vid, vname, col in (("helmet_shelf_red", "Helmet shelf (red)", "#e31837"), ("helmet_shelf_crimson", "Helmet shelf (crimson)", "#9e1b32")):
    hs = item(vid, vname, (0.5, 0.24, 0.32), mount="wall", wall_y=1.2, group="decor", family="helmet_shelf",
              variant={"en": vname.split("(")[1][:-1]}, room=["basement"], tags=["helmet", "shelf", "football"])
    hs.box(-0.25, 0.25, -0.12, 0.12, 0.0, 0.025, "#5b4636")
    for x in (-0.2, 0.18):
        hs.box(x, x+0.02, -0.12, -0.1, 0.0, 0.24, BLACK)
    hs.cyl(-0.12, 0.12, -0.11, 0.11, 0.025, 0.26, col).box(0.0, 0.13, 0.02, 0.11, 0.05, 0.13, "#e8e8e8")

bc = item("bat_case", "Baseball bat display case", (0.95, 0.1, 0.1), mount="wall", wall_y=1.65, group="decor",
          room=["basement"], tags=["bat", "baseball", "display"])
bc.box(-0.475, -0.44, -0.05, 0.05, 0, 0.1, BLACK).box(0.44, 0.475, -0.05, 0.05, 0, 0.1, BLACK)
bc.box(-0.44, 0.44, -0.045, 0.045, 0.005, 0.095, "glass", edges="faint")
bc.loft(-0.42, 0.42, -0.015, 0.015, 0.035, 0.065, "#c49a6c", top=(-0.42, 0.42, -0.015, 0.015))

for vid, vname, a, b in (("wall_flag_red", "Wall flag (red and gold)", "#e31837", "#ffb81c"), ("wall_flag_blue", "Wall flag (light blue)", "#74b4e6", "#174885")):
    fl = item(vid, vname, (1.5, 0.012, 0.9), mount="wall", wall_y=1.3, group="decor", family="wall_flag",
              variant={"en": vname.split("(")[1][:-1]}, room=["basement"], tags=["flag", "banner"])
    fl.box(-0.75, 0.75, -0.006, 0.0, 0, 0.9, a)
    fl.box(0.45, 0.6, -0.006, 0.006, 0, 0.9, b).box(0.62, 0.68, -0.006, 0.006, 0, 0.9, "white")

fr = item("photo_frames", "Framed photos (3, stacked)", (0.3, 0.03, 1.05), mount="wall", wall_y=1.15, group="decor",
          room=["basement", "living"], tags=["photo", "frame", "picture"])
for y in (0.0, 0.36, 0.72):
    fr.box(-0.15, 0.15, -0.015, 0.015, y, y+0.33, "#2d2622").box(-0.11, 0.11, 0.0, 0.017, y+0.05, y+0.28, "#cfd6dc")

# ---------------------------------------------------------------- storage / mechanical
ah = item("air_handler", "Air handler with plenum", (0.6, 0.65, 2.4), group="mechanical", room=["storage", "utility"],
          tags=["hvac", "air handler", "furnace", "ac"], electric=True)
ah.box(-0.3, 0.3, -0.3, 0.325, 0, 0.12, METAL, fix="h")                   # drain pan stand
ah.box(-0.3, 0.3, -0.3, 0.3, 0.12, 1.32, "#5f605c")                        # cabinet
ah.box(-0.28, 0.28, 0.3, 0.31, 0.7, 0.72, "#4b4c49")                       # panel seam
ah.box(-0.24, 0.24, -0.28, 0.28, 1.32, 2.4, STEEL, edges="faint")         # plenum to the ceiling
ah.box(-0.06, 0.06, 0.3, 0.32, 1.35, 1.45, "#f1f1f1")                     # thermostat

ws = item("water_softener", "Water softener", (0.26, 0.26, 1.15), group="mechanical", room=["storage", "utility"],
          tags=["water softener", "softener", "filter"])
ws.cyl(-0.13, 0.13, -0.13, 0.13, 0, 1.02, BLACK).box(-0.09, 0.09, -0.09, 0.09, 1.02, 1.15, "#2e2e2e")

ep = item("electrical_panel", "Electrical panel", (0.36, 0.1, 0.9), mount="wall", wall_y=0.95, group="mechanical",
          room=["storage", "utility", "garage"], tags=["breaker", "electrical", "panel"], electric=True)
ep.box(-0.18, 0.18, -0.05, 0.04, 0, 0.9, "#8c8f90", edges=True).box(-0.12, 0.12, 0.04, 0.045, 0.25, 0.65, "#7b7e7f")
ep.box(-0.01, 0.01, 0.04, 0.05, 0.42, 0.48, BLACK)

sp = item("support_post", "Steel support post", (0.11, 0.11, 2.5), group="structure", room=["storage", "basement"],
          tags=["post", "column", "lally"])
sp.cyl(-0.04, 0.04, -0.04, 0.04, 0, 2.47, "#5a3d2e").box(-0.055, 0.055, -0.055, 0.055, 2.47, 2.5, "#4a3428")

bm = item("steel_beam", "Steel I-beam", (6.0, 0.15, 0.25), mount="ceiling", group="structure",
          room=["storage", "basement"], tags=["beam", "girder", "i-beam"])
bm.box(-3, 3, -0.075, 0.075, 0, 0.02, "#4a3428", fix="dh").box(-3, 3, -0.075, 0.075, 0.23, 0.25, "#4a3428", fix="dh")
bm.box(-3, 3, -0.008, 0.008, 0.02, 0.23, "#553b2d", fix="dh")

du = item("duct_trunk", "HVAC duct trunk", (6.0, 0.5, 0.3), mount="ceiling", group="mechanical",
          room=["storage", "utility"], tags=["duct", "hvac", "trunk line"])
du.box(-3, 3, -0.25, 0.25, 0, 0.3, STEEL, edges="faint")

sb = item("storage_boxes", "Stacked storage boxes", (0.6, 0.45, 0.75), group="storage", room=["storage"],
          tags=["boxes", "cardboard", "moving"])
sb.box(-0.3, 0.3, -0.225, 0.225, 0, 0.4, "#b08d5e").box(-0.27, 0.25, -0.2, 0.21, 0.4, 0.75, "#a6845a")

lg = item("luggage", "Suitcases", (0.75, 0.3, 0.72), group="storage", room=["storage"], tags=["luggage", "suitcase"])
lg.box(-0.375, 0.0, -0.15, 0.15, 0.04, 0.72, "#a89a83").box(0.03, 0.375, -0.13, 0.13, 0.04, 0.6, "#a89a83")
for x in (-0.33, -0.05, 0.07, 0.33):
    lg.cyl(x-0.025, x+0.025, -0.025, 0.025, 0, 0.04, BLACK)

db = item("dog_bed", "Dog bed cushion", (0.9, 0.7, 0.2), group="pets", room=["storage", "basement"],
          tags=["dog", "bed", "cushion", "pet"])
db.box(-0.45, 0.45, -0.35, 0.35, 0, 0.12, "#6b6b6b").box(-0.45, 0.45, -0.35, -0.22, 0.12, 0.2, "#5d5d5d")

pack = {
    "format": "fp3dpack", "version": 1, "id": "ourhome.basement", "name": "Our basement",
    "publisher": "Our Home 3D", "release": 1,
    "description": "Furniture made for our basement: fitness, pets, decor and the mechanical room.",
    "items": [i.json() for i in items],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(pack, indent=1) + "\n", encoding="utf-8")
print(f"{len(items)} items, {sum(len(i.parts) for i in items)} parts -> {OUT}")
