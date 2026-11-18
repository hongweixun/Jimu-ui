#!/usr/bin/env python3
"""弹出动画时序探针（页面内 rAF 录制）：打开 poppable 日历时逐帧记录布局指标，
找出「闪一下」发生在哪一帧、哪个属性在跳。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab  # noqa: E402

ensure_edge()
tab = new_tab()

tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
tab.send("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
tab.goto("http://localhost:5173/components/calendar", wait=6)
time.sleep(1.0)

RECORDER = """(()=>{
  window.__f=[];
  const snap=()=>{
    const p=document.querySelector('.jm-popup');
    const cal=p?p.querySelector('.jm-calendar'):null;
    const vp=cal?cal.querySelector('.jm-calendar__viewport'):null;
    const hd=cal?cal.querySelector('.jm-calendar__header'):null;
    const wd=cal?cal.querySelector('.jm-calendar__weekdays'):null;
    const ft=cal?cal.querySelector('.jm-calendar__footer'):null;
    const pr=p?p.getBoundingClientRect():null;
    const cs=p?getComputedStyle(p):null;
    return {
      t:performance.now(),
      pTop: pr?Math.round(pr.top):null,
      pH: p?Math.round(p.offsetHeight):0,
      op: cs?Math.round(Number(cs.opacity)*100)/100:0,
      calH: cal?Math.round(cal.offsetHeight):0,
      vpH: vp?vp.clientHeight:0,
      vpTop: vp?Math.round(vp.getBoundingClientRect().top):0,
      vpST: vp?Math.round(vp.scrollTop):0,
      vpSH: vp?vp.scrollHeight:0,
      headH: hd?Math.round(hd.offsetHeight):0,
      weekH: wd?Math.round(wd.offsetHeight):0,
      footH: ft?Math.round(ft.offsetHeight):0,
      pSH: p?p.scrollHeight:0,
      pCH: p?p.clientHeight:0,
      cssVar: cal?getComputedStyle(cal).getPropertyValue('--jm-calendar-viewport-h').trim():'',
    };
  };
  const loop=()=>{
    window.__f.push(snap());
    if(window.__f.length<150) requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
  return 'rec';
})()"""
print(tab.js(RECORDER))

# 录制启动后 100ms 触发点击（页面内触发，走与用户点击同一条 Vue 事件链）
tab.js(
    """(()=>{
      setTimeout(()=>{
        const b=[...document.querySelectorAll('.demo-page button')].find(x=>x.textContent.includes('底部弹出'));
        window.__btn = !!b;
        if(b) b.click();
      }, 100);
      return 'armed';
    })()"""
)

time.sleep(2.8)
print("btn found:", tab.js("window.__btn"), "| frames:", tab.js("window.__f.length"))

frames = json.loads(tab.js("JSON.stringify(window.__f)"))
t0 = frames[0]["t"]
print("\n  t(ms) |  pTop   pH   op | calH vpH vpTop vpST/vpSH | head week foot | pSH/pCH | cssVar")
for f in frames:
    print(
        f"{f['t']-t0:>7.0f} | {str(f['pTop']):>5} {f['pH']:>4} {f['op']:>4.2f} | {f['calH']:>4} {f['vpH']:>3} {f['vpTop']:>5} "
        f"{str(f['vpST']):>5}/{f['vpSH']:<5} | {f['headH']:>4} {f['weekH']:>4} {f['footH']:>4} | {f['pSH']}/{f['pCH']} | {f['cssVar']}"
    )
