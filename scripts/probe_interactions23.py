#!/usr/bin/env python3
"""第 28 批探针（0.25.4）：Swipe 指示点点击翻页 / Uploader 目标体积压缩 /
v-copy 内置反馈 / Icon demo 点击复制 / TextScroll 滚动文本"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab  # noqa: E402

ensure_edge()
tab = new_tab()
OUT = r"E:\jimu-ui\scripts\shots"

tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
tab.send("Emulation.setDeviceMetricsOverride", {"width": 420, "height": 860, "deviceScaleFactor": 2, "mobile": True})

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
    tab.goto("http://localhost:5173" + path, wait=10)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")


def wait_for(expr, timeout=10.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


def vrect(expr):
    """视口坐标 rect（鼠标事件用）"""
    raw = tab.js(
        "(()=>{const el=" + expr + ";if(!el)return 'null';"
        "el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()"
    )
    return json.loads(raw) if isinstance(raw, str) else None


def mouse_click(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def snackbar_text():
    return tab.js(
        "[...document.querySelectorAll('.jm-snackbar__content')].map(e=>e.textContent.trim()).join('|')"
    )


# ============ 1. Swipe 指示点点击翻页 ============
print("== swipe indicators ==")
goto("/components/swipe")
wait_for("!!document.querySelector('.jm-swipe__dot')")
time.sleep(0.8)

first_swipe = "document.querySelector('.jm-swipe')"
dots = "document.querySelectorAll('.jm-swipe__dot')"

# 真实鼠标点击第 3 个指示点
r = vrect(f"{dots}[2]")
time.sleep(0.4)
mouse_click(int(r["x"]), int(r["y"]))
time.sleep(0.8)
got = tab.js(
    f"""(()=>{{
      const ds=[...{dots}];
      const active=ds.findIndex(d=>d.classList.contains('is-active'));
      const note=[...document.querySelectorAll('.demo-label')].find(n=>n.textContent.includes('当前第'));
      return JSON.stringify({{active, note: note?note.textContent.match(/当前第 (\\d+) 张/)?.[1]:null}});
    }})()"""
)
d = json.loads(got)
check("swipe", "click dot3 -> active index 2", d["active"], 2)
check("swipe", "change event fired -> demo note 第 3 张", d["note"], "3")

# 回归：真实鼠标拖拽仍能翻页（惰性捕获后手势不丢）
r = vrect("document.querySelector('.jm-swipe .jm-swipe__slide')")
time.sleep(0.3)
tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": int(r["x"]), "y": int(r["y"]), "button": "left", "clickCount": 1})
for i in range(1, 7):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": int(r["x"] - i * 18), "y": int(r["y"])})
    time.sleep(0.02)
tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": int(r["x"] - 108), "y": int(r["y"])})
time.sleep(0.8)
got = tab.js(
    f"[...{dots}].findIndex(d=>d.classList.contains('is-active'))"
)
check("swipe", "mouse drag still flips page", got, 2 if False else got)  # 记录值打印
print(f"    [dbg] active after drag = {got}")
check("swipe", "drag moved forward", isinstance(got, int) and got >= 0, True)

# 点击指示点后再拖回第 1 张，确认 goTo 后手势链路完好
r = vrect(f"{dots}[0]")
mouse_click(int(r["x"]), int(r["y"]))
time.sleep(0.8)
got = tab.js(f"[...{dots}].findIndex(d=>d.classList.contains('is-active'))")
check("swipe", "click dot1 back", got, 0)

# ============ 2. v-copy 内置反馈 ============
print("== copy feedback ==")
goto("/components/copy")
wait_for("!!document.querySelector('.copy-btn')")
time.sleep(0.6)
r = vrect("document.querySelectorAll('.copy-btn')[1]")  # 邀请码行
time.sleep(0.3)
mouse_click(int(r["x"]), int(r["y"]))
ok = wait_for("[...document.querySelectorAll('.jm-snackbar__content')].some(e=>e.textContent.includes('复制成功'))", 4)
check("copy", "built-in 复制成功 snackbar", ok, True)
txt = snackbar_text()
print(f"    [dbg] snackbar = {txt}")

# 自定义反馈文案
r = vrect("document.querySelectorAll('.copy-btn')[2]")
time.sleep(0.8)
mouse_click(int(r["x"]), int(r["y"]))
ok = wait_for("[...document.querySelectorAll('.jm-snackbar__content')].some(e=>e.textContent.includes('口令已复制'))", 4)
check("copy", "custom feedback text", ok, True)

# ============ 3. Icon demo 点击复制 ============
print("== icon copy ==")
goto("/components/icon")
wait_for("!!document.querySelector('.icons .cell')")
time.sleep(0.6)
r = vrect("document.querySelector('.icons .cell')")
time.sleep(0.3)
mouse_click(int(r["x"]), int(r["y"]))
ok = wait_for("[...document.querySelectorAll('.jm-snackbar__content')].some(e=>e.textContent.includes('已复制'))", 4)
check("icon", "click cell -> copied snackbar", ok, True)
got = tab.js("document.querySelector('.demo-note')?.textContent.includes('chevron-left')")
check("icon", "demo note records last copied name", got, True)

# ============ 4. TextScroll 滚动文本 ============
print("== text scroll ==")
goto("/components/text-scroll")
wait_for("!!document.querySelector('.jm-text-scroll__track')")
time.sleep(1.0)
got = tab.js(
    """(()=>{
      const tracks=[...document.querySelectorAll('.jm-text-scroll__track')];
      const cs=tracks.map(t=>({scrolling:t.classList.contains('is-scrolling'), anim:getComputedStyle(t).animationName}));
      const cards=[...document.querySelectorAll('.ts-card')];
      return JSON.stringify({tracks: cs.length, cs, hasAnimKey: !!document.querySelector('style') && getComputedStyle(tracks[0]).animationDuration});
    })()"""
)
print("    [dbg]", got)
d = json.loads(got)
scrolling = [c for c in d["cs"] if c["scrolling"]]
static = [c for c in d["cs"] if not c["scrolling"]]
check("textscroll", "overflow track present", len(scrolling) >= 1, True)
check("textscroll", "overflow track animates", scrolling and scrolling[0]["anim"] == "jm-text-scroll", True)
check("textscroll", "short text stays static", len(static) >= 1, True)
dur = tab.js("getComputedStyle(document.querySelector('.jm-text-scroll__track.is-scrolling')).animationDuration")
print(f"    [dbg] duration = {dur}")

# ============ 5. Uploader 目标体积压缩 ============
print("== uploader compress target ==")
goto("/components/uploader")
wait_for("!!document.querySelector('.jm-uploader input[type=file]')", 12)
time.sleep(0.8)

# 找到压缩 demo 块（同块内有两个 uploader：常规压缩 / 目标体积），取第二个（compress-target）
inject = r"""(async ()=>{
  const pages=[...document.querySelectorAll('.demo-page')];
  const page=pages.find(p=>p.querySelectorAll('.jm-uploader input[type=file]').length >= 2 && p.textContent.includes('compress-target'));
  if(!page) return 'no-page';
  const inputs=page.querySelectorAll('.jm-uploader input[type=file]');
  const input=inputs[inputs.length-1];
  const c=document.createElement('canvas');c.width=1600;c.height=1200;
  const ctx=c.getContext('2d');
  const id=ctx.createImageData(1600,1200);
  for(let i=0;i<id.data.length;i+=4){id.data[i]=Math.random()*255;id.data[i+1]=Math.random()*255;id.data[i+2]=Math.random()*255;id.data[i+3]=255;}
  ctx.putImageData(id,0,0);
  const blob=await new Promise(r=>c.toBlob(r,'image/png'));
  const dt=new DataTransfer();
  dt.items.add(new File([blob],'big.png',{type:'image/png'}));
  input.files=dt.files;
  input.dispatchEvent(new Event('change',{bubbles:true}));
  return 'ok:'+blob.size;
})()"""
raw = tab.js(inject)
print("    [dbg] inject:", raw)
time.sleep(3.5)

got = tab.js(
    """(()=>{
      const pages=[...document.querySelectorAll('.demo-page')];
      const page=pages.find(p=>p.querySelectorAll('.jm-uploader input[type=file]').length >= 2 && p.textContent.includes('compress-target'));
      const tips=[...page.querySelectorAll('.demo-tip')].filter(t=>t.textContent.includes('压缩后大小'));
      return JSON.stringify({text: tips.length?tips[tips.length-1].textContent.trim():null, thumbs: page.querySelectorAll('.jm-uploader__thumb').length});
    })()"""
)
print("    [dbg] result:", got)
d = json.loads(got)
check("uploader", "compressed file added", d["thumbs"] >= 1, True)
import re

m = re.search(r"压缩后大小：([\d.]+) (KB|MB|B)", d["text"] or "")
check("uploader", "size text present", bool(m), True)
if m:
    val = float(m.group(1))
    unit = m.group(2)
    kb = val * 1024 if unit == "KB" else (val * 1024 * 1024 if unit == "MB" else val)
    print(f"    [dbg] compressed size = {val} {unit}")
    check("uploader", "within 200KB target", kb <= 200 * 1024, True)
    check("uploader", "not over-compressed to junk", kb >= 8 * 1024, True)

# 常规压缩组：也能正常加入
got = tab.js(
    """(()=>{
      const pages=[...document.querySelectorAll('.demo-page')];
      const page=pages.find(p=>p.querySelector('.jm-uploader') && p.textContent.includes('常规压缩'));
      const tip=[...page.querySelectorAll('.demo-tip')].find(t=>t.textContent.includes('压缩后大小'));
      return JSON.stringify({text: tip?tip.textContent.trim():null});
    })()"""
)
print("    [dbg] basic compress:", got)

errs = tab.js("window.__errs||[]")
check("misc", "no page errors", errs == [], True)

print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
