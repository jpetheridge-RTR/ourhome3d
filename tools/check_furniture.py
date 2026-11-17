"""Checks the furniture files against the pack schema limits (a stand-in for packs.validate_payload, which needs
voluptuous): ids, ranges, part counts, colours, mounts. Run: python3 tools/check_furniture.py"""
import json, re, sys
from pathlib import Path

ID = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,39}$")
COL = re.compile(r"^#[0-9a-fA-F]{6}$")
ROLES = {"body", "fabric", "cushion", "wood", "white", "metal", "dark", "glass", "plant", "pot", "accent"}
PART_KEYS = {"shape", "x", "z", "w", "d", "y", "h", "color", "top", "edges", "glow", "screen", "tx", "tz", "tw", "td",
             "axis", "rot", "fix", "advent", "spin", "bind"}
ITEM_KEYS = {"id", "name", "size", "electric", "mount", "wall_y", "surface", "vehicle", "hole", "light", "parts",
             "symbol", "group", "room", "tags", "family", "variant", "slots"}
errs = []
for path in sorted(Path(__file__).resolve().parents[1].glob("custom_components/ourhome3d/furniture/*.json")):
    pack = json.loads(path.read_text())
    assert pack["format"] == "fp3dpack" and pack["version"] == 1 and ID.match(pack["id"])
    assert not pack.get("features") and not pack.get("module") and pack.get("instance") is None
    ids = set()
    for it in pack["items"]:
        e = lambda m: errs.append(f"{path.name}:{it['id']}: {m}")
        if set(it) - ITEM_KEYS: e(f"unknown keys {set(it) - ITEM_KEYS}")
        if not ID.match(it["id"]) or it["id"] in ids: e("bad/duplicate id")
        ids.add(it["id"])
        if not all(0.01 <= v <= 10 for v in it["size"]) or len(it["size"]) != 3: e("size")
        if it.get("mount", "floor") not in ("floor", "surface", "wall", "ceiling"): e("mount")
        if not 0 <= it.get("wall_y", 1) <= 3: e("wall_y")
        for k in ("group", "family"):
            if k in it and not ID.match(it[k]): e(k)
        for r in it.get("room", []):
            if not ID.match(r): e("room")
        if not 1 <= len(it["parts"]) <= 60: e(f"{len(it['parts'])} parts")
        for i, p in enumerate(it["parts"]):
            pe = lambda m: e(f"part {i}: {m}")
            if set(p) - PART_KEYS: pe(f"keys {set(p) - PART_KEYS}")
            if p["shape"] not in ("box", "cyl", "loft"): pe("shape")
            for k in ("x", "z", "tx", "tz"):
                if k in p and not -0.5 <= p[k] <= 0.5: pe(f"{k}={p[k]}")
            for k in ("w", "d", "h", "tw", "td"):
                if k in p and not 0.001 <= p[k] <= 1: pe(f"{k}={p[k]}")
            if not 0 <= p["y"] <= 1: pe(f"y={p['y']}")
            if p["y"] + p["h"] > 1.0001: pe(f"y+h={p['y'] + p['h']:.3f} > 1")
            for k in ("color", "top"):
                if k in p and not (COL.match(p[k]) or p[k] in ROLES): pe(f"{k}={p[k]}")
            if "fix" in p and not re.match(r"^[wdh]{1,3}$", p["fix"]): pe("fix")
            if "edges" in p and p["edges"] not in (True, False, "glow", "faint"): pe("edges")
    print(f"{path.name}: {len(pack['items'])} items checked")
print("\n".join(errs) or "no problems")
sys.exit(1 if errs else 0)
