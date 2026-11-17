"""Re-stamps the lazily loaded bundles: each `./ourhome3d-<part>.js?v=<hash>` reference gets the first 12 hex digits
of the SHA-256 of that file, as NeonPlan's build does, so browsers never keep a stale copy after a change.
Usage: python3 tools/restamp.py [custom_components/ourhome3d/frontend]"""
import hashlib, re, sys
from pathlib import Path

d = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "custom_components/ourhome3d/frontend")
files = sorted(d.glob("ourhome3d*.js"))
ref = re.compile(r"\./(ourhome3d-[a-z0-9-]+\.js)\?v=[0-9a-f]+")
for _ in range(10):
    digest = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:12] for f in files}
    changed = False
    for f in files:
        s = f.read_text(encoding="utf-8")
        n = ref.sub(lambda m: f"./{m.group(1)}?v={digest[m.group(1)]}" if m.group(1) in digest else m.group(0), s)
        if n != s:
            f.write_text(n, encoding="utf-8")
            changed = True
    if not changed:
        break
for f in files:
    print(f.name, hashlib.sha256(f.read_bytes()).hexdigest()[:12])
