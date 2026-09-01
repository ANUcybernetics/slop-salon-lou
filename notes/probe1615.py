import sys, json
sys.path.insert(0, "/home/sprite/slop-salon-lou/notes")
from cf_walk_fast import walk
res = walk(16, 15, 60000, collect=[1251, 2502, 2500, 2501, 2503, 2504])
print("records:", res["records"], flush=True)
for t in [1251, 2500, 2501, 2502, 2503, 2504]:
    s = res["strikes"].get(t, [])
    print(f"  {t}: {len(s)} strikes, first {s[0] if s else '-'}", flush=True)
