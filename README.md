# Our Home 3D

Our own copy of [NeonPlan 3D](https://github.com/Mastershort/neonplan3d) (v3.4.3, MIT licensed) for our Home Assistant,
with furniture made for our house. Everything NeonPlan 3D does stays: the editor, the 3D view, walking through the
model, live lights, media, climate, sensors and cameras, the dashboard card and Assist questions.

All credit for the original goes to Mastershort. This copy is not affiliated with or supported by them; please don't
report problems with it to the NeonPlan 3D project.

## What is different from NeonPlan 3D

- **Its own name and domain:** `ourhome3d` (panel "Our Home 3D" at `/ourhome3d`, card `custom:ourhome3d-card`), so
  NeonPlan 3D updates never overwrite it.
- **Built-in furniture:** every pack file in `custom_components/ourhome3d/furniture/` loads at start-up without a
  shop signature, because it ships with the code. These files may only hold furniture (no Pro features and no module
  code). Packs imported from a file still need a valid signature, as in NeonPlan 3D.
- **Our basement pack** (`ourhome.basement`): treadmill, wire dog crate, raised dog cots, dog bed, printer, standing and
  wall mirrors, vanity light, shelf floor lamp, speaker stands, air purifier, wall ledge, helmet shelves, bat display
  case, wall flags, stacked photo frames, air handler with plenum, water softener, electrical panel, steel support
  post, steel I-beam, HVAC duct trunk, storage boxes and suitcases.

The version in `manifest.json` stays at the NeonPlan release it is based on (3.4.3), because the frontend checks it
against its own version.

## Install

Settings → Marketplace → ⋮ → Custom repositories → add this repository as an *Integration*, install **Our Home 3D**,
restart Home Assistant, then add the integration under Settings → Devices & services.

To bring a NeonPlan 3D plan over: NeonPlan 3D → Editor → Settings → Backup → Export, then the same place in Our Home 3D
→ Import.

## Adding or changing furniture

Furniture is written in metres in `tools/build_furniture.py`:

```
python3 tools/build_furniture.py   # writes custom_components/ourhome3d/furniture/ourhome_basement.json
python3 tools/check_furniture.py   # checks ids, ranges and colours against the pack schema
```

Raise `release` in the pack when items change, commit, update the integration in the Marketplace and restart.
Each part is a `box`, `cyl` (cylinder) or `loft` (a block whose top can be smaller or shifted); colours are `#rrggbb`
or a palette role (`wood`, `fabric`, `white`, `metal`, `dark`, `glass`, ...) that follows the chosen look.

## Updating from NeonPlan 3D

New NeonPlan 3D releases are not picked up automatically. To take one over: check out the new release of
`Mastershort/neonplan3d`, copy `custom_components/neonplan3d` over `custom_components/ourhome3d`, run
`tools/rename.py` on it, and re-apply the built-in furniture loader (`load_builtin_packs` in `packs.py` and its two
uses in `storage.py`). Keep `furniture/` and the manifest fields.

## Licence

MIT, see [LICENSE](LICENSE). Original code © 2026 Mastershort.
