import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"

ensure_edge()
tab = new_tab()

PAGES = {
    "grid": [
        ("count", "document.querySelectorAll('.jm-grid').length"),
        ("cols", "getComputedStyle(document.querySelector('.jm-grid')).gridTemplateColumns"),
        ("itemW", "Math.round(document.querySelector('.jm-grid__item').getBoundingClientRect().width)"),
        ("squareRatio", "(()=>{const el=[...document.querySelectorAll('.jm-grid')][1].querySelector('.jm-grid__item');const r=el.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]})()"),
        ("badge", "document.querySelector('.jm-grid__badge')?.textContent"),
    ],
    "image": [
        ("imgs", "document.querySelectorAll('.jm-image').length"),
        ("loaded", "[...document.querySelectorAll('.jm-image__img')].filter(i=>i.complete&&i.naturalWidth>0).length"),
        ("errText", "document.querySelector('.jm-image__error .jm-image__tip')?.textContent"),
        ("sizes", "[...document.querySelectorAll('.jm-image')].slice(0,4).map(e=>{const r=e.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)})"),
    ],
    "swipe": [
        ("slides", "document.querySelectorAll('.jm-swipe__slide').length"),
        ("dots", "document.querySelectorAll('.jm-swipe')[0].querySelectorAll('.jm-swipe__dot').length"),
        ("track", "document.querySelector('.jm-swipe__track')?.style.transform"),
        ("heights", "[...document.querySelectorAll('.jm-swipe')].map(e=>Math.round(e.getBoundingClientRect().height))"),
    ],
    "picker": [
        ("cells", "document.querySelectorAll('.jm-cell').length"),
        ("openBtn", "!!document.querySelector('.jm-cell.is-clickable')"),
    ],
    "uploader": [
        ("items", "document.querySelectorAll('.jm-uploader__item').length"),
        ("triggers", "document.querySelectorAll('.jm-uploader__trigger').length"),
        ("thumbsOk", "[...document.querySelectorAll('.jm-uploader__thumb')].filter(i=>i.complete&&i.naturalWidth>0).length"),
    ],
    "pull-refresh": [
        ("roots", "document.querySelectorAll('.jm-pull-refresh').length"),
        ("head", "document.querySelector('.jm-pull-refresh__text')?.textContent"),
        ("scrollerH", "Math.round(document.querySelector('.scroller').getBoundingClientRect().height)"),
    ],
    "list": [
        ("rows", "document.querySelectorAll('.jm-list .row').length"),
        ("placeholder", "document.querySelector('.jm-list__placeholder')?.textContent?.trim()"),
        ("sentinel", "!!document.querySelector('.jm-list__sentinel')"),
    ],
}

for page, exprs in PAGES.items():
    print("=" * 20, page)
    tab.goto(f"{BASE}/components/{page}", wait=3.0)
    for name, expr in exprs:
        try:
            print(f"  {name}: {json.dumps(tab.js(expr), ensure_ascii=False)}")
        except Exception as e:
            print(f"  {name}: ERR {e}")
    tab.shot(rf"E:\jimu-ui\scripts\shots\{page}.png")

print("title:", tab.js("document.title"))
tab.ws.close()
