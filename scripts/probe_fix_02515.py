# -*- coding: utf-8 -*-
"""0.25.15 探针：
1) Calendar 点选「露出但非副标题月」的日期不跳页（scrollTop 不变）
2) IndexBar 轻点平滑滚动（中间帧连续）、拖动仍瞬时定位
"""
import sys, time, json

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

ensure_edge()
tab = new_tab()
tab.send("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

# ---------- 1) Calendar 不跳页 ----------
tab.goto("http://localhost:5173/components/calendar", wait=8)
time.sleep(1)
r = tab.js(r"""(()=>{
  const cal=document.querySelector('.jm-calendar');
  const vp=cal.querySelector('.jm-calendar__viewport');
  if(!vp) return 'no-vp';
  cal.scrollIntoView({block:'start'});
  const secs=[...vp.querySelectorAll('.jm-calendar__month')];
  if(secs.length<2) return 'too-few-months';
  // 取第一个月，把视口滚到「首月占主体 + 次月标题+第一行露出在底部」
  const first=secs[0], next=secs[1];
  const rowH=first.querySelector('.jm-calendar__day').offsetHeight;
  const want=next.offsetTop + 26 + rowH + 8 - vp.clientHeight;
  vp.scrollTop=Math.max(want, 0);
  return JSON.stringify({scroll:vp.scrollTop, vpH:vp.clientHeight,
    nextTop:next.offsetTop, firstBottom:first.offsetTop+first.offsetHeight,
    subtitle:(cal.querySelector('.jm-calendar__subtitle')||cal.querySelector('.jm-calendar__month-title'))?.textContent.trim()});
})()""")
print("setup:", r)
d = json.loads(r)
time.sleep(0.3)

r = tab.js(r"""(()=>{
  const cal=document.querySelector('.jm-calendar');
  const vp=cal.querySelector('.jm-calendar__viewport');
  const secs=[...vp.querySelectorAll('.jm-calendar__month')];
  const next=secs[1];
  // 次月第一行里第一个可选的日子
  const rows=[...next.querySelectorAll('.jm-calendar__days')];
  const day=[...rows[0].querySelectorAll('.jm-calendar__day.is-current')].find(x=>!x.classList.contains('is-disabled'));
  if(!day) return 'no-day';
  const before=vp.scrollTop;
  const txt=day.textContent.trim();
  day.click();
  return JSON.stringify({before, txt});
})()""")
d = json.loads(r)
time.sleep(0.4)
r = tab.js(r"""(()=>{
  const vp=document.querySelector('.jm-calendar__viewport');
  const sel=document.querySelector('.jm-calendar .is-selected');
  return JSON.stringify({after:vp.scrollTop, selTxt:sel?sel.textContent.trim().slice(0,4):null});
})()""")
e = json.loads(r)
check("cal.select-visible-month-no-jump",
      abs(e["after"] - d["before"]) <= 1,
      f"before={d['before']} after={e['after']} day={d['txt']} sel={e['selTxt']}")

# ---------- 2) IndexBar 轻点平滑滚动 ----------
tab.goto("http://localhost:5173/components/index-bar", wait=8)
# 无头环境强制了 prefers-reduced-motion: reduce（原生 smooth 也不动画），覆写还原正常环境
tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
time.sleep(1)
print("reduced-motion now:", tab.js("window.matchMedia('(prefers-reduced-motion: reduce)').matches"))
r = tab.js(r"""(()=>{
  const items=[...document.querySelectorAll('.jm-index-bar__item')];
  if(items.length<6) return 'few';
  const t=items[4]; // 第 5 个索引
  t.scrollIntoView({block:'center'});
  const rc=t.getBoundingClientRect();
  return JSON.stringify({x:Math.round(rc.x+rc.width/2), y:Math.round(rc.y+rc.height/2), label:t.textContent.trim(),
    n:items.length});
})()""")
d = json.loads(r)
print("indexbar target:", d)
time.sleep(0.3)

# 轻点：pointerdown → 100ms → pointerup，随后采样 scrollTop 轨迹
tab.js("""(()=>{
  const items=[...document.querySelectorAll('.jm-index-bar__item')];
  const el=items[4];
  const rc=el.getBoundingClientRect();
  const y=rc.y+rc.height/2, x=rc.x+rc.width/2;
  window.__trace=[];
  window.__t0=performance.now();
  const snap=()=>{const c=document.getElementById('idx-scroll');window.__trace.push([Math.round(performance.now()-window.__t0), Math.round(c.scrollTop)])};
  snap();
  el.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:x,clientY:y,pointerId:1}));
  setTimeout(snap,30);
  setTimeout(()=>{el.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:x,clientY:y,pointerId:1}));
    [80,160,240,360,520,800].forEach(ms=>setTimeout(snap,ms));},100);
  return 1;
})()""")
time.sleep(1.2)
trace = json.loads(tab.js("JSON.stringify(window.__trace)"))
print("tap trace (ms, scrollY):", trace)
mid = [p for p in trace if 130 <= p[0] <= 500]
distinct_mid = len(set(p[1] for p in trace if p[0] >= 130))
moved = trace[-1][1] != trace[0][1]
check("indexbar.tap-moves", moved, f"{trace[0]}->{trace[-1]}")
check("indexbar.tap-smooth-intermediate", moved and distinct_mid >= 3, f"distinct mid positions={distinct_mid}")

# 终点核对：目标分组标题到达容器顶附近
r = tab.js(r"""(()=>{
  const items=[...document.querySelectorAll('.jm-index-bar__item')];
  const label=items[4].textContent.trim();
  const anchors=[...document.querySelectorAll('.jm-index-anchor')];
  const a=anchors.find(x=>x.textContent.trim().startsWith(label));
  if(!a) return 'no-anchor';
  return JSON.stringify({label, top:Math.round(a.getBoundingClientRect().top)});
})()""")
print("anchor after tap:", r)

# 拖动：pointerdown 在第1个 → move 到第8个 → up，应瞬时到达（trace 首帧即近终点）
r = tab.js(r"""(()=>{
  const items=[...document.querySelectorAll('.jm-index-bar__item')];
  const bar=document.querySelector('.jm-index-bar__sidebar');
  const a=items[0].getBoundingClientRect(), b=items[Math.min(7,items.length-1)].getBoundingClientRect();
  window.__trace2=[];
  const snap=()=>{const c=document.getElementById('idx-scroll');window.__trace2.push([Math.round(performance.now()), Math.round(c.scrollTop)])};
  bar.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:a.x+a.width/2,clientY:a.y+a.height/2,pointerId:2}));
  snap();
  bar.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,clientX:b.x+b.width/2,clientY:b.y+b.height/2,pointerId:2}));
  bar.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:b.x+b.width/2,clientY:b.y+b.height/2,pointerId:2}));
  snap();
  return JSON.stringify(window.__trace2);
})()""")
print("drag trace:", r)

print("\n==== summary ====")
fails = [x for x in results if not x[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed")
sys.exit(1 if fails else 0)
