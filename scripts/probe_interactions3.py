"""第五批组件（Icon/Space/Layout/Avatar/SwipeCell/Slider/DropdownMenu）交互回归。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
results = []


def check(name, desc, actual, expect):
    ok = actual == expect
    results.append((name, desc, ok, actual, expect))
    print(("PASS" if ok else "FAIL"), name, "-", desc, "" if ok else f"\n   actual={actual!r} expect={expect!r}")


def dispatch(tab, sel, event, x=None, y=None):
    box = tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(!e) return null; const r=e.getBoundingClientRect();"
        f"return {{x:r.left+r.width/2, y:r.top+r.height/2}}}})()"
    )
    if not box:
        return
    opts = {"bubbles": True, "pointerId": 1, "isPrimary": True,
            "clientX": x if x is not None else box["x"],
            "clientY": y if y is not None else box["y"]}
    tab.js(f"document.querySelector({json.dumps(sel)}).dispatchEvent("
           f"new PointerEvent({json.dumps(event)}, {json.dumps(opts)}))")


def drag(tab, sel, dx, dy=0, steps=8):
    box = tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(!e) return null; const r=e.getBoundingClientRect();"
        f"return {{x:r.left+r.width/2, y:r.top+r.height/2}}}})()"
    )
    if not box:
        return
    dispatch(tab, sel, "pointerdown")
    for i in range(1, steps + 1):
        dispatch(tab, sel, "pointermove", box["x"] + dx * i / steps, box["y"] + dy * i / steps)
        time.sleep(0.015)
    dispatch(tab, sel, "pointerup")


def click(tab, sel):
    tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(e) e.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))}})()"
    )


def px(v):
    try:
        return float(str(v).split("(")[1].split("px")[0])
    except Exception:
        return 0.0


ensure_edge()
tab = new_tab()

# ---------- Icon ----------
tab.goto(f"{BASE}/components/icon", wait=3)
check("icon", "svg 渲染", tab.js("document.querySelectorAll('.jm-icon').length") > 30, True)
check("icon", "path 按 d 渲染",
      tab.js("document.querySelector('.jm-icon').querySelectorAll('path').length") >= 1, True)
check("icon", "自定义 school 已注册",
      tab.js("[...document.querySelectorAll('.jm-icon')].some(i=>i.querySelectorAll('path').length===2)"), True)

# ---------- Space ----------
tab.goto(f"{BASE}/components/space", wait=3)
gap = tab.js("getComputedStyle(document.querySelectorAll('.jm-space')[0]).gap")
check("space", "默认间距 8px", gap, "8px")
between = tab.js("getComputedStyle(document.querySelectorAll('.jm-space')[5]).justifyContent")
check("space", "justify between", between, "space-between")

# ---------- Layout ----------
tab.goto(f"{BASE}/components/layout", wait=3)
w24 = tab.js("document.querySelectorAll('.jm-col')[0].getBoundingClientRect().width")
w12 = tab.js("document.querySelectorAll('.jm-col')[1].getBoundingClientRect().width")
check("layout", "span12 是 span24 的一半", round(w12 * 2), round(w24))

# ---------- Avatar ----------
tab.goto(f"{BASE}/components/avatar", wait=3)
check("avatar", "头像组 max=4 折叠", tab.js("document.querySelectorAll('.jm-avatar-group .jm-avatar').length"), 4)
check("avatar", "+N 兜底", tab.js("document.querySelector('.jm-avatar-group__rest')?.textContent"), "+3")
check("avatar", "图片头像已渲染", tab.js("document.querySelectorAll('.jm-avatar__img').length"), 3)

# ---------- SwipeCell ----------
tab.goto(f"{BASE}/components/swipe-cell", wait=3)
root_sel = ".jm-swipe-cell__track"
dispatch(tab, root_sel, "pointerdown")
for i in range(1, 9):
    box = tab.js("(()=>{const e=document.querySelector('.jm-swipe-cell__track');const r=e.getBoundingClientRect();return {x:r.left+r.width/2, y:r.top+r.height/2}})()")
    dispatch(tab, root_sel, "pointermove", box["x"] - i * 25, box["y"])
    time.sleep(0.02)
dispatch(tab, root_sel, "pointerup")
time.sleep(0.5)
raw_off = tab.js("document.querySelector('.jm-swipe-cell__track').style.getPropertyValue('--jm-swipe-cell-offset')")
off = float(str(raw_off).replace('px', '') or 0)
check("swipe-cell", "拖动后展开（位移为负）", off < -30, True)
rows_before = tab.js("document.querySelectorAll('.jm-swipe-cell').length")
# 真实点击会先触发 pointerdown（在这里重置滑动标记），再触发 click
dispatch(tab, ".jm-swipe-cell__side--right .btn--danger", "pointerdown")
click(tab, ".jm-swipe-cell__side--right .btn--danger")
time.sleep(0.4)
rows_after = tab.js("document.querySelectorAll('.jm-swipe-cell').length")
check("swipe-cell", "删除按钮生效", rows_after, rows_before - 1)

# ---------- Slider ----------
tab.goto(f"{BASE}/components/slider", wait=3)
label0 = tab.js("document.body.innerText.match(/基础：(\\d+)/)?.[1]")
drag(tab, ".jm-slider", 60, 0)
label1 = tab.js("document.body.innerText.match(/基础：(\\d+)/)?.[1]")
check("slider", "拖动改值", label1 != label0, True)
rect = tab.js("(()=>{const t=document.querySelectorAll('.jm-slider')[0].querySelector('.jm-slider__track');const r=t.getBoundingClientRect();return {l:r.left, w:r.width}})()")
dispatch(tab, ".jm-slider", "pointerdown", rect["l"] + rect["w"] * 0.8, 0)
dispatch(tab, ".jm-slider", "pointerup", rect["l"] + rect["w"] * 0.8, 0)
time.sleep(0.2)
check("slider", "点轨道跳到 80", int(label1 and tab.js("document.body.innerText.match(/基础：(\\d+)/)?.[1]") or 0) == 80, True)
range_txt = tab.js("document.body.innerText.match(/双滑块：(\\d+) ~ (\\d+)/)")
check("slider", "双滑块渲染两个按钮",
      tab.js("document.querySelectorAll('.jm-slider')[1].querySelectorAll('.jm-slider__button').length"), 2)

# ---------- DropdownMenu ----------
tab.goto(f"{BASE}/components/dropdown-menu", wait=3)
click(tab, ".jm-dropdown-item__title")
time.sleep(0.4)
panel_h = tab.js("document.querySelector('.jm-dropdown-item__panel')?.getBoundingClientRect().height ?? 0")
check("dropdown", "展开后面板可见", panel_h > 100, True)
option_cnt = tab.js("document.querySelectorAll('.jm-dropdown-item__option').length")
check("dropdown", "选项数量", option_cnt, 5)
click(tab, ".jm-dropdown-item__option:nth-child(2)")
time.sleep(0.4)
check("dropdown", "选中后标题同步", "一年级" in str(tab.js("document.querySelector('.jm-dropdown-item__text')?.textContent")), True)
check("dropdown", "选中后面板收起",
      tab.js("document.querySelector('.jm-dropdown-item__panel') === null"), True)

print()
fails = [r for r in results if not r[2]]
print(f"== {len(results) - len(fails)}/{len(results)} 通过 ==")
for r in fails:
    print("FAILED:", r[0], "-", r[1], "actual:", r[3], "expect:", r[4])
