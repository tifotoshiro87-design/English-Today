# -*- coding: utf-8 -*-
"""fetch_podcast.py - Lấy 2 video mới nhất của 3 kênh YouTube, ghi ra data/podcasts.json.
Dùng RSS công khai của YouTube, chỉ cần thư viện chuẩn của Python (không cần API key, không cần pip)."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

VN = timezone(timedelta(hours=7))
THU_MUC = Path(__file__).parent / "data"
THU_MUC.mkdir(exist_ok=True)
FILE = THU_MUC / "podcasts.json"
SO_VIDEO = 2
KENH = [("unleashed", "@EnglishPodcastUnleashed"),
        ("basic", "@BasicEnglishStudio"),
        ("speakupp", "@SpeakUppEnglish")]
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}


def tai(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9",
                                                "Cookie": "CONSENT=YES+1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def tim_id_kenh(handle):
    html = tai(f"https://www.youtube.com/{handle}").decode("utf-8", "replace")
    for mau in (r'channel_id=(UC[\w-]{22})', r'"channelId":"(UC[\w-]{22})"', r'"externalId":"(UC[\w-]{22})"'):
        m = re.search(mau, html)
        if m:
            return m.group(1)
    raise ValueError("Không tìm thấy mã kênh")


def doc_rss(xml_bytes):
    cay = ET.fromstring(xml_bytes)
    ds = []
    for e in cay.findall("a:entry", NS)[:SO_VIDEO]:
        vid = e.findtext("yt:videoId", default="", namespaces=NS)
        if not vid:
            continue
        ds.append({"title": (e.findtext("a:title", default="", namespaces=NS) or "").strip(),
                   "url": f"https://www.youtube.com/watch?v={vid}",
                   "thumb": f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg",
                   "date": (e.findtext("a:published", default="", namespaces=NS) or "")[:10]})
    return ds


def main():
    try:
        cu = {c["key"]: c for c in json.loads(FILE.read_text(encoding="utf-8")).get("channels", [])}
    except (OSError, ValueError):
        cu = {}
    ket_qua = []
    for key, handle in KENH:
        c = cu.get(key, {"key": key, "handle": handle, "id": None, "items": []})
        try:
            if not c.get("id"):
                c["id"] = tim_id_kenh(handle)
            items = doc_rss(tai(f"https://www.youtube.com/feeds/videos.xml?channel_id={c['id']}"))
            if items:
                c["items"] = items
            c["error"] = None
            print("OK ", key, len(items), "video")
        except Exception as e:  # noqa: BLE001 - lỗi mạng thì giữ danh sách cũ, không làm hỏng app
            c["error"] = f"{type(e).__name__}: {e}"
            print("LỖI", key, c["error"])
        ket_qua.append(c)
    FILE.write_text(json.dumps({"fetched_at": datetime.now(VN).strftime("%Y-%m-%d %H:%M"), "channels": ket_qua},
                               ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
