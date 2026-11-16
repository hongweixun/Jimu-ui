"""VirtualList 动态行高回归：逐行测量 / 无重叠 / 滚动锚定 / 跳行与跳底 / 固定行高不回归。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
ensure_edge()
tab = new_tab()
ok = fail = 0


def check(section, name, actual, expect):
    global ok, fail
    good = (
        actual == expect
        or (isinstance(expect, tuple) and actual in expect)
        or (callable(expect) and expect(actual))
    )
    if good:
        ok += 1
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False)[:120]}")
    else:
        fail += 1
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False)[:220]}, want {expect}")


DYNAMIC_LIST = "document.querySelector('.chat-stage__list')"
ROWS = f"[...{DYNAMIC_LIST}.querySelectorAll('.jm-virtual-list__item')]"

# 读取渲染窗口的几何：data-index / 行高 / transform 里的 y / 相对视口的 top
GEOM = f"""{ROWS}.map(el => {{
  const m = el.style.transform.match(/translateY\\(([-\\d.]+)px/);
  return {{
    i: Number(el.dataset.index),
    y: m ? +m[1] : 0,
    h: Math.round(el.getBoundingClientRect().height),
    top: Math.round(el.getBoundingClientRect().top - {DYNAMIC_LIST}.getBoundingClientRect().top),
  }};
}})"""


def overlaps(rows):
    """相邻两行：上一行的底不能超过下一行的顶（留 1px 容差给亚像素）"""
    bad = []
    for a, b in zip(rows, rows[1:]):
        if a["y"] + a["h"] > b["y"] + 1:
            bad.append((a["i"], b["i"], a["y"] + a["h"], b["y"]))
    return bad


tab.goto(f"{BASE}/components/virtual-list", wait=4)
time.sleep(1.2)

# ---------- 渲染与测量 ----------
check("dyn", "dynamic demo exists", tab.js(
    f"!!{DYNAMIC_LIST}"
), True)

rows = tab.js(GEOM)
check("dyn", "only visible rows rendered", len(rows), lambda n: 0 < n <= 20)
check("dyn", "row heights differ (content driven)", len({r["h"] for r in rows}), lambda n: n >= 3)
check("dyn", "no vertical overlap", overlaps(rows), [])
check("dyn", "positions follow measured heights", rows[1]["y"], lambda v: abs(v - rows[0]["h"]) <= 1)

content_h = tab.js(
    f"parseFloat({DYNAMIC_LIST}.querySelector('.jm-virtual-list__content').style.height)"
)
# 300 条、估值 64 = 19200；实测行高普遍更矮/更高，总高应已按实测重算
check("dyn", "content height recomputed after measure", content_h, lambda v: 12000 < v < 40000)
check("dyn", "content height is integer-ish", content_h % 1, 0)

scroll_h = tab.js(f"{DYNAMIC_LIST}.scrollHeight")
check("dyn", "scroller height matches content", scroll_h, lambda v: abs(v - content_h) <= 2)

# ---------- 跳行：居中对齐 ----------
tab.js("[...document.querySelectorAll('.demo-page .jm-button')].find(b=>b.textContent.includes('第 151 条居中')).click()")
time.sleep(0.9)
rows = tab.js(GEOM)
mid = [r for r in rows if r["i"] == 150]
check("dyn", "scrollToIndex(150) renders target", len(mid), 1)
if mid:
    view_h = tab.js(f"{DYNAMIC_LIST}.clientHeight")
    center_off = mid[0]["top"] + mid[0]["h"] / 2 - view_h / 2
    check("dyn", "target centered in viewport", round(center_off), lambda v: abs(v) <= 24)
check("dyn", "no overlap after jump", overlaps(rows), [])
check("dyn", "jump lands near index 150 (overscan above)", rows[0]["i"], lambda v: 140 <= v <= 146)

# ---------- 滚动锚定：上方行重测后目标行不漂移 ----------
before = [r for r in tab.js(GEOM) if r["i"] == 150]
time.sleep(0.8)
after = [r for r in tab.js(GEOM) if r["i"] == 150]
check("dyn", "anchor row stays put after re-measure", (before[0]["top"] if before else None), after[0]["top"] if after else None)

# ---------- 跳到底：末条可见、底部无空洞 ----------
tab.js("[...document.querySelectorAll('.demo-page .jm-button')].find(b=>b.textContent.includes('跳到最新')).click()")
time.sleep(0.9)
rows = tab.js(GEOM)
check("dyn", "last item rendered", rows[-1]["i"], 299)
tail_gap = tab.js(f"""(function() {{
  const el = {DYNAMIC_LIST};
  const last = [...el.querySelectorAll('.jm-virtual-list__item')].pop();
  const content = el.querySelector('.jm-virtual-list__content');
  const contentBottom = content.getBoundingClientRect().bottom;
  return Math.round(contentBottom - Math.min(last.getBoundingClientRect().bottom, contentBottom));
}})()""")
check("dyn", "content bottom <= last item bottom (no empty tail)", tail_gap, lambda v: v <= 2)
bottom_scroll_h = tab.js(f"{DYNAMIC_LIST}.scrollHeight")
check("dyn", "no overlap at bottom", overlaps(rows), [])
# 「到底」的实用标准：最后一条完整落在视口里（末尾还在陆续测量，总高微涨，scrollTop 不必死贴 contentHeight）
last_bottom = tab.js(
    "(function(){const el=" + DYNAMIC_LIST + ";"
    "const items=el.querySelectorAll('.jm-virtual-list__item');"
    "const last=items[items.length-1];"
    "return Math.round(last.getBoundingClientRect().bottom-el.getBoundingClientRect().top);})()"
)
check(
    "dyn",
    "last item fully visible at bottom",
    last_bottom,
    lambda v: 0 < v <= tab.js(f"{DYNAMIC_LIST}.clientHeight") + 2,
)

# ---------- 固定行高模式不受影响 ----------
fixed = "document.querySelectorAll('.demo-page')[0].querySelector('.jm-virtual-list')"
tab.js(f"{fixed}.scrollTop = 0")
time.sleep(0.4)
fixed_rows = tab.js(f"""[...{fixed}.querySelectorAll('.jm-virtual-list__item')].map(el => {{
  const m = el.style.transform.match(/translateY\\(([-\\d.]+)px/);
  return {{ y: m ? +m[1] : 0, h: Math.round(el.getBoundingClientRect().height) }};
}})""")
check("fixed", "still 56px rows", sorted({r["h"] for r in fixed_rows}), [56])
check("fixed", "still 56px stride", sorted({r["y"] % 56 for r in fixed_rows}), [0])
check("fixed", "content height unchanged", tab.js(
    f"{fixed}.querySelector('.jm-virtual-list__content').style.height"
), "112000px")


# ---------- PhotoWall 虚拟渲染 ----------
tab.goto(f"{BASE}/components/photo-wall", wait=4)
# 首访该页时 Vite 需要冷编译新 demo（virtual.vue），轮询等它出现，别用固定 sleep
for _ in range(30):
    if tab.js("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('1200 张'))"):
        break
    time.sleep(0.5)
time.sleep(0.8)

demo_v = "[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('1200 张'))"
vwall = "document.querySelectorAll('.jm-photo-wall')[3]"

check("vw", "virtual demo exists", tab.js(f"!!{demo_v}"), True)
check("vw", "small wall mounts all 12", tab.js(
    "document.querySelectorAll('.jm-photo-wall')[0].querySelectorAll('.jm-photo-wall__item').length"
), 12)

mounted_small = tab.js(f"{vwall}.querySelectorAll('.jm-photo-wall__item').length")
check("vw", "1200-item wall mounts far fewer", mounted_small, lambda n: 0 < n <= 60)
wall_h = tab.js(f"parseFloat({vwall}.style.height)")
check("vw", "wall height reflects full layout", wall_h, lambda v: 100000 < v < 160000)

# 滚动翻页：挂载窗口随可视带移动
tab.js(f"{demo_v}.scrollIntoView({{block:'start'}})")
time.sleep(0.5)
def scroll_and_probe(delta):
    tab.js(f"""(() => {{
      const c = {demo_v}.closest('.phone__content') || document.scrollingElement;
      const top = {demo_v}.getBoundingClientRect().top - c.getBoundingClientRect().top + c.scrollTop;
      c.scrollTop = top + {delta};
    }})()""")
    time.sleep(0.4)
    return tab.js(f"[...{vwall}.querySelectorAll('.jm-photo-wall__item')].slice(0,1).map(i=>Number(i.dataset.uid))[0]")

first1 = scroll_and_probe(0)
first2 = scroll_and_probe(20000)
first3 = scroll_and_probe(110000)
check("vw", "mounted window follows scroll", (first1, first2, first3), lambda v: v[0] < 15 and 150 < v[1] < 400 and v[2] > 900)
check("vw", "still small DOM deep in list", tab.js(f"{vwall}.querySelectorAll('.jm-photo-wall__item').length"), lambda n: n <= 60)
check("vw", "no empty wall", tab.js(f"{vwall}.querySelectorAll('.jm-photo-wall__item').length") > 0, True)

# 关掉虚拟渲染：1200 张全挂载
tab.js(f"{demo_v}.querySelector('.jm-switch').click()")
time.sleep(1.2)
check("vw", "switch off mounts all", tab.js(f"{vwall}.querySelectorAll('.jm-photo-wall__item').length"), 1200)

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(0 if fail == 0 else 1)
