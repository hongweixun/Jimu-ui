#!/usr/bin/env python3
"""第 21 批（0.23.0）探针：Rate 半星 / Tooltip·Popover 方位 / Pagination 重叠 /
Steps 当前步 / Collapse 圆角 / Form 控件整合 / Scanner 按钮文字对比度"""
import json
import sys
import time

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


def wait_for(expr, timeout=8.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


def js(code, page=0):
    return tab.js(code.replace("__P__", "document.querySelectorAll('.demo-page')[" + str(page) + "]"))


def rect(expr):
    raw = js(
        "(()=>{const el=" + expr + ";if(!el)return 'null';"
        "el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return JSON.stringify({l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height});})()",
    )
    if not isinstance(raw, str):
        print("  [dbg] rect error:", raw)
        return None
    return json.loads(raw)


def mouse_move(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})


def mouse_click(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def click_center(expr, page=0, retries=3):
    """点击元素中心；合成事件偶发首丢，失败自动重试"""
    for _ in range(retries):
        p = rect(expr) if isinstance(expr, str) else expr
        if not p:
            time.sleep(0.4)
            continue
        mouse_click(int(p["l"] + p["w"] / 2), int(p["t"] + p["h"] / 2))
        return p
    return None


# ================= Rate 半星 =================
print("== rate ==")
goto("/components/rate")
wait_for("[...document.querySelectorAll('.jm-rate')].some(r=>r.querySelector('.jm-rate__hit--half'))")

R = tab.js("[...document.querySelectorAll('.jm-rate')].findIndex(r=>r.querySelector('.jm-rate__hit--half'))")
print("  [dbg] allow-half rate idx:", R)


def rate_click(frac, retries=4):
    """点第 1 颗星的水平位置 frac∈(0,1)，返回 aria-valuenow"""
    for _ in range(retries):
        p = rect("document.querySelectorAll('.jm-rate')[" + str(R) + "].querySelector('.jm-rate__item')")
        if not p:
            time.sleep(0.3)
            continue
        mouse_click(int(p["l"] + p["w"] * frac), int(p["t"] + p["h"] / 2))
        time.sleep(0.25)
        v = js("document.querySelectorAll('.jm-rate')[" + str(R) + "].getAttribute('aria-valuenow')", 0)
        if v not in (None, "", "3.5"):
            return v
        time.sleep(0.3)
    return v


v_half = rate_click(0.25)
check("rate", "half star clickable -> 0.5", v_half, "0.5")
v_full = rate_click(0.75)
check("rate", "full star clickable -> 1", v_full, "1")

# ================= Tooltip left / right =================
print("== tooltip ==")
goto("/components/tooltip")
wait_for("[...document.querySelectorAll('.jm-tooltip')].some(t=>t.textContent.includes('left'))")
time.sleep(1.2)

for label, place in (("left", "is-left"), ("right", "is-right")):
    idx = tab.js(
        "[...document.querySelectorAll('.jm-tooltip')].findIndex(t=>{"
        "const b=t.querySelector('.jm-button');"
        "return b && b.textContent.trim()==='" + label + "'})"
    )
    ref = rect(f"document.querySelectorAll('.jm-tooltip')[{idx}]")
    mouse_move(int(ref["l"] + ref["w"] / 2), int(ref["t"] + ref["h"] / 2))
    ok = wait_for(f"document.querySelectorAll('.jm-tooltip')[{idx}].querySelector('.jm-tooltip__panel')", 4)
    time.sleep(0.4)
    panel = rect(f"document.querySelectorAll('.jm-tooltip')[{idx}].querySelector('.jm-tooltip__panel')")
    if place == "is-left":
        # 面板在触发器左侧，间距 ≈ 8px；垂直中心对齐
        check("tooltip", "left: panel on the left side", panel["r"] <= ref["l"] - 4, True)
        check("tooltip", "left: gap ≈ 8px", round(ref["l"] - panel["r"]), 8)
        check("tooltip", "left: vertically centered", abs((panel["t"] + panel["h"] / 2) - (ref["t"] + ref["h"] / 2)) < 15, True)
    else:
        check("tooltip", "right: panel on the right side", panel["l"] >= ref["r"] - 4, True)
        check("tooltip", "right: gap ≈ 8px", round(panel["l"] - ref["r"]), 8)
        check("tooltip", "right: vertically centered", abs((panel["t"] + panel["h"] / 2) - (ref["t"] + ref["h"] / 2)) < 15, True)
    mouse_move(5, 5)
    time.sleep(0.4)

# ================= Popover 宽度与方位 =================
print("== popover ==")
goto("/components/popover")
wait_for("[...document.querySelectorAll('.jm-popover')].some(p=>p.textContent.includes('下'))")
time.sleep(1.2)

P = tab.js("[...document.querySelectorAll('.jm-popover')].findIndex(p=>p.textContent.includes('下'))")
click_center(rect(f"document.querySelectorAll('.jm-popover')[{P}].querySelector('.jm-popover__reference')"))
ok = wait_for(f"document.querySelectorAll('.jm-popover')[{P}].querySelector('.jm-popover__panel')", 4)
time.sleep(0.3)
# 面板与触发器在同一次求值里测量，避免 scrollIntoView 造成的位移偏差
ppref = js(
    "(()=>{const p=document.querySelectorAll('.jm-popover')[" + str(P) + "];"
    "const rr=p.querySelector('.jm-popover__reference').getBoundingClientRect();"
    "const pr=p.querySelector('.jm-popover__panel');if(!pr)return 'null';"
    "const pp=pr.getBoundingClientRect();"
    "return JSON.stringify({refB:rr.bottom,refL:rr.left,refR:rr.right,refT:rr.top,panT:pp.top,panL:pp.left,panR:pp.right,panW:pp.width,panH:pp.height});})()"
)
pp = json.loads(ppref)
check("popover", "panel rendered", ok, True)
check("popover", "long content not squeezed into one column", pp["panW"] > 140, True)
check("popover", "text flows horizontally (w > h)", pp["panW"] > pp["panH"], True)
check("popover", "bottom placement below reference", pp["panT"] >= pp["refB"] + 6, True)
mouse_click(5, 5)
time.sleep(0.4)

# ================= Pagination 无重叠 =================
# 移动端组件按手机宽度测：桌面窗口太窄时 flex-wrap 换行会让不同行的元素水平重叠，属于误判
print("== pagination ==")
tab.send("Emulation.setDeviceMetricsOverride", {"width": 400, "height": 780, "deviceScaleFactor": 1, "mobile": True})
goto("/components/pagination")
wait_for("document.querySelectorAll('.jm-pagination').length >= 2")
time.sleep(1.2)

overlap = js("""(()=>{
  let bad=[];
  document.querySelectorAll('.jm-pagination').forEach((nav,i)=>{
    const pages=[...nav.querySelectorAll('.jm-pagination__page,.jm-pagination__more')];
    const prev=nav.querySelector('.jm-pagination__prev');
    const next=nav.querySelector('.jm-pagination__next');
    const hit=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left);
    pages.forEach(p=>{
      if(hit(p.getBoundingClientRect(),next?.getBoundingClientRect())) bad.push(i+':next/'+p.textContent.trim());
      if(hit(p.getBoundingClientRect(),prev?.getBoundingClientRect())) bad.push(i+':prev/'+p.textContent.trim());
    });
  });
  return JSON.stringify(bad);
})()""")
check("pagination", "no overlap between arrows and page numbers", json.loads(overlap), [])
tab.send("Emulation.clearDeviceMetricsOverride")

# ================= Steps 当前步样式 =================
print("== steps ==")
goto("/components/steps")
wait_for("document.querySelectorAll('.jm-step.is-process').length >= 1")
time.sleep(1.0)

st = js("""(()=>{
  const d=document.querySelector('.jm-step.is-process .jm-step__dot');
  const c=getComputedStyle(d);
  return JSON.stringify({bg:c.backgroundColor,color:c.color,radius:c.borderRadius,shadow:c.boxShadow});
})()""")
s = json.loads(st)
check("steps", "process dot filled with primary", s["bg"], "rgb(0, 160, 233)")
check("steps", "process number is white", s["color"], "rgb(255, 255, 255)")
check("steps", "process dot keeps soft glow ring", s["shadow"] not in ("none", ""), True)

# ================= Collapse 圆角 / 去边框 =================
print("== collapse ==")
goto("/components/collapse")
wait_for("document.querySelectorAll('.jm-collapse.is-round').length >= 2")
time.sleep(1.0)

col = js("""(()=>{
  const c1=document.querySelector('.jm-collapse.is-round:not(.is-border)');
  const c2=document.querySelector('.jm-collapse.is-round.is-border');
  const s1=getComputedStyle(c1), s2=getComputedStyle(c2);
  return JSON.stringify({
    r1: s1.borderTopLeftRadius, bt1: s1.borderTopWidth, sh1: s1.boxShadow,
    r2: s2.borderTopLeftRadius, bt2: s2.borderTopWidth,
    legacy: (()=>{const l=[...document.querySelectorAll('.jm-collapse')].find(x=>!x.classList.contains('is-round'));
      const v=getComputedStyle(l); return v.borderTopWidth+'/'+v.borderTopLeftRadius;})(),
  });
})()""")
c = json.loads(col)
check("collapse", "round card default radius 12px", c["r1"], "12px")
check("collapse", "borderless: no top border", c["bt1"], "0px")
check("collapse", "borderless: card shadow", c["sh1"] not in ("none", ""), True)
check("collapse", "round=10 -> 10px radius", c["r2"], "10px")
check("collapse", "round+border -> full outline 1px", c["bt2"], "1px")
check("collapse", "legacy style untouched (default border, no radius)", c["legacy"], "1px/0px")

# ================= Form 控件整合演示 =================
print("== form controls ==")
goto("/components/form")
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.querySelector('.jm-radio-group')&&p.querySelector('.jm-uploader'))", 12)
F = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelector('.jm-radio-group')&&p.querySelector('.jm-uploader'))")
print("  [dbg] controls page:", F)

fc = js("""JSON.stringify({
  radios: __P__.querySelectorAll('.jm-radio').length,
  checks: __P__.querySelectorAll('.jm-checkbox').length,
  rate: !!__P__.querySelector('.jm-rate'),
  stepper: !!__P__.querySelector('.jm-stepper'),
  sw: !!__P__.querySelector('.jm-switch'),
  up: !!__P__.querySelector('.jm-uploader'),
  ta: !!__P__.querySelector('.jm-input__textarea, textarea'),
  cell: !!__P__.querySelector('.jm-cell'),
})""", F)
f = json.loads(fc)
check("form", "radio group rendered", f["radios"] >= 3, True)
check("form", "checkbox group rendered", f["checks"] >= 4, True)
check("form", "rate rendered", f["rate"], True)
check("form", "stepper rendered", f["stepper"], True)
check("form", "switch rendered", f["sw"], True)
check("form", "uploader rendered", f["up"], True)
check("form", "textarea rendered", f["ta"], True)
check("form", "picker trigger cell rendered", f["cell"], True)

# 点城市 Cell → 底部弹层 Picker 出现
cell_sel = f"document.querySelectorAll('.demo-page')[{F}].querySelector('.jm-cell')"
click_center(cell_sel)
ok = wait_for(f"document.querySelectorAll('.demo-page')[{F}].querySelector('.jm-popup')", 4)
time.sleep(0.5)
picker = js(f"document.querySelectorAll('.demo-page')[{F}].querySelector('.jm-popup .jm-picker') ? 1 : 0", F)
check("form", "city popup opens picker", picker, 1)
tab.js(
    "(()=>{const p=document.querySelectorAll('.demo-page')[" + str(F) + "];"
    "const opts=[...p.querySelectorAll('.jm-picker-column__item')];"
    "const t=opts.find(o=>o.textContent.includes('杭州'));"
    "if(t){t.dispatchEvent(new MouseEvent('click',{bubbles:true}));}"
    "return opts.length;})()"
)
time.sleep(0.4)
conf = js(
    "(()=>{const p=document.querySelectorAll('.demo-page')[" + str(F) + "];"
    "const btn=[...p.querySelectorAll('.jm-picker button,.jm-popup button')].find(b=>b.textContent.includes('确认'));"
    "if(btn){btn.dispatchEvent(new MouseEvent('click',{bubbles:true}));return true;}return false;})()"
)
time.sleep(0.5)
city = js(
    "(()=>{const p=document.querySelectorAll('.demo-page')[" + str(F) + "];"
    "const c=p.querySelector('.jm-cell .jm-cell__value,.jm-cell [class*=value]');"
    "return c?c.textContent.trim():'';})()"
)
check("form", "picker confirm fills city", "杭州" in city, True)

# ================= Scanner 按钮对比度 =================
print("== scanner ==")
goto("/components/scanner")
wait_for("document.querySelectorAll('.jm-scanner').length >= 2")
time.sleep(1.0)

sc = js("getComputedStyle(document.querySelector('.demo-page .btn')).color")
check("scanner", "demo button text is white", sc, "rgb(255, 255, 255)")

# ================= 汇总 =================
print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
