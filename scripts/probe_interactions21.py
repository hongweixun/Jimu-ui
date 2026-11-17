#!/usr/bin/env python3
"""第 22 批（0.24.0）探针：Form 上传器整行布局 / Descriptions 间距 /
Popover 视口回移 / Pagination 分级 / Ellipsis / Video"""
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
    raw = tab.js(
        "(()=>{const el=" + expr + ";if(!el)return 'null';"
        "el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return JSON.stringify({l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height});})()"
    )
    if not isinstance(raw, str):
        print("  [dbg] rect error:", raw)
        return None
    return json.loads(raw)


def mouse_click(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def click_center(p):
    mouse_click(int(p["l"] + p["w"] / 2), int(p["t"] + p["h"] / 2))


# ================= Form 上传器整行布局 =================
print("== form uploader ==")
goto("/components/form")
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.querySelector('.jm-radio-group')&&p.querySelector('.jm-uploader'))", 12)
F = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelector('.jm-radio-group')&&p.querySelector('.jm-uploader'))")

fu = js("""(()=>{
  const up=__P__.querySelector('.jm-uploader');
  const trig=up.querySelector('.jm-uploader__trigger');
  const value=up.closest('.jm-form-item__value');
  const trigR=trig.getBoundingClientRect();
  return JSON.stringify({trigW:Math.round(trigR.width), valueFull:value.getBoundingClientRect().width>240});
})()""", F)
f = json.loads(fu)
check("form", "uploader cell not squeezed (>=55px)", f["trigW"] >= 55, True)
check("form", "uploader value row takes full width", f["valueFull"], True)

# ================= Descriptions 间距 =================
print("== descriptions ==")
goto("/components/descriptions")
wait_for("document.querySelectorAll('.jm-descriptions').length >= 1")
time.sleep(1.0)

de = js("""(()=>{
  const d=document.querySelector('.jm-descriptions:not(.is-border)');
  const c=getComputedStyle(d);
  const cell=getComputedStyle(d.querySelector('.jm-descriptions__cell'));
  return JSON.stringify({rowGap:c.rowGap, padY:cell.paddingTop});
})()""")
d = json.loads(de)
check("descriptions", "row-gap 10px", d["rowGap"], "10px")
check("descriptions", "cell padding-y 10px", d["padY"], "10px")

# ================= Popover 视口回移 =================
print("== popover clamp ==")
goto("/components/popover")
wait_for("[...document.querySelectorAll('.jm-popover')].some(p=>p.textContent.includes('下'))")
time.sleep(1.2)

# 缩到手机视口宽度：面板居中在贴近边缘的按钮上，不回移必然越界
tab.send("Emulation.setDeviceMetricsOverride", {"width": 400, "height": 780, "deviceScaleFactor": 1, "mobile": True})
time.sleep(0.8)

P = tab.js("[...document.querySelectorAll('.jm-popover')].findIndex(p=>p.textContent.includes('下'))")
tab.js(f"document.querySelectorAll('.jm-popover')[{P}].querySelector('.jm-popover__reference').click() || true")
ok = wait_for(f"document.querySelectorAll('.jm-popover')[{P}].querySelector('.jm-popover__panel')", 5)
time.sleep(0.6)
pc = tab.js(
    "(()=>{const panel=document.querySelectorAll('.jm-popover')[" + str(P) + "].querySelector('.jm-popover__panel');"
    "const phone=document.querySelector('.demo__phone')||document.documentElement;"
    "const pr=panel.getBoundingClientRect();const hr=phone.getBoundingClientRect();"
    "return JSON.stringify({pl:Math.round(pr.left),pr:Math.round(pr.right),hl:Math.round(hr.left),hrr:Math.round(hr.right),vw:innerWidth});})()"
)
pc = json.loads(pc)
check("popover", "panel rendered", ok, True)
# 手机框内不越界（回移生效；窗口视口兜底）
check("popover", "panel within clip box (left)", pc["pl"] >= pc["hl"] - 1, True)
check("popover", "panel within clip box (right)", pc["pr"] <= pc["hrr"] + 1, True)
check("popover", "panel within viewport too", pc["pl"] >= -1 and pc["pr"] <= pc["vw"] + 1, True)
tab.send("Emulation.clearDeviceMetricsOverride")
mouse_click(5, 5)
time.sleep(0.4)

# ================= Pagination 分级 =================
print("== pagination ==")
goto("/components/pagination")
wait_for("document.querySelectorAll('.jm-pagination').length >= 2")
time.sleep(1.2)

pg = tab.js("""(()=>{
  const nav=document.querySelector('.jm-pagination');
  const span=nav.querySelector('.jm-pagination__prev span');
  const visible=span && getComputedStyle(span).display!=='none';
  let bad=[];
  const pages=[...nav.querySelectorAll('.jm-pagination__page,.jm-pagination__more')];
  const prev=nav.querySelector('.jm-pagination__prev');
  const next=nav.querySelector('.jm-pagination__next');
  const hit=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left);
  pages.forEach(p=>{
    if(hit(p.getBoundingClientRect(),next?.getBoundingClientRect())) bad.push('next/'+p.textContent.trim());
    if(hit(p.getBoundingClientRect(),prev?.getBoundingClientRect())) bad.push('prev/'+p.textContent.trim());
  });
  return JSON.stringify({textKept:!!visible, overlap:bad});
})()""")
p = json.loads(pg)
check("pagination", "prev/next text kept at ~350px container", p["textKept"], True)
check("pagination", "no overlap after grading", p["overlap"], [])

# ================= Ellipsis =================
print("== ellipsis ==")
goto("/components/ellipsis")
wait_for("document.querySelectorAll('.jm-ellipsis').length >= 3")
time.sleep(1.0)

E = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelectorAll('.jm-ellipsis').length>=3)")
el = tab.js(
    "(()=>{const pages=document.querySelectorAll('.demo-page')[" + str(E) + "];"
    "const els=[...pages.querySelectorAll('.jm-ellipsis')];"
    "const single=els[0].querySelector('.jm-ellipsis__text');"
    "const multi=els[1];"
    "const mtext=multi.querySelector('.jm-ellipsis__text');"
    "const action=multi.querySelector('.jm-ellipsis__action');"
    "return JSON.stringify({"
    "clamp1:getComputedStyle(single).webkitLineClamp,"
    "h3:Math.round(mtext.getBoundingClientRect().height),"
    "lh:(parseFloat(getComputedStyle(mtext).lineHeight)*3).toFixed(0),"
    "action:action?action.textContent.trim():null,"
    "overflowShown:!!action});})()"
)
e = json.loads(el)
check("ellipsis", "single-line clamp applied", e["clamp1"], "1")
check("ellipsis", "multi-line collapsed to ~3 lines", abs(e["h3"] - float(e["lh"])) <= 6, True)
check("ellipsis", "expand action shown when overflowing", e["action"], "展开")
# 点展开 → 高度变大、文案变收起
h_before = e["h3"]
act = rect(f"document.querySelectorAll('.demo-page')[{E}].querySelectorAll('.jm-ellipsis')[1].querySelector('.jm-ellipsis__action')")
click_center(act)
time.sleep(0.5)
el2 = tab.js(
    "(()=>{const multi=document.querySelectorAll('.demo-page')[" + str(E) + "].querySelectorAll('.jm-ellipsis')[1];"
    "const t=multi.querySelector('.jm-ellipsis__text');"
    "return JSON.stringify({h:Math.round(t.getBoundingClientRect().height),action:multi.querySelector('.jm-ellipsis__action').textContent.trim()});})()"
)
e2 = json.loads(el2)
check("ellipsis", "expanded taller", e2["h"] > h_before + 10, True)
check("ellipsis", "action toggles to collapse", e2["action"], "收起")

# ================= Video =================
print("== video ==")
goto("/components/video")
wait_for("document.querySelectorAll('.jm-video').length >= 2", 12)
time.sleep(1.5)

vd = tab.js("""(()=>{
  const vs=[...document.querySelectorAll('.jm-video video')];
  const v1=vs[0], v2=vs[1];
  const r1=document.querySelectorAll('.jm-video')[0].getBoundingClientRect();
  return JSON.stringify({
    n:vs.length,
    ratio:Math.round(r1.height/Math.max(1,r1.width)*100),
    preload:v1?.getAttribute('preload'),
    muted2:v2?.muted,
    controls2:v2?.controls,
    loop2:v2?.loop,
  });
})()""")
v = json.loads(vd)
check("video", "two players rendered", v["n"], 2)
check("video", "16:9 default ratio (~56%)", abs(v["ratio"] - 56) <= 3, True)
check("video", "lazy preload none", v["preload"], "none")
check("video", "playInView forces muted", v["muted2"], True)
check("video", "playInView demo hides controls", v["controls2"], False)
check("video", "loop enabled in carousel demo", v["loop2"], True)

# ================= 汇总 =================
print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
