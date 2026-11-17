"""Renames a copy of custom_components/neonplan3d to ourhome3d (domain, panel, paths, websocket commands, brand).

Keeps links to mastershort.de and the NeonPlan GitHub project, and the shop fingerprint. Usage: python3 tools/rename.py DIR
"""
import re, os, sys
root = sys.argv[1]
pat = re.compile(r'(?<!https://)(?<!mastershort\.de/)(?<!/en/)(?<!astershort/)neonplan3d')
brand = re.compile(r'NeonPlan 3D')
counts = {}
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        if not f.endswith(('.py', '.js', '.json', '.yaml', '.yml', '.md', '.txt', '.html', '.css', '.mjs')):
            continue
        s = open(p, encoding='utf-8').read()
        o = s
        s = s.replace('f"neonplan3d:{instance_id}"', 'f"@@KEEPFP@@:{instance_id}"')
        s = pat.sub('ourhome3d', s)
        s = s.replace('@@KEEPFP@@', 'neonplan3d')
        s = brand.sub('Our Home 3D', s)
        s = s.replace('f"NeonPlan3D/{', 'f"OurHome3D/{')
        # its own element names, so it never borrows NeonPlan's components when both are loaded
        s = s.replace('fp3d-', 'oh3d-').replace('fp3dReloadSent', 'oh3dReloadSent')
        if s != o:
            counts[p] = (len(pat.findall(o)), len(brand.findall(o)))
            open(p, 'w', encoding='utf-8').write(s)
for dp, dn, fn in os.walk(root):
    for f in fn:
        if 'neonplan3d' in f:
            os.rename(os.path.join(dp, f), os.path.join(dp, f.replace('neonplan3d', 'ourhome3d')))
print(len(counts), 'files changed')
for k, v in sorted(counts.items()):
    print(v, k.replace(root, ""))
