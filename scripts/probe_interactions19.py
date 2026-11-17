#!/usr/bin/env python3
"""第 20 批（0.22.0）探针：Scanner 扫描线形态 / Uploader banner / 安全区 / Tooltip PC 长按"""
import sys
import time
import json

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab  # noqa: E402

ensure_edge()
tab = new_tab()
tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})

passed = 0
failed = []


def check(group, name, got, want):
    global passed
    ok = got == want
    if ok:
        passed += 1
        print(f"  PASS {group}/{name}")
    else:
        failed.append(f"{group}/{name}")
        print(f"  FAIL {group}/{name}: got {got!r}, want {want!r}")


def goto(path):
    tab.goto("http://localhost:5173" + path, wait=6)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")


def wait_for(expr, timeout=6.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


def js(code, page=0):
    return tab.js(code.replace("__P__", "document.querySelectorAll('.demo-page')[" + str(page) + "]"))


def center(expr, page=0):
    return js(
        "(()=>{const el=" + expr + ";if(!el)return null;"
        "el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return {x:r.left+r.width/2,y:r.top+r.height/2};})()",
        page,
    )


def mouse_press(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})


def mouse_release(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def mouse_click(x, y):
    mouse_press(x, y)
    mouse_release(x, y)


# ================= Scanner 扫描线形态 =================
print("== scanner ==")
goto("/components/scanner")
wait_for("document.querySelectorAll('.jm-scanner').length >= 2")
time.sleep(1.5)

r = js("""(async()=>{
  const sc=document.querySelector('.jm-scanner');
  if(!sc) return {err: 'no scanner'};
  const line=sc.querySelector('.jm-scanner__line');
  const before=getComputedStyle(line,'::before');
  const after=getComputedStyle(line,'::after');
  // 采样拖尾 transform 两个半周期
  const vals=new Set();
  for(let i=0;i<14;i++){ vals.add(after.transform); await new Promise(r2=>setTimeout(r2,150)); }
  return {
    lineBg: before.backgroundImage || before.background,
    lineFilter: before.filter,
    tailAnim: after.animationName,
    tailMoved: vals.size>1,
    nVals: vals.size,
  }
})()""")
if "err" in r:
    print("  [dbg] scanner err:", r)
    sys.exit(1)
check("scanner", "line has horizontal edge fade", "linear-gradient(90deg" in (r["lineBg"] or ""), True)
check("scanner", "line uses drop-shadow glow", "drop-shadow" in (r["lineFilter"] or ""), True)
check("scanner", "tail follows direction", r["tailAnim"], "jm-scanner-tail")
check("scanner", "tail flips between half cycles", r["tailMoved"], True)
print("  [dbg] tail nVals:", r.get("nVals"))

# ================= Uploader banner =================
print("== uploader banner ==")
goto("/components/uploader")
wait_for("document.querySelectorAll('.jm-uploader-banner').length >= 1", 12)
B = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelector('.jm-uploader-banner'))")
print("  [dbg] banner page:", B)
time.sleep(1.5)

# demo 里第二个 banner（photoFiles 预置 1 张）→ 计数与文件行
banners = js("""JSON.stringify({
  n: __P__.querySelectorAll('.jm-uploader-banner').length,
  titles: [...__P__.querySelectorAll('.jm-uploader-banner__title')].map(e=>e.textContent.trim()),
  descs: [...__P__.querySelectorAll('.jm-uploader-banner__desc')].map(e=>e.textContent.trim()),
  counts: [...__P__.querySelectorAll('.jm-uploader-banner__count')].map(e=>e.textContent.trim()),
  rows: __P__.querySelectorAll('.jm-uploader-list__row').length,
})""", B)
b = json.loads(banners)
check("uploader", "banner cards rendered", b["n"], 2)
check("uploader", "banner titles", b["titles"], ["上传证书图片", "上传现场照片"])
check("uploader", "banner desc only on first", b["descs"], ["支持 JPG / PNG / PDF，可拍照上传"])
check("uploader", "count badge shows 1/5", any("1/5" in c for c in b["counts"]), True)
check("uploader", "file row rendered for prefilled item", b["rows"] >= 1, True)

# banner 点击 → 触发文件选择（input.click 不弹窗但会派发 change 目标；这里只验证点击可达 + 无报错）
c = center("__P__.querySelectorAll('.jm-uploader-banner')[0]", B)
mouse_click(c["x"], c["y"])
time.sleep(0.4)
check("uploader", "banner click no error", js("JSON.stringify(window.__errs)"), "[]")

# 删除预置文件行 → 计数消失（0 个时不渲染计数）
c2 = center("__P__.querySelectorAll('.jm-uploader-list__row')[0]", B)
mouse_click(c2["x"] + (c2["x"] and 0), c2["y"])  # 点缩略图避免误触
time.sleep(0.3)
delbtn = center("__P__.querySelectorAll('.jm-uploader-list__del')[0]", B)
mouse_click(delbtn["x"], delbtn["y"])
time.sleep(0.5)
rows_after = js("__P__.querySelectorAll('.jm-uploader-list__row').length", B)
check("uploader", "banner file row deletable", rows_after, 0)

# ================= 安全区 =================
print("== safe area ==")
goto("/components/safe-area")
wait_for("document.querySelectorAll('.jm-safe-spacer').length >= 2")
time.sleep(1.5)

r = js("""JSON.stringify({
  spacers: __P__.querySelectorAll('.jm-safe-spacer').length,
  h1: __P__.querySelectorAll('.jm-safe-spacer')[0].getBoundingClientRect().height,
  cls: __P__.querySelectorAll('.jm-safe-spacer')[0].className,
  bg: getComputedStyle(__P__.querySelectorAll('.jm-safe-spacer')[0]).backgroundColor,
  padClsExists: [...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>r.selectorText==='.jm-safe-pad-bottom')}catch(e){return false}}),
})""")
s = json.loads(r)
check("safe-area", "spacers rendered", s["spacers"], 2)
check("safe-area", "min-height fallback 20px", s["h1"], 20)
check("safe-area", "spacer class", s["cls"], "jm-safe-spacer is-bottom")
check("safe-area", "custom background", s["bg"], "rgb(247, 248, 250)")
check("safe-area", "utility class .jm-safe-pad-bottom registered", s["padClsExists"], True)

# Popup 底部弹层 safe-area 类仍在（回归确认）
goto("/components/popup")
wait_for("document.querySelectorAll('.jm-popup').length >= 1 || document.querySelectorAll('.demo-page').length >= 1")
time.sleep(1)
check("safe-area", "popup page reachable", js("window.__errs===undefined || window.__errs.length"), 0)

# ================= Tooltip PC 鼠标长按 =================
print("== tooltip pc ==")
goto("/components/tooltip")
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('长按这行字'))")
time.sleep(1.5)

# 找到「长按这行字」所在的 jm-tooltip，按住鼠标 600ms
pos = None
for pg in range(3):
    pos = center("[...__P__.querySelectorAll('.jm-tag')].find(t=>t.textContent.includes('长按这行字'))", pg)
    if pos:
        break
check("tooltip", "longpress target found", bool(pos), True)
if pos:
    mouse_press(pos["x"], pos["y"])
    time.sleep(0.65)
    opened = js("""(()=>{const tip=[...document.querySelectorAll('.jm-tooltip')].find(t=>t.textContent.includes('长按这行字'));
      return tip && tip.classList.contains('is-open');})()""")
    mouse_release(pos["x"], pos["y"])
    time.sleep(2.0)  # auto-hide-delay 1.6s
    closed = js("""(()=>{const tip=[...document.querySelectorAll('.jm-tooltip')].find(t=>t.textContent.includes('长按这行字'));
      return tip.classList.contains('is-open');})()""")
    check("tooltip", "PC mouse long-press opens", opened, True)
    check("tooltip", "auto hide after release", closed, False)

# 快速点击不应触发长按（<450ms 松手）
if pos:
    mouse_press(pos["x"], pos["y"])
    time.sleep(0.15)
    mouse_release(pos["x"], pos["y"])
    time.sleep(0.5)
    opened2 = js("""(()=>{const tip=[...document.querySelectorAll('.jm-tooltip')].find(t=>t.textContent.includes('长按这行字'));
      return tip.classList.contains('is-open');})()""")
    check("tooltip", "quick click does not trigger", opened2, False)

# ================= 汇总 =================
print(f"== total={passed + len(failed)} fail={len(failed)} ==")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
