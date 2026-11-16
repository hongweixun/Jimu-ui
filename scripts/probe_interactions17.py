# -*- coding: utf-8 -*-
"""第十八批（0.20.0）横切能力探针：v-longpress / v-copy / v-lazy / 组合式函数"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
fails = []
total = 0


def check(section, name, actual, expect):
    global total
    total += 1
    ok = actual == expect or (callable(expect) and expect(actual))
    if ok:
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False, default=str)[:100]}")
    else:
        fails.append(f"{section}/{name}")
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False, default=str)[:220]}, want {expect}")


def js(code, page=0):
    return tab.js(code.replace("__P__", "document.querySelectorAll('.demo-page')[" + str(page) + "]"))


def center(expr):
    """scrollIntoView 后返回元素中心坐标"""
    return js(
        "(()=>{const el=" + expr + ";if(!el)return null;el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return {x:r.left+r.width/2,y:r.top+r.height/2};})()"
    )


def mouse_press(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})


def mouse_move(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y, "button": "left"})


def mouse_release(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def touch_drag(x, y, dx, dy, steps=6, hold=0.03):
    tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
    for i in range(1, steps + 1):
        tab.send("Input.dispatchTouchEvent", {"type": "touchMove",
                 "touchPoints": [{"x": x + dx * i / steps, "y": y + dy * i / steps}]})
        time.sleep(hold)
    tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.35)


def press_button(text, page=0):
    js("(()=>{const b=[...__P__.querySelectorAll('button')].find(x=>x.textContent.trim().includes('"
       + text + "'));if(b){b.focus();b.click()}})()", page)


def wait_for(expr, timeout=6.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


ensure_edge()
tab = new_tab()
tab.send("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 1000, "deviceScaleFactor": 1, "mobile": False})
try:
    tab.send("Browser.grantPermissions", {"permissions": ["clipboardReadWrite", "clipboardSanitizedWrite"]})
except Exception:
    pass


def goto(path):
    tab.goto(BASE + path, wait=6)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")


# ================= v-longpress =================
goto("/components/long-press")
wait_for("__P__.querySelector('.lp-card')".replace("__P__", "document.querySelectorAll('.demo-page')[0]"))
time.sleep(1.2)
print("== long-press ==")

c1 = center("__P__.querySelector('.lp-card')")
mouse_press(c1["x"], c1["y"])
time.sleep(0.3)
pressing = js("__P__.querySelector('.lp-card').classList.contains('is-pressing')")
mouse_release(c1["x"], c1["y"])
time.sleep(0.4)
tip_e = js("__P__.querySelector('.demo-tip').textContent")
check("long-press", "pressing class during hold", pressing, True)
check("long-press", "early release does not trigger", "已长按" not in tip_e, True)

# move-cancel 在触发测试之前：tip 还是初始态，消极断言才可靠
c1c = center("__P__.querySelector('.lp-card')")
mouse_press(c1c["x"], c1c["y"])
mouse_move(c1c["x"] + 24, c1c["y"])
mouse_release(c1c["x"] + 24, c1c["y"])
time.sleep(0.8)
tip3 = js("__P__.querySelector('.demo-tip').textContent")
check("long-press", "move beyond tolerance cancels", "已长按" not in tip3, True)

c1b = center("__P__.querySelector('.lp-card')")
mouse_press(c1b["x"], c1b["y"])
time.sleep(0.65)
tip1 = js("__P__.querySelector('.demo-tip').textContent")
mouse_release(c1b["x"], c1b["y"])
time.sleep(0.4)
check("long-press", "500ms hold triggers", "已长按「书架卡片」" in tip1, True)

c2 = center("__P__.querySelector('.lp-card--alt')")
mouse_press(c2["x"], c2["y"])
time.sleep(1.35)
mouse_release(c2["x"], c2["y"])
time.sleep(0.5)
tip4 = js("__P__.querySelector('.demo-tip').textContent")
check("long-press", "custom 1200ms duration triggers", "已长按「慢速卡片」" in tip4, True)

# ================= v-copy =================
print("== copy ==")
goto("/components/copy")
wait_for("document.querySelectorAll('.demo-page')[0].querySelector('.copy-btn')")
time.sleep(1.2)

btn1 = center("__P__.querySelectorAll('.copy-btn')[0]")
mouse_press(btn1["x"], btn1["y"])
mouse_release(btn1["x"], btn1["y"])
time.sleep(0.6)
tip_c1 = js("__P__.querySelector('.demo-tip').textContent")
check("copy", "function-value copy succeeds", tip_c1, "已复制：JM20261116002")

clip = tab.js("navigator.clipboard ? navigator.clipboard.readText().catch(e=>'deny') : 'no-api'")
time.sleep(0.4)
check("copy", "clipboard content matches", clip, "JM20261116002")

btn2 = center("__P__.querySelectorAll('.copy-btn')[1]")
mouse_press(btn2["x"], btn2["y"])
mouse_release(btn2["x"], btn2["y"])
time.sleep(0.6)
# 字符串形式不带 onSuccess，tip 保持上一条；验证剪贴板内容本身
clip2 = tab.js("navigator.clipboard.readText().catch(e=>'deny')")
time.sleep(0.3)
check("copy", "string-value copy succeeds", clip2, "EDU-8F3K-2026")

# ================= v-lazy =================
print("== lazy ==")
goto("/components/lazy")
wait_for("document.querySelectorAll('.demo-page')[0].querySelectorAll('.course-card').length >= 6")
time.sleep(1.2)

def loaded_stats():
    return js("""(()=>{const imgs=[...__P__.querySelectorAll('img[data-jm-lazy]')];
      return {total:imgs.length, withSrc:imgs.filter(i=>i.getAttribute('src')).length,
        loadedTxt:[...__P__.querySelectorAll('.course-state')].filter(s=>s.textContent.includes('已加载')).length,
        comments:__P__.querySelector('.comment-title') ? __P__.querySelector('.comment-title').textContent : ''};})()""")

initial = loaded_stats()
check("lazy", "not all images load initially", initial["withSrc"] < initial["total"], True)
check("lazy", "visible images loaded", initial["withSrc"] >= 1, True)
check("lazy", "comments not loaded yet", initial["comments"], "")

# 滚动到最底（手机框内容器 .phone__content 才是真正的滚动容器）
js("""(()=>{const el=__P__.querySelector('.comment-zone');
  const box=el.closest('.phone__content')||el.closest('.demo__phone')||document.scrollingElement;
  box.scrollTop = box.scrollHeight;})()""")
time.sleep(1.5)
final = loaded_stats()
check("lazy", "all images loaded after scroll", final["withSrc"], final["total"])
check("lazy", "comment zone lazy content", final["comments"].startswith("课堂讨论（42"), True)

# ================= 组合式函数 =================
print("== composables ==")
goto("/components/composables")
wait_for("document.querySelectorAll('.demo-page')[0].querySelectorAll('button').length >= 3")
time.sleep(1.2)

# useCountDown
press_button("获取验证码")
time.sleep(0.5)
r0 = js("""(()=>{const b=[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('重发'));
  return {txt:b?b.textContent.trim():'', disabled:b?b.disabled:null,
    tip:[...__P__.querySelectorAll('.tip')][0].textContent};})()""")
check("count-down", "starts with 10s", r0["txt"], "重发（10s）")
check("count-down", "button disabled while running", r0["disabled"], True)
check("count-down", "tip updated", r0["tip"].startswith("验证码已发送"), True)
time.sleep(2.2)
r1 = js("(()=>{const b=[...document.querySelectorAll('.demo-page')[0].querySelectorAll('button')].find(b=>b.textContent.includes('重发'));return b?b.textContent.trim():''})()")
check("count-down", "remaining decreases", r1 in ("重发（8s）", "重发（7s）"), True)
time.sleep(8.5)
r2 = js("""(()=>{const b=[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('验证码')||b.textContent.includes('重发'));
  return {txt:b?b.textContent.trim():'', disabled:b?b.disabled:null,
    tip:[...__P__.querySelectorAll('.tip')][0].textContent};})()""")
check("count-down", "finish resets button", (r2["txt"], r2["disabled"]), ("获取验证码", False))
check("count-down", "onFinish fired", r2["tip"], "倒计时结束，可以重发了")

# useClickOutsideWhen
press_button("点外部收起")
time.sleep(0.5)
panel_open = js("__P__.querySelector('.panel') !== null")
check("click-outside", "panel opens", panel_open, True)
# 点面板外：第一行验证码 tip 在 root（第二个 row）之外
outside = center("__P__.querySelectorAll('.tip')[0]")
mouse_press(outside["x"], outside["y"])
mouse_release(outside["x"], outside["y"])
time.sleep(0.5)
panel_closed = js("__P__.querySelector('.panel') === null")
outside_tip = js("__P__.querySelectorAll('.tip')[1].textContent")
check("click-outside", "outside click closes", panel_closed, True)
check("click-outside", "handler fired", outside_tip, "已点外部收起")

# useSwipe
pad_c = center("__P__.querySelector('.pad')")
touch_drag(pad_c["x"], pad_c["y"], -80, 10)
swipe_tip = js("__P__.querySelectorAll('.tip')[2].textContent")
check("use-swipe", "horizontal swipe detected as left", swipe_tip, "滑动方向：left")
pad_c2 = center("__P__.querySelector('.pad')")
touch_drag(pad_c2["x"], pad_c2["y"], 5, 4, steps=2)
swipe_tip2 = js("__P__.querySelectorAll('.tip')[2].textContent")
check("use-swipe", "tiny move not a swipe", swipe_tip2, "位移不够，不算滑动")

# 防抖 vs 节流
for _ in range(6):
    press_button("连点试试")
    time.sleep(0.06)
counts_fast = js("""(()=>{const tips=[...__P__.querySelectorAll('.tip')].find(t=>t.textContent.includes('原始点击'));
  const m=tips.textContent.match(/原始点击 (\\d+) 次 · 防抖只记 (\\d+) · 节流 (\\d+)/);
  return {raw:+m[1], debounce:+m[2], throttle:+m[3]};})()""")
check("debounce-throttle", "raw clicks counted", counts_fast["raw"], 6)
check("debounce-throttle", "debounce suppresses during rapid", counts_fast["debounce"], 0)
check("debounce-throttle", "throttle keeps sampling", counts_fast["throttle"], lambda v: 1 <= v <= 3)
time.sleep(0.7)
counts_late = js("""(()=>{const tips=[...__P__.querySelectorAll('.tip')].find(t=>t.textContent.includes('原始点击'));
  const m=tips.textContent.match(/防抖只记 (\\d+)/); return +m[1];})()""")
check("debounce-throttle", "debounce fires once after stop", counts_late, 1)

# 全局错误
check("global", "no page errors", tab.js("JSON.stringify(window.__errs)"), "[]")

print()
print("total=%d fail=%d" % (total, len(fails)))
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL PASS")
