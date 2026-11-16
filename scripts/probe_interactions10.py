"""PhotoWall 照片墙交互回归：瀑布流布局 / 响应式列数 / 懒加载 / 预览 / 长按拖拽。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
ensure_edge()
tab = new_tab()
ok = fail = 0


def check(page, name, actual, expect):
    global ok, fail
    good = (
        actual == expect
        or (isinstance(expect, tuple) and actual in expect)
        or (callable(expect) and expect(actual))
    )
    if good:
        ok += 1
        print(f"  PASS {page}/{name}: {json.dumps(actual, ensure_ascii=False)[:110]}")
    else:
        fail += 1
        print(f"  FAIL {page}/{name}: got {json.dumps(actual, ensure_ascii=False)[:220]}, want {expect}")


def page(has_text):
    return (
        f"[...document.querySelectorAll('.demo-page')]"
        f".find(p=>p.textContent.includes('{has_text}'))"
    )


def wall_of(has_text, index=0):
    return f"{page(has_text)}.querySelectorAll('.jm-photo-wall')[{index}]"


def slots(sel):
    return tab.js(
        f"[...{sel}.querySelectorAll('.jm-photo-wall__item')].map(i=>{{"
        f"const m=i.style.transform.match(/translate3d\\(([-\\d.]+)px,\\s*([-\\d.]+)px/);"
        f"return {{x:m?+m[1]:0,y:m?+m[2]:0,w:parseFloat(i.style.width),h:parseFloat(i.style.height)}}}})"
    )


def touch_drag(x, y, dx, dy, steps=8, hold=0.03, press=0.45):
    tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
    time.sleep(press)  # 等长按激活
    for i in range(1, steps + 1):
        tab.send(
            "Input.dispatchTouchEvent",
            {"type": "touchMove", "touchPoints": [{"x": x + dx * i / steps, "y": y + dy * i / steps}]},
        )
        time.sleep(hold)
    tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.5)


# ---------------- 布局 ----------------
tab.goto(f"{BASE}/components/photo-wall", wait=4)
time.sleep(1)

check("wall", "four walls on page", tab.js("document.querySelectorAll('.jm-photo-wall').length"), 4)
check("wall", "first three item counts", tab.js(
    "[...document.querySelectorAll('.jm-photo-wall')].slice(0,3)"
    ".map(w=>w.querySelectorAll('.jm-photo-wall__item').length)"
), [12, 6, 6])

s1 = slots(wall_of("瀑布流 + 响应式"))
check("wall", "2 columns in 308px container", tab.js(
    f"new Set({json.dumps(s1)}.map(s=>s.x)).size"
), 2)
check("wall", "column width fills container", tab.js(
    f"{wall_of('瀑布流 + 响应式')}.clientWidth"
), lambda v: abs(s1[0]["w"] * 2 + 8 - v) <= 2)
check("wall", "first item at origin", (s1[0]["x"], s1[0]["y"]), (0, 0))
check("wall", "second item in other column", s1[1]["x"] > s1[0]["x"] and s1[1]["y"] == 0, True)

# 无重叠：任意两格矩形不相交
overlap = tab.js(
    f"(()=>{{const S={json.dumps(s1)};for(let i=0;i<S.length;i++)for(let j=i+1;j<S.length;j++){{"
    f"const a=S[i],b=S[j];if(a.x<b.x+b.w-1&&b.x<a.x+a.w-1&&a.y<b.y+b.h-1&&b.y<a.y+a.h-1)return [i,j]}}return null}})()"
)
check("wall", "no overlapping cells", overlap, None)
check("wall", "wall height covers lowest cell", tab.js(
    f"{wall_of('瀑布流 + 响应式')}.style.height.replace('px','')|0"
), lambda v: abs(v - max(s["y"] + s["h"] for s in s1)) <= 2)

# 第 5 张没有 ratio：滚入视口、图片加载后应按 naturalHeight/Width 测量（480/360=1.333）
tab.js(f"{wall_of('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__item')[4].scrollIntoView({{block:'center'}})")
for _ in range(20):
    ready = tab.js(
        f"(()=>{{const it={wall_of('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__item')[4];"
        f"const img=it.querySelector('img');return img && img.complete && img.naturalHeight>0}})()"
    )
    if ready:
        break
    time.sleep(0.15)
time.sleep(0.4)
measured = tab.js(
    f"{wall_of('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__item')[4].style.height.replace('px','')|0"
)
check("wall", "ratio auto measured after load", measured, lambda v: abs(v - s1[4]["w"] * 480 / 360) <= 2)

# 响应式：容器从 308 拉宽到 500，2 列应自动变 3 列
tab.js(f"{page('瀑布流 + 响应式')}.style.width='500px'")
time.sleep(0.5)
s1b = slots(wall_of("瀑布流 + 响应式"))
check("wall", "columns respond to resize", tab.js(f"new Set({json.dumps(s1b)}.map(s=>s.x)).size"), 3)
tab.js(f"{page('瀑布流 + 响应式')}.style.width=''")
time.sleep(0.4)

# ---------------- 懒加载 ----------------
# 只数第一个 demo：新增的 1200 张虚拟 demo 会污染全局计数
total = tab.js(f"{page('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__item').length")
initial = tab.js(f"{page('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__img').length")
check("wall", "lazy: fewer images than items initially", initial, lambda v: 0 < v < total)
check("wall", "lazy: placeholders rendered", tab.js(
    f"{page('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__ph').length > 0"
), True)
tab.js(f"{page('瀑布流 + 响应式')}.closest('.phone__content').scrollTop = 99999")
time.sleep(0.9)
final = tab.js(f"{page('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__img').length")
check("wall", "lazy: more images after scrolling", final > initial, True)

# ---------------- 预览 ----------------
tab.js(f"{wall_of('瀑布流 + 响应式')}.querySelector('.jm-photo-wall__item').click()")
time.sleep(0.6)
check("preview", "opens inside phone frame", tab.js(
    "(()=>{const p=document.querySelector('.jm-image-preview');if(!p)return null;"
    "return p.classList.contains('is-inline')&&!!p.closest('[data-jm-preview-scope]')})()"
), True)
check("preview", "index shows 1 / 12", tab.js(
    "document.querySelector('.jm-image-preview__index')?.textContent"
), "1 / 12")
tab.js("document.querySelector('.jm-image-preview__close')?.click()")
time.sleep(0.4)
check("preview", "closes on button", tab.js("!document.querySelector('.jm-image-preview')"), True)

# 键盘打开预览
tab.js(f"{{const el={wall_of('瀑布流 + 响应式')}.querySelectorAll('.jm-photo-wall__item')[2];el.focus()}}")
tab.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
tab.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
time.sleep(0.5)
check("preview", "opens via keyboard Enter", tab.js(
    "document.querySelector('.jm-image-preview__index')?.textContent"
), "3 / 12")
tab.js("document.querySelector('.jm-image-preview__close')?.click()")
time.sleep(0.4)

# ---------------- 拖拽排序 ----------------
wall3 = wall_of("长按 0.3 秒拿起")
tab.js(f"{wall3}.scrollIntoView({{block:'center'}})")
time.sleep(0.3)
order_before = tab.js(f"[...{wall3}.querySelectorAll('.jm-photo-wall__item')].map(i=>i.querySelector('img')?.alt)")
box = tab.js(f"(()=>{{const r={wall3}.getBoundingClientRect();return {{x:r.left,y:r.top,w:r.width,h:r.height}}}})()")
first = tab.js(f"{wall3}.querySelector('.jm-photo-wall__item').style.transform")

# 长按第一张，拖到最底部 → 应落到最后一格
touch_drag(box["x"] + box["w"] * 0.35, box["y"] + box["h"] * 0.08, 0, box["h"] * 0.82, steps=10)
order_after = tab.js(f"[...{wall3}.querySelectorAll('.jm-photo-wall__item')].map(i=>i.querySelector('img')?.alt)")
check("drag", "order changed by drag", order_after[0] != order_before[0] and order_after[-1] == order_before[0], True)
check("drag", "sort state updated", tab.js(
    f"{page('长按 0.3 秒拿起')}.querySelector('.state__last').textContent"
), "第 1 张 → 第 6 位")
check("drag", "items written back to model", tab.js(
    f"{page('长按 0.3 秒拿起')}.querySelector('.state p').textContent.replace(/\\s+/g,'')"
).startswith("当前顺序：2"), True)
check("drag", "drag does not open preview", tab.js("!document.querySelector('.jm-image-preview')"), True)
check("drag", "dragged item settles into slot", tab.js(
    f"[...{wall3}.querySelectorAll('.jm-photo-wall__item')].map(i=>i.style.transform)"
), lambda v: all("scale" not in t for t in v))

# 短按（未长按）应视为点击 → 打开预览
tab.js(f"{wall3}.scrollIntoView({{block:'center'}})")
box = tab.js(f"(()=>{{const r={wall3}.getBoundingClientRect();return {{x:r.left,y:r.top,w:r.width,h:r.height}}}})()")
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": box["x"] + box["w"] * 0.35, "y": box["y"] + box["h"] * 0.1}]})
time.sleep(0.06)
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.6)
check("drag", "short tap still opens preview", tab.js(
    "document.querySelector('.jm-image-preview__index')?.textContent"
), lambda v: isinstance(v, str) and v.endswith("/ 6"))
tab.js("document.querySelector('.jm-image-preview__close')?.click()")
time.sleep(0.4)

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(1 if fail else 0)
