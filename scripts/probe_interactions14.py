"""图片预览手势回归：双击缩放 / 双指捏合 / 放大后平移 / 边界回弹 / 翻页仍正常 / 键盘缩放 / 关闭复位。"""
import json
import re
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


def scale_of():
    """读当前图片的计算后 transform 里的缩放系数（matrix(a,b,c,d,e,f) 的 a）"""
    # 只给当前页的 img 绑了 inline transform，用它定位「正在显示的那张」
    v = tab.js(
        "(()=>{const imgs=[...document.querySelectorAll('.jm-image-preview__img')];"
        "const img=imgs.find(i=>i.style.transform)||imgs[0];if(!img)return null;"
        "const t=getComputedStyle(img).transform;"
        "if(!t||t==='none')return 1;const m=t.match(/matrix\\(([-\\d.e]+)/);return m?+m[1]:1})()"
    )
    return round(v, 2) if isinstance(v, (int, float)) else v


def translate_of():
    v = tab.js(
        "(()=>{const imgs=[...document.querySelectorAll('.jm-image-preview__img')];"
        "const img=imgs.find(i=>i.style.transform)||imgs[0];if(!img)return null;"
        "const m=getComputedStyle(img).transform.match(/matrix\\([^)]*\\)/);"
        "if(!m)return [0,0];const p=m[0].slice(7,-1).split(',').map(Number);return [Math.round(p[4]),Math.round(p[5])]})()"
    )
    return v


def idx():
    return tab.js("document.querySelector('.jm-image-preview__index')?.textContent.trim()")


def touch(points, type_):
    tab.send(
        "Input.dispatchTouchEvent",
        {
            "type": type_,
            "touchPoints": [{"x": p[0], "y": p[1], "id": i} for i, p in enumerate(points)],
        },
    )


def tap(x, y, gap=0.09):
    touch([(x, y)], "touchStart")
    time.sleep(0.05)
    touch([], "touchEnd")
    time.sleep(gap)


def double_tap(x, y):
    tap(x, y, gap=0.06)
    tap(x, y, gap=0.1)
    time.sleep(0.45)


def open_preview():
    tab.js(
        "(()=>{const it=document.querySelector('.jm-photo-wall__item');it.focus();it.click()})()"
    )
    time.sleep(0.8)


# ============================ 打开 ============================
tab.goto(f"{BASE}/components/photo-wall", wait=4)
time.sleep(1.6)
open_preview()
check("zoom", "preview opened", idx(), "1 / 12")
check("zoom", "starts at scale 1", scale_of(), 1)

box = tab.js(
    "(()=>{const r=document.querySelector('.jm-image-preview').getBoundingClientRect();"
    "return {x:r.left,y:r.top,w:r.width,h:r.height}})()"
)
cx = box["x"] + box["w"] / 2
cy = box["y"] + box["h"] / 2

# ============================ 双击 ============================
double_tap(cx, cy)
check("zoom", "double tap zooms to 2.5x", scale_of(), lambda v: abs(v - 2.5) <= 0.05)
check("zoom", "zoomed image marked", tab.js(
    "document.querySelectorAll('.jm-image-preview__img.is-zoomed').length"
), 1)
check("zoom", "double tap does not switch page", idx(), "1 / 12")

double_tap(cx, cy)
check("zoom", "double tap again resets to 1x", scale_of(), 1)

# 第二次双击是"复位"，不能顺带把预览关掉（旧实现里第一次点击会立刻 close）
check("zoom", "double tap keeps preview open", tab.js(
    "!!document.querySelector('.jm-image-preview')"
), True)

# ============================ 双指捏合 ============================
touch([(cx - 40, cy), (cx + 40, cy)], "touchStart")
time.sleep(0.12)
for step in range(1, 7):
    d = 40 + step * 18
    touch([(cx - d, cy), (cx + d, cy)], "touchMove")
    time.sleep(0.05)
touch([], "touchEnd")
time.sleep(0.5)
pinched = scale_of()
check("zoom", "pinch zooms in", pinched, lambda v: 1.6 < v <= 4.0)

# 放大后单指拖动 = 平移，不翻页
before_t = translate_of()
touch([(cx, cy)], "touchStart")
for step in range(1, 6):
    touch([(cx - step * 14, cy - step * 6)], "touchMove")
    time.sleep(0.05)
touch([], "touchEnd")
time.sleep(0.45)
after_t = translate_of()
check("zoom", "drag pans while zoomed", after_t != before_t, True)
check("zoom", "pan does not switch page", idx(), "1 / 12")
check("zoom", "pan stays within bounds", tab.js(
    "(()=>{const imgs=[...document.querySelectorAll('.jm-image-preview__img')];"
    "const img=imgs.find(i=>i.style.transform)||imgs[0];"
    "const r=img.getBoundingClientRect();const p=document.querySelector('.jm-image-preview').getBoundingClientRect();"
    "return Math.round(r.left)-Math.round(p.left)<=1 && Math.round(r.right)>=Math.round(p.right)-1})()"
), True)

# 双击复位后，左右滑动手势恢复
double_tap(cx, cy)
check("zoom", "reset before swipe", scale_of(), 1)
touch([(cx + 90, cy)], "touchStart")
for step in range(1, 7):
    touch([(cx + 90 - step * 30, cy)], "touchMove")
    time.sleep(0.05)
touch([], "touchEnd")
time.sleep(0.6)
check("zoom", "swipe still switches after reset", idx(), "2 / 12")
check("zoom", "new page starts unzoomed", scale_of(), 1)

# ============================ 键盘缩放 ============================
tab.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "=", "code": "Equal", "windowsVirtualKeyCode": 187})
tab.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "=", "code": "Equal", "windowsVirtualKeyCode": 187})
time.sleep(0.45)
check("zoom", "keyboard + zooms", scale_of(), lambda v: v > 1.2)
tab.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "0", "code": "Digit0", "windowsVirtualKeyCode": 48})
tab.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "0", "code": "Digit0", "windowsVirtualKeyCode": 48})
time.sleep(0.45)
check("zoom", "keyboard 0 resets", scale_of(), 1)

# ============================ 关闭复位 ============================
double_tap(cx, cy)
check("zoom", "zoomed again before close", scale_of(), lambda v: v > 2)
tab.js("document.querySelector('.jm-image-preview__close').click()")
time.sleep(0.7)
open_preview()
check("zoom", "reopen starts at 1x", scale_of(), 1)
check("zoom", "reopen starts at first page", idx(), "1 / 12")

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(0 if fail == 0 else 1)
