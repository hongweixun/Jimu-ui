#!/usr/bin/env python3
"""第 23 批（0.25.0）探针：Popover 四方向视口回移 / Pagination Varlet 化 /
Drag 拖拽 / Snackbar 消息条 / QRCode 二维码 / Guide 引导 / Calendar 今日角标"""
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
    tab.goto("http://localhost:5173" + path, wait=10)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")


def wait_for(expr, timeout=8.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


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


def viewport_of(dx, dy):
    """文档坐标 → 视口坐标"""
    sp = json.loads(tab.js("JSON.stringify({x:scrollX,y:scrollY})"))
    return int(dx - sp["x"]), int(dy - sp["y"])


def drag_doc(x1, y1, x2, y2, steps=6):
    """按文档坐标执行按下-拖动-松开"""
    vx1, vy1 = viewport_of(x1, y1)
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": vx1, "y": vy1, "button": "left", "clickCount": 1})
    for i in range(1, steps + 1):
        vx, vy = viewport_of(x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps)
        tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": vx, "y": vy})
    vx2, vy2 = viewport_of(x2, y2)
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": vx2, "y": vy2, "button": "left", "clickCount": 1})


def js_click(el_expr):
    tab.js("(" + el_expr + ").click() || true")


def drect(expr):
    """文档坐标（不受 scrollIntoView 重新居中影响）"""
    raw = tab.js(
        "(()=>{const el=" + expr + ";if(!el)return 'null';"
        "const r=el.getBoundingClientRect();"
        "return JSON.stringify({l:r.left+scrollX,t:r.top+scrollY,r:r.right+scrollX,b:r.bottom+scrollY,w:r.width,h:r.height});})()"
    )
    if not isinstance(raw, str):
        print("  [dbg] drect error:", raw)
        return None
    return json.loads(raw)


# ================= Popover 四方向视口回移 =================
print("== popover 4 directions ==")
goto("/components/popover")
wait_for("document.querySelectorAll('.jm-popover').length >= 5", 15)
time.sleep(1.5)

tab.send("Emulation.setDeviceMetricsOverride", {"width": 400, "height": 780, "deviceScaleFactor": 1, "mobile": True})
time.sleep(0.8)

markers = [("top", "is-top"), ("bottom", "is-bottom"), ("left", "is-left"), ("right", "is-right")]
for name, cls in markers:
    idx = tab.js("[...document.querySelectorAll('.jm-popover')].findIndex(p=>p.className.includes('" + cls + "'))")
    if not isinstance(idx, int):
        check("popover", f"{name} locate", str(idx)[:40], "int")
        continue
    tab.js(f"document.querySelectorAll('.jm-popover')[{idx}].querySelector('.jm-popover__reference').click() || true")
    ok = wait_for(
        f"!!document.querySelectorAll('.jm-popover')[{idx}].querySelector('.jm-popover__panel')", 5)
    time.sleep(0.7)
    raw = tab.js(
        "(()=>{const panel=document.querySelectorAll('.jm-popover')[" + str(idx) + "].querySelector('.jm-popover__panel');"
        "if(!panel)return 'null';"
        "const phone=document.querySelector('.demo__phone')||document.documentElement;"
        "const pr=panel.getBoundingClientRect();const hr=phone.getBoundingClientRect();"
        "return JSON.stringify({pl:Math.round(pr.left),prt:Math.round(pr.right),pt:Math.round(pr.top),pb:Math.round(pr.bottom),hl:Math.round(hr.left),hrt:Math.round(hr.right),ht:Math.round(hr.top),hb:Math.round(hr.bottom)});})()"
    )
    if not isinstance(raw, str):
        print("  [dbg] measure error:", raw)
        check("popover", f"{name} measure", False, True)
        mouse_click(5, 5)
        time.sleep(0.4)
        continue
    r = json.loads(raw)
    check("popover", f"{name} panel rendered", ok, True)
    check("popover", f"{name} within phone left", r["pl"] >= r["hl"] - 1, True)
    check("popover", f"{name} within phone right", r["prt"] <= r["hrt"] + 1, True)
    check("popover", f"{name} within phone top", r["pt"] >= r["ht"] - 1, True)
    check("popover", f"{name} within phone bottom", r["pb"] <= r["hb"] + 1, True)
    # 箭头跟随触发器：箭头中心应等于触发器中心钳制进面板安全区后的位置（±6px）
    arow = tab.js(
        "(()=>{const host=document.querySelectorAll('.jm-popover')[" + str(idx) + "];"
        "const a=host.querySelector('.jm-popover__arrow');const p=host.querySelector('.jm-popover__panel');"
        "if(!a||!p)return 'null';"
        "const ar=a.getBoundingClientRect();const hr=host.getBoundingClientRect();const pr=p.getBoundingClientRect();"
        "return JSON.stringify({acx:Math.round(ar.left+ar.width/2),tcx:Math.round(hr.left+hr.width/2),acy:Math.round(ar.top+ar.height/2),tcy:Math.round(hr.top+hr.height/2),pl:Math.round(pr.left),prt:Math.round(pr.right),pt:Math.round(pr.top),pb:Math.round(pr.bottom)});})()"
    )
    if isinstance(arow, str) and arow.startswith("{"):
        a = json.loads(arow)
        if name in ("top", "bottom"):
            exp = max(a["pl"] + 12, min(a["prt"] - 12, a["tcx"]))
            check("popover", f"{name} arrow tracks trigger x", abs(a["acx"] - exp) <= 6, True)
        else:
            exp = max(a["pt"] + 12, min(a["pb"] - 12, a["tcy"]))
            check("popover", f"{name} arrow tracks trigger y", abs(a["acy"] - exp) <= 6, True)
    else:
        check("popover", f"{name} arrow locate", False, True)
    mouse_click(5, 5)
    time.sleep(0.4)
tab.send("Emulation.clearDeviceMetricsOverride")

# ================= Pagination Varlet 化 =================
print("== pagination ==")
goto("/components/pagination")
wait_for("document.querySelectorAll('.jm-pagination').length >= 4")
time.sleep(1.0)

pg = tab.js("""(()=>{
  const pages=[...document.querySelectorAll('.jm-pagination')];
  const sizer=pages[0].querySelector('.jm-pagination__size select');
  const card=pages[0].querySelector('.jm-pagination__prev')?.closest('.jm-pagination');
  const cs=getComputedStyle(card);
  return JSON.stringify({
    sizer: !!sizer,
    options: sizer ? [...sizer.options].map(o=>o.value) : [],
    shadow: cs.boxShadow !== 'none',
    radius: cs.borderRadius,
  });
})()""")
pg = json.loads(pg)
check("pagination", "size-changer select rendered", pg["sizer"], True)
check("pagination", "size options", pg["options"], ["10", "20", "50", "100"])
check("pagination", "floating card shadow", pg["shadow"], True)

# 改每页条数 → 当前页按比例重算
tab.js("""(()=>{
  const s=document.querySelector('.jm-pagination__size select');
  s.value='50';
  s.dispatchEvent(new Event('change',{bubbles:true}));
  return true;
})()""")
time.sleep(0.5)
after = tab.js("""(()=>{
  const note=[...document.querySelectorAll('.demo-note')].map(n=>n.textContent).join(' ');
  const m=note.match(/当前第 (\\d+) 页、每页 (\\d+) 条/);
  const cur=document.querySelector('.jm-pagination .jm-pagination__page.is-active');
  return JSON.stringify({page:m?+m[1]:0,size:m?+m[2]:0,active:cur?cur.textContent.trim():''});
})()""")
after = json.loads(after)
check("pagination", "page-size changed to 50", after["size"], 50)
check("pagination", "current recalculated to 1", after["page"], 1)

# 快速跳转
demo2 = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelector('.jm-pagination__jumper'))")
if isinstance(demo2, int):
    tab.js(f"""(()=>{{
      const p=document.querySelectorAll('.demo-page')[{demo2}];
      const inp=p.querySelector('.jm-pagination__jumper input');
      inp.value='9';
      inp.dispatchEvent(new Event('input',{{bubbles:true}}));
      inp.dispatchEvent(new KeyboardEvent('keyup',{{key:'Enter',bubbles:true}}));
      return true;
    }})()""")
    time.sleep(0.5)
    jn = tab.js("""(()=>{
      const j=document.querySelector('.jm-pagination__jumper');
      const act=[...j.closest('.jm-pagination').querySelectorAll('.jm-pagination__page')].find(b=>b.classList.contains('is-active'));
      return act?act.textContent.trim():'';
    })()""")
    check("pagination", "quick jumper to page 9", jn, "9")

# total 插槽
ttotal = tab.js("""(()=>{
  const tot=[...document.querySelectorAll('.jm-pagination__total')].map(e=>e.textContent.trim());
  const hit=tot.find(t=>t.includes('共') && t.includes('当前'));
  return hit || '';
})()""")
check("pagination", "total slot text", ttotal, "共 96 条，当前 81-90 条")

# ================= Drag 拖拽 =================
print("== drag ==")
goto("/components/drag")
wait_for("document.querySelectorAll('.jm-drag').length >= 4")
time.sleep(1.0)

# 全部用文档坐标：rect() 的 scrollIntoView 会把元素重新居中，视觉坐标不可靠
rect("document.querySelectorAll('.jm-drag')[0]")  # 先滚入视口
d0 = drect("document.querySelectorAll('.jm-drag')[0]")
if d0:
    cx, cy = d0["l"] + d0["w"] / 2, d0["t"] + d0["h"] / 2
    drag_doc(cx, cy, cx + 60, cy + 60)
    time.sleep(0.6)
    d0b = drect("document.querySelectorAll('.jm-drag')[0]")
    check("drag", "basic drag moved", abs(d0b["l"] - d0["l"]) >= 40 and abs(d0b["t"] - d0["t"]) >= 40, True)
    # 点一下不算拖拽：位置不变
    vx, vy = viewport_of(d0b["l"] + d0b["w"] / 2, d0b["t"] + d0b["h"] / 2)
    mouse_click(vx, vy)
    time.sleep(0.4)
    d0c = drect("document.querySelectorAll('.jm-drag')[0]")
    check("drag", "click does not move", abs(d0c["l"] - d0b["l"]) <= 2, True)
    # 容器约束：拖 300px 也出不了 stage1
    cx2, cy2 = d0c["l"] + d0c["w"] / 2, d0c["t"] + d0c["h"] / 2
    drag_doc(cx2, cy2, cx2 + 300, cy2 + 300, steps=3)
    time.sleep(0.6)
    d0d = drect("document.querySelectorAll('.jm-drag')[0]")
    st1 = drect("document.querySelector('#stage1')")
    check("drag", "clamped inside stage", d0d["r"] <= st1["r"] + 2 and d0d["b"] <= st1["b"] + 2, True)
else:
    check("drag", "basic drag locate", False, True)

# direction="x"：只横移（先滚入视口，再按压）
d1 = rect("document.querySelectorAll('.jm-drag')[1]")
if d1:
    d1d = drect("document.querySelectorAll('.jm-drag')[1]")
    cx, cy = d1d["l"] + d1d["w"] / 2, d1d["t"] + d1d["h"] / 2
    drag_doc(cx, cy, cx + 60, cy + 60, steps=2)
    time.sleep(0.6)
    d1b = drect("document.querySelectorAll('.jm-drag')[1]")
    check("drag", "direction x only horizontal", abs(d1b["l"] - d1d["l"]) >= 30, True)
    check("drag", "direction x no vertical", abs(d1b["t"] - d1d["t"]) <= 2, True)
else:
    check("drag", "direction x locate", False, True)

# attraction="x"：松手吸附到最近的边
d2 = rect("document.querySelectorAll('.jm-drag')[2]")
if d2:
    d2d = drect("document.querySelectorAll('.jm-drag')[2]")
    cx, cy = d2d["l"] + d2d["w"] / 2, d2d["t"] + d2d["h"] / 2
    drag_doc(cx, cy, cx + 60, cy, steps=2)
    time.sleep(0.8)
    d2b = drect("document.querySelectorAll('.jm-drag')[2]")
    st2 = drect("document.querySelector('#stage2')")
    snapped = d2b["l"] <= st2["l"] + 8 or d2b["r"] >= st2["r"] - 8
    check("drag", "attraction x snaps to edge", snapped, True)
else:
    check("drag", "attraction locate", False, True)

# reset（stage3 内联初始位置 left:30px top:20px）
tab.js("[...document.querySelectorAll('.demo-page')].find(p=>p.querySelector('.jm-drag')).querySelector('button.reset').click()")
time.sleep(0.5)
d3 = drect("document.querySelectorAll('.jm-drag')[3]")
st3 = drect("document.querySelector('#stage3')")
check("drag", "reset back to inline initial", abs(d3["l"] - st3["l"] - 30) <= 4 and abs(d3["t"] - st3["t"] - 20) <= 4, True)

# ================= Snackbar =================
print("== snackbar ==")
goto("/components/snackbar")
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('底部消息条'))")
time.sleep(0.8)

def snb_open(label):
    idx = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.textContent.includes('" + label + "'))")
    tab.js(f"""(()=>{{
      const p=document.querySelectorAll('.demo-page')[{idx}];
      const btn=[...p.querySelectorAll('button.chip')].find(b=>b.textContent.includes('{label}'));
      btn.click();
      return true;
    }})()""")

snb_open("成功")
ok = wait_for("!!document.querySelector('.jm-snackbar--success')", 5)
time.sleep(0.5)
s1 = tab.js("""(()=>{
  const el=document.querySelector('.jm-snackbar--success');
  const r=el.getBoundingClientRect();
  return JSON.stringify({text:el.querySelector('.jm-snackbar__content').textContent, top:Math.round(r.top), n:document.querySelectorAll('.jm-snackbar').length});
})()""")
s1 = json.loads(s1)
check("snackbar", "success type rendered", ok, True)
check("snackbar", "success content", s1["text"], "提交成功，审核将在 1 个工作日内完成")
check("snackbar", "singleton: one at a time", s1["n"], 1)

snb_open("普通")
time.sleep(0.5)
s2 = json.loads(tab.js("JSON.stringify({n:document.querySelectorAll('.jm-snackbar').length, t:document.querySelector('.jm-snackbar__content')?.textContent})"))
check("snackbar", "new replaces old", s2["n"], 1)
check("snackbar", "old cleared", s2["t"], "草稿已自动保存")

snb_open("底部消息条")
time.sleep(1.0)
ok = wait_for("!!document.querySelector('.jm-snackbar__action')", 5)
check("snackbar", "bottom snackbar exists", ok, True)
# 出现且进场动画一结束立即测量（bar 3 秒自动消失，不能拖太久）
# 消息条挂载在手机模拟器屏幕内：以屏幕底边为基准测距离
s3 = 'none'
end = time.time() + 3
while time.time() < end:
    s3 = tab.js("""(()=>{
      const act=document.querySelector('.jm-snackbar__action');
      const el=act?act.closest('.jm-snackbar'):null;
      if(!el)return 'none';
      if(el.className.includes('enter-active')||el.className.includes('leave-active'))return 'anim';
      const screen=document.querySelector('.phone__screen');
      const r=el.getBoundingClientRect(), sr=screen.getBoundingClientRect();
      return JSON.stringify({bottom:Math.round(sr.bottom-r.bottom), inside: r.left>=sr.left-1 && r.right<=sr.right+1 && r.bottom<=sr.bottom+1, action:act.textContent});
    })()""")
    if isinstance(s3, str) and s3.startswith("{"):
        break
    time.sleep(0.15)
if isinstance(s3, str) and s3.startswith("{"):
    s3 = json.loads(s3)
    check("snackbar", "bottom position near screen bottom", 0 <= s3["bottom"] <= 24, True)
    check("snackbar", "bar inside phone screen", s3["inside"], True)
    check("snackbar", "action button", s3["action"], "去结算")
else:
    check("snackbar", "bottom position measurable", s3, "json")

js_click("[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('clearSnackbar')).querySelector('button.chip--ghost')")
time.sleep(0.5)
check("snackbar", "clearSnackbar removes all", tab.js("document.querySelectorAll('.jm-snackbar').length"), 0)

snb_open("竖排消息条")
ok = wait_for("!!document.querySelector('.jm-snackbar.is-vertical')", 5)
check("snackbar", "vertical layout", ok, True)

# ================= QRCode =================
print("== qrcode ==")
goto("/components/qrcode")
wait_for("document.querySelectorAll('.jm-qrcode canvas').length >= 2")
time.sleep(0.8)

q1 = tab.js("""(()=>{
  try{
    const c=document.querySelector('.jm-qrcode canvas');
    if(!c)return JSON.stringify({err:'no canvas'});
    const ctx=c.getContext('2d');
    const img=ctx.getImageData(0,0,c.width,c.height).data;
    let dark=0;
    for(let i=0;i<img.length;i+=4){ if(img[i]<128) dark++; }
    return JSON.stringify({w:c.width,h:c.height,dark,css:Math.round(c.getBoundingClientRect().width)});
  }catch(e){return JSON.stringify({err:e.message});}
})()""")
q1 = json.loads(q1)
if "err" in q1:
    check("qrcode", "canvas readable", False, True)
else:
    check("qrcode", "canvas rendered", q1["w"] > 0 and q1["dark"] > 50, True)
    check("qrcode", "canvas is HD (>= css size)", q1["w"] >= q1["css"], True)

# 改内容后重绘（像素变化）
before = q1.get("dark", 0)
idx = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.querySelector('.jm-qrcode'))")
tab.js(f"""(()=>{{
  const p=document.querySelectorAll('.demo-page')[{idx}];
  const inp=p.querySelector('input.jm-input__control') || p.querySelector('input');
  const setter=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
  setter.call(inp,'https://workbuddy.cn/hello');
  inp.dispatchEvent(new Event('input',{{bubbles:true}}));
  return true;
}})()""")
time.sleep(0.6)
q2r = tab.js("""(()=>{
  try{
    const c=document.querySelector('.jm-qrcode canvas');
    if(!c)return JSON.stringify({err:'no canvas'});
    const ctx=c.getContext('2d');
    const img=ctx.getImageData(0,0,c.width,c.height).data;
    let dark=0;
    for(let i=0;i<img.length;i+=4){ if(img[i]<128) dark++; }
    return JSON.stringify({dark});
  }catch(e){return JSON.stringify({err:e.message});}
})()""")
q2 = json.loads(q2r)
check("qrcode", "re-encodes on value change", "err" not in q2 and q2["dark"] != before, True)

# 导出 toDataURL
url = tab.js("""(()=>{
  const host=[...document.querySelectorAll('.demo-page')].find(p=>p.querySelector('canvas'));
  const comp=host.querySelector('.jm-qrcode');
  const inst=comp.__vueParentComponent?.exposed;
  if(!inst) return '';
  return inst.toDataURL ? inst.toDataURL(2) : '';
})()""")
check("qrcode", "toDataURL returns png", isinstance(url, str) and url.startswith("data:image/png;base64,"), True)

# ================= Guide =================
print("== guide ==")
goto("/components/guide")
# Guide 未开启时不渲染任何元素，按页面文本定位 demo
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('开始引导'))")
time.sleep(0.8)

idx = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.textContent.includes('开始引导'))")
js_click(f"[...document.querySelectorAll('.demo-page')[{idx}].querySelectorAll('button.chip--primary')].find(b=>b.textContent.includes('开始引导'))")
ok = wait_for("!!document.querySelector('.jm-guide__bubble')", 5)
time.sleep(0.6)
g1 = json.loads(tab.js("""(()=>{
  const bubble=document.querySelector('.jm-guide__bubble');
  const mask=document.querySelector('.jm-guide__mask');
  const hl=document.querySelector('.jm-guide__highlight');
  const cnt=document.querySelector('.jm-guide__count');
  const tgt=document.getElementById('guide-step-1').getBoundingClientRect();
  const hr=hl?hl.getBoundingClientRect():null;
  const sr=document.querySelector('.phone__screen').getBoundingClientRect();
  const mr=mask.getBoundingClientRect();
  const br=bubble.getBoundingClientRect();
  return JSON.stringify({
    cnt: cnt?cnt.textContent.trim():'',
    overlap: hr && hr.left < tgt.right && hr.right > tgt.left && hr.top < tgt.bottom && hr.bottom > tgt.top,
    title: bubble.querySelector('.jm-guide__title').textContent,
    maskOnScreenOnly: Math.abs(mr.left-sr.left)<3 && Math.abs(mr.right-sr.right)<3 && Math.abs(mr.top-sr.top)<3 && Math.abs(mr.bottom-sr.bottom)<3,
    bubbleInside: br.left>=sr.left-1 && br.right<=sr.right+1 && br.top>=sr.top-1,
  });
})()"""))
check("guide", "bubble shown", ok, True)
check("guide", "count 1/3", g1["cnt"], "1/3")
check("guide", "highlight covers step target", g1["overlap"], True)
check("guide", "first step title", g1["title"], "搜索课程")
check("guide", "mask covers phone screen only", g1["maskOnScreenOnly"], True)
check("guide", "bubble inside phone screen", g1["bubbleInside"], True)

js_click("document.querySelector('.jm-guide__btn.is-primary')")
time.sleep(0.6)
g2 = tab.js("document.querySelector('.jm-guide__count')?.textContent.trim() || ''")
check("guide", "next -> 2/3", g2, "2/3")

js_click("[...document.querySelectorAll('.jm-guide__btn')].find(b=>b.textContent.includes('跳过'))")
time.sleep(0.5)
check("guide", "skip closes guide", tab.js("!!document.querySelector('.jm-guide__bubble')"), False)

# dialog 模式
idx = tab.js("[...document.querySelectorAll('.demo-page')].findIndex(p=>p.textContent.includes('开始引导'))")
js_click(f"[...document.querySelectorAll('.demo-page')[{idx}].querySelectorAll('button.chip')].find(b=>b.textContent.includes('弹窗引导'))")
ok = wait_for("!!document.querySelector('.jm-guide__bubble')", 5)
time.sleep(0.5)
gd = json.loads(tab.js("""(()=>{
  const shade=document.querySelectorAll('.jm-guide__shade').length;
  const cnt=document.querySelector('.jm-guide__count')?.textContent.trim()||'';
  const bubble=document.querySelector('.jm-guide__bubble');
  const br=bubble.getBoundingClientRect();
  const sr=document.querySelector('.phone__screen').getBoundingClientRect();
  return JSON.stringify({shades:shade, cnt, bubble:!!bubble,
    centered: Math.abs((br.left+br.right)/2-(sr.left+sr.right)/2)<10 && Math.abs((br.top+br.bottom)/2-(sr.top+sr.bottom)/2)<10,
    inside: br.left>=sr.left-1 && br.right<=sr.right+1 && br.top>=sr.top-1 && br.bottom<=sr.bottom+1});
})()"""))
check("guide", "dialog bubble shown", gd["bubble"], True)
check("guide", "dialog mode full shade (no hole)", gd["shades"], 1)
check("guide", "dialog count 1/2", gd["cnt"], "1/2")
check("guide", "dialog centered in phone screen", gd["centered"], True)
check("guide", "dialog inside phone screen", gd["inside"], True)

# ================= Calendar 今日角标 =================
print("== calendar today ==")
goto("/components/calendar")
wait_for("[...document.querySelectorAll('.demo-page')].some(p=>p.querySelector('.jm-calendar'))", 12)
time.sleep(0.8)
# 打开第一个日历（若收起则点头展开）
opened = wait_for("document.querySelector('.jm-calendar__days') && document.querySelector('.jm-calendar__days').offsetHeight > 100", 4)
if not opened:
    js_click("document.querySelector('.jm-calendar__header')")
    wait_for("document.querySelector('.jm-calendar__days') && document.querySelector('.jm-calendar__days').offsetHeight > 100", 6)
time.sleep(0.5)
cal = json.loads(tab.js("""(()=>{
  const day=document.querySelector('.jm-calendar__day.is-today');
  if(!day) return JSON.stringify({found:false});
  const info=day.querySelector('.jm-calendar__day-info.is-bottom');
  return JSON.stringify({found:true, text:day.querySelector('.jm-calendar__day-text').textContent.trim(), badge:info?info.textContent.trim():'', selected:day.classList.contains('is-selected')});
})()"""))
check("calendar", "today cell found", cal.get("found"), True)
# 0.25.3 起「今」字小字改为「今天」二字替代数字（对齐 TDesign）
check("calendar", "today shows 今天 instead of number", cal.get("text"), "今天")
check("calendar", "today has no 今 below", cal.get("badge"), "")

# ================= 汇总 =================
print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
