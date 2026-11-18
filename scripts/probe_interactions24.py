#!/usr/bin/env python3
"""第 29 批探针（0.25.6）：Calendar 月份纵向连续滚动 / poppable 弹出模式 /
iOS 首帧即渲染定位 / 横滑翻月与边界钳制"""
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


def mouse_click(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def mouse_drag(x, y, dx, dy, steps=8):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    for i in range(1, steps + 1):
        tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x + dx * i // steps, "y": y + dy * i // steps, "button": "left"})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x + dx, "y": y + dy, "button": "left", "clickCount": 1})


# ============ 1. 月份纵向连续滚动 ============
print("== calendar month scroll ==")
goto("/components/calendar")
wait_for("[...document.querySelectorAll('.jm-calendar__viewport')].length > 0 && document.querySelector('.jm-calendar__viewport .jm-calendar__month')", 12)
time.sleep(0.8)


def cal_state(i=0):
    raw = tab.js(
        f"""(()=>{{
          const cal=document.querySelectorAll('.jm-calendar')[{i}];
          const vp=cal.querySelector('.jm-calendar__viewport');
          const label=cal.querySelector('.jm-calendar__month-text')||cal.querySelector('.jm-calendar__month');
          const first=vp.querySelector('.jm-calendar__month');
          return JSON.stringify({{
            label: label?label.textContent.trim():null,
            scrollTop: Math.round(vp.scrollTop),
            monthH: first?first.offsetHeight:0,
            months: vp.querySelectorAll('.jm-calendar__month').length,
            viewportH: vp.clientHeight,
          }});
        }})()"""
    )
    return json.loads(raw)


st = cal_state(0)
print("    [dbg]", st)
check("calendar-scroll", "viewport renders months", st["months"] > 1, True)
# 跨月格去掉后月高随实际行数收缩（4~6 行），viewport 固定 6 行高：一个月高 ≤ viewport ≤ 月高+一行
check(
    "calendar-scroll",
    "viewport ~ one month tall",
    0 < st["monthH"] <= st["viewportH"] <= st["monthH"] + 64,
    True,
)

# 各月高度应随行数不同而不同（首月 6 行的话，找一个 5 行/4 行的月份对比）
heights = json.loads(
    tab.js(
        """(()=>{
          const cal=document.querySelector('.jm-calendar');
          return JSON.stringify([...cal.querySelectorAll('.jm-calendar__month')].map(m=>m.offsetHeight));
        })()"""
    )
)
check("calendar-scroll", "month heights vary with rows", len(set(heights)) > 1 or len(heights) <= 1, True)

# 月份分隔标题：数量与月份节一致，第二条是下个月
titles = json.loads(
    tab.js(
        """(()=>{
          const cal=document.querySelector('.jm-calendar');
          const t=[...cal.querySelectorAll('.jm-calendar__month-title')];
          return JSON.stringify({n: t.length, second: t[1]?t[1].textContent.trim():null});
        })()"""
    )
)
check("calendar-title", "month title per section", titles["n"] == st["months"], True)
check("calendar-title", "second month labeled", titles["second"], "2026年6月")

# 向下滚两个月 → 副标题跟随
raw = tab.js(
    """(()=>{
      const cal=document.querySelector('.jm-calendar');
      const vp=cal.querySelector('.jm-calendar__viewport');
      const h=vp.querySelector('.jm-calendar__month').offsetHeight;
      vp.scrollTop = h*2;
      return 'ok';
    })()"""
)
time.sleep(0.6)
st2 = cal_state(0)
check("calendar-scroll", "scroll updates subtitle", st2["label"] not in (None, st["label"]) and st2["scrollTop"] > 0, True)

# 滚回顶部 → 回到最小月（滚动区顶 = min-date 所在月）
tab.js("document.querySelector('.jm-calendar .jm-calendar__viewport').scrollTop = 0")
time.sleep(0.6)
st3 = cal_state(0)
check("calendar-scroll", "scroll top reaches min month", "2026年5月" in (st3["label"] or ""), True)

# 箭头：平滑滚一个月
cal0_center = json.loads(
    tab.js(
        """(()=>{const el=document.querySelector('.jm-calendar .jm-calendar__viewport');
          const r=el.getBoundingClientRect();return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()"""
    )
)
arrow_next = json.loads(
    tab.js(
        """(()=>{const cal=document.querySelector('.jm-calendar');
          const b=cal.querySelector('.jm-calendar__arrow[aria-label="下个月"]');
          const r=b.getBoundingClientRect();return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()"""
    )
)
mouse_click(int(arrow_next["x"]), int(arrow_next["y"]))
time.sleep(0.9)
st4 = cal_state(0)
check("calendar-scroll", "next arrow advances one month", st4["label"] != st["label"], True)
mouse_click(int(json.loads(tab.js("""(()=>{const cal=document.querySelector('.jm-calendar');
  const b=cal.querySelector('.jm-calendar__arrow[aria-label="上个月"]');
  const r=b.getBoundingClientRect();return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()"""))["x"]),
    int(json.loads(tab.js("""(()=>{const cal=document.querySelector('.jm-calendar');
  const b=cal.querySelector('.jm-calendar__arrow[aria-label="上个月"]');
  const r=b.getBoundingClientRect();return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()"""))["y"]))
time.sleep(0.9)

# 横滑翻月（真实鼠标拖拽）
mouse_drag(int(cal0_center["x"]), int(cal0_center["y"]), -90, 0)
time.sleep(0.7)
st5 = cal_state(0)
check("calendar-swipe", "horizontal drag flips month", st5["label"] != st4["label"], True)

# ============ 2. poppable 弹出模式 ============
print("== calendar poppable ==")
open_res = tab.js(
    """(()=>{
      const btn=[...document.querySelectorAll('.demo-page button')].find(b=>b.textContent.includes('底部弹出'));
      if(!btn) return 'no-btn';
      btn.click();
      return 'ok';
    })()"""
)
check("calendar-poppable", "open button found", open_res, "ok")

# iOS 首帧规避：打开后立刻（不等动画）滚动区已渲染、已定位到今天所在月
t0 = time.time()
ok_render = wait_for(
    "!!(()=>{const p=document.querySelector('.jm-popup');return !!p && !!p.querySelector('.jm-calendar__viewport');})()",
    8,
)
check("calendar-poppable", "popup opened", ok_render, True)

st_pop = json.loads(
    tab.js(
        """(()=>{
          const p=document.querySelector('.jm-popup');
          const cal=p.querySelector('.jm-calendar');
          const vp=cal.querySelector('.jm-calendar__viewport');
          const days=vp.querySelector('.jm-calendar__days');
          const label=cal.querySelector('.jm-calendar__month-text')||cal.querySelector('.jm-calendar__month');
          return JSON.stringify({
            daysH: days?days.offsetHeight:0,
            scrollTop: Math.round(vp.scrollTop),
            label: label?label.textContent.trim():null,
            closeBtn: !!p.querySelector('.jm-popup__close'),
            confirm: !!cal.querySelector('.jm-calendar__confirm'),
          });
        })()"""
    )
)
print("    [dbg]", st_pop, "opened at", round(time.time() - t0, 2), "s")
check("calendar-poppable", "content rendered immediately (iOS)", st_pop["daysH"] > 100, True)
check("calendar-poppable", "pre-scrolled to today month (no blank)", st_pop["scrollTop"] > 0, True)
check("calendar-poppable", "subtitle shows current month", "2026年11月" in (st_pop["label"] or ""), True)
check("calendar-poppable", "popup has close & confirm", st_pop["closeBtn"] and st_pop["confirm"], True)

# 高度适配：标题与确认按钮必须同时可见（都落在弹层面板可视范围内）
fit = json.loads(
    tab.js(
        """(()=>{
          const p=document.querySelector('.jm-popup');
          const cal=p.querySelector('.jm-calendar');
          const pr=p.getBoundingClientRect();
          const title=cal.querySelector('.jm-calendar__header').getBoundingClientRect();
          const confirm=cal.querySelector('.jm-calendar__confirm').getBoundingClientRect();
          return JSON.stringify({
            titleVisible: title.top >= pr.top - 1,
            confirmVisible: confirm.bottom <= pr.bottom + 1,
            calH: cal.offsetHeight, panelH: p.clientHeight,
          });
        })()"""
    )
)
print("    [dbg] fit", fit)
check("calendar-poppable", "title visible with confirm", fit["titleVisible"] and fit["confirmVisible"], True)
check("calendar-poppable", "calendar fits panel (no inner scroll)", fit["calH"] <= fit["panelH"] + 1, True)

# 弹层内相对滚一个月（从当前定位处 +1）
tab.js(
    """(()=>{const vp=document.querySelector('.jm-popup .jm-calendar__viewport');
      const h=vp.querySelector('.jm-calendar__month').offsetHeight;
      vp.scrollTop = vp.scrollTop + h; return 'ok';})()"""
)
time.sleep(0.6)
label2 = tab.js(
    "(()=>{const cal=document.querySelector('.jm-popup .jm-calendar');"
    "const l=cal.querySelector('.jm-calendar__month-text')||cal.querySelector('.jm-calendar__month');"
    "return l?l.textContent.trim():null;})()"
)
check("calendar-poppable", "scroll inside popup updates subtitle", "2026年12月" in (label2 or ""), True)

# 选一天（限定今天所在的 11 月节，避免命中其他月份的同名日期）+ 确认 → 弹层关闭、demo 记录更新
sel = tab.js(
    """(()=>{
      const sec=document.querySelector('.jm-popup .jm-calendar__month[data-mi="6"]');
      if(!sec) return 'no-sec';
      const days=[...sec.querySelectorAll('.jm-calendar__day')];
      const d=days.find(x=>x.textContent.trim()==='20' && !x.disabled && x.classList.contains('is-current'));
      if(!d) return 'no-day';
      d.click();
      return 'ok';
    })()"""
)
check("calendar-poppable", "pick a day", sel, "ok")
time.sleep(0.3)
selected_now = tab.js(
    "(()=>{const d=document.querySelector('.jm-popup .jm-calendar__day.is-selected');return d?d.textContent.trim():null;})()"
)
check("calendar-poppable", "day selected ring", selected_now, "20")

tab.js(
    "(()=>{const b=document.querySelector('.jm-popup .jm-calendar__confirm');if(b)b.click();else return 'no-btn';})()"
)
time.sleep(1.0)
closed = tab.js("(()=>{return !document.querySelector('.jm-popup');})()")
check("calendar-poppable", "confirm closes popup", bool(closed), True)
note = tab.js(
    "[...document.querySelectorAll('.demo-note')].map(n=>n.textContent).join('|')"
)
check("calendar-poppable", "result note updated", "11月20日" in (note or ""), True)

# ============ 3. poppable 区间日历的滚动边界钳制 ============
print("== calendar poppable bounds ==")
open2 = tab.js(
    """(()=>{
      if(document.querySelector('.jm-popup')) return 'popup-left-open';
      const btn=[...document.querySelectorAll('.demo-page button')].find(b=>b.textContent.includes('请假区间'));
      if(!btn) return 'no-btn';
      btn.click();
      return 'ok';
    })()"""
)
check("calendar-poppable", "range popup opened", open2, "ok")
wait_for("document.querySelectorAll('.jm-popup').length > 0", 8)
time.sleep(0.8)
bounds = json.loads(
    tab.js(
        """(()=>{
          const cal=document.querySelector('.jm-popup .jm-calendar');
          if(!cal) return JSON.stringify({err:'no-popup'});
          const vp=cal.querySelector('.jm-calendar__viewport');
          const label=cal.querySelector('.jm-calendar__month-text')||cal.querySelector('.jm-calendar__month');
          return JSON.stringify({topLabel: label.textContent.trim(), months: vp.querySelectorAll('.jm-calendar__month').length});
        })()"""
    )
)
print("    [dbg]", bounds)
check("calendar-poppable", "range calendar min bound", "2026年11月" in (bounds.get("topLabel") or ""), True)
check("calendar-poppable", "range calendar months 2026-11~2027-12", bounds.get("months"), 14)

# 滚到底 → 2027年12月
tab.js("document.querySelector('.jm-popup .jm-calendar__viewport').scrollTop = 99999")
time.sleep(0.6)
bottom_label = tab.js(
    "(()=>{const cal=document.querySelector('.jm-popup .jm-calendar');"
    "const l=cal.querySelector('.jm-calendar__month-text')||cal.querySelector('.jm-calendar__month');"
    "return l?l.textContent.trim():null;})()"
)
check("calendar-poppable", "range calendar max bound", "2027年12月" in (bottom_label or ""), True)

# 关闭
tab.js(
    "(()=>{const b=document.querySelector('.jm-popup .jm-popup__close');if(b)b.click();})()"
)
time.sleep(0.6)

errs = tab.js("JSON.stringify(window.__errs||[])")
check("errors", "no page errors", errs, "[]")

tab.shot(OUT + r"\cal_scroll_poppable.png")
print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
