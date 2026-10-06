# -*- coding: utf-8 -*-
"""Them bai hoc moi vao data/. Dung: python tools/add_lessons.py bai_moi.json
bai_moi.json = danh sach (list) cac bai, moi bai co id dang B1-SOCIAL-006, level, topic, n, ...
Chi ghi them vao file cua dung cap-chu de, tu cap nhat data/meta.json va CAPNHAT.md. Khong dong vao index.html."""
import json, sys, datetime
from pathlib import Path
R = Path(__file__).resolve().parent.parent
new = json.load(open(sys.argv[1], encoding="utf-8"))
meta = json.load(open(R/"data/meta.json", encoding="utf-8"))
have = set()
for f in meta["files"]:
    have |= {x["id"] for x in json.load(open(R/f"data/lessons/{f}.json", encoding="utf-8"))}
touched = []
for l in new:
    assert l["id"] not in have, "Trung id: " + l["id"]
    k = l["level"] + "-" + l["topic"]
    p = R/f"data/lessons/{k}.json"
    arr = json.load(open(p, encoding="utf-8")) if p.exists() else []
    arr.append(l); arr.sort(key=lambda x: x["n"])
    json.dump(arr, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    if k not in meta["files"]: meta["files"].append(k); meta["files"].sort()
    have.add(l["id"]); touched.append(l["id"])
json.dump(meta, open(R/"data/meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = {}
for f in meta["files"]:
    lv = f.split("-")[0]; tot[lv] = tot.get(lv, 0) + len(json.load(open(R/f"data/lessons/{f}.json", encoding="utf-8")))
with open(R/"CAPNHAT.md", "a", encoding="utf-8") as fh:
    fh.write(f"- {datetime.date.today()}: them {', '.join(touched)} -> tong {tot}\n")
print("OK", touched, tot)
