#!/usr/bin/env python3
"""日历 0.25.3 排版验证：TDesign 方格布局 / 今天二字 / 备注独立行 / demo 卡片页"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab  # noqa: E402

ensure_edge()
tab = new_tab()
OUT = r"E:\jimu-ui\scripts\shots"

tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
# 手机宽度视口，贴近文档站手机模拟器
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


def wait_for(expr, timeout=12.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.2)
    return False


def js_click(sel):
    tab.js(
        "(()=>{const el=document.querySelector(" + json.dumps(sel) + ");"
        "if(!el)return 'null';"
        "const r=el.getBoundingClientRect();"
        "const ev=new MouseEvent('click',{bubbles:true,cancelable:true,clientX:r.left+r.width/2,clientY:r.top+r.height/2});"
        "el.dispatchEvent(ev);return 'ok';})()"
    )


print("== goto calendar demo ==")
goto("/components/calendar")
ok = wait_for("!!document.querySelector('.jm-calendar__days') && !!document.querySelector('.phone__screen')")
check("page", "calendar rendered in phone", ok, True)
time.sleep(1.0)

# 滚动到第一个日历
tab.js("document.querySelector('.jm-calendar').scrollIntoView({block:'start'})")
time.sleep(0.8)

info = tab.js(
    """(()=>{
      const cals=[...document.querySelectorAll('.jm-calendar')];
      const cal=cals[0]; if(!cal) return 'null';
      const todayCell=cal.querySelector('.jm-calendar__day.is-today');
      const selCell=cal.querySelector('.jm-calendar__day.is-selected');
      const marked=cal.querySelector('.jm-calendar__day-info.is-bottom:not(:empty)');
      const weekdays=cal.querySelector('.jm-calendar__weekdays');
      return JSON.stringify({
        cals: cals.length,
        todayText: todayCell ? todayCell.querySelector('.jm-calendar__day-text').textContent.trim() : null,
        todayHasBottom: todayCell ? !!todayCell.querySelector('.jm-calendar__day-info.is-bottom').textContent.trim() : null,
        selText: selCell ? selCell.querySelector('.jm-calendar__day-text').textContent.trim() : null,
        markedText: marked ? marked.textContent.trim() : null,
        markedIsFlow: marked ? getComputedStyle(marked).position : null,
        weekdayFs: weekdays ? getComputedStyle(weekdays.querySelector('.jm-calendar__weekday')).fontSize : null,
      });
    })()"""
)
print("info:", info)
d = json.loads(info)
check("layout", "today shows 今天 instead of number", d["todayText"], "今天")
check("layout", "today has no 今 below number", d["todayHasBottom"], False)
check("layout", "marked info is in normal flow (independent row)", d["markedIsFlow"], "static")
check("layout", "weekday header font bumped", d["weekdayFs"], "13px")

# 备注与数字不重叠：可约小字 top >= 数字圆底
gap = tab.js(
    """(()=>{
      const cal=document.querySelectorAll('.jm-calendar')[0];
      const day=cal.querySelector('.jm-calendar__day-info.is-bottom:not(:empty)').closest('.jm-calendar__day');
      const main=day.querySelector('.jm-calendar__day-text').getBoundingClientRect();
      const info=day.querySelector('.jm-calendar__day-info.is-bottom').getBoundingClientRect();
      return JSON.stringify({clear: info.top >= main.bottom - 1, gap: +(info.top-main.bottom).toFixed(1)});
    })()"""
)
print("gap:", gap)
g = json.loads(gap)
check("layout", "bottom info clear of number", g["clear"], True)

tab.js("document.querySelector('.jm-calendar').scrollIntoView({block:'start'})")
time.sleep(0.6)
tab.shot(OUT + r"\cal_card1.png")

# 区间卡
rng = tab.js(
    """(()=>{
      const cals=[...document.querySelectorAll('.jm-calendar')];
      const cal=cals.find(c=>c.querySelector('.jm-calendar__day.is-in-range'));
      if(!cal) return 'null';
      const band=cal.querySelector('.jm-calendar__day.is-in-range .jm-calendar__day-main');
      const br=band.getBoundingClientRect();
      const num=band.querySelector('.jm-calendar__day-text').getBoundingClientRect();
      return JSON.stringify({bandH: +br.height.toFixed(0), numH: +num.height.toFixed(0)});
    })()"""
)
print("range:", rng)
tab.js("const c=[...document.querySelectorAll('.jm-calendar')].find(c=>c.querySelector('.jm-calendar__day.is-in-range')); c.scrollIntoView({block:'start'})")
time.sleep(0.6)
tab.shot(OUT + r"\cal_card2.png")

# 多选卡（橙色）
tab.js("[...document.querySelectorAll('.jm-calendar')].pop().scrollIntoView({block:'start'})")
time.sleep(0.6)
tab.shot(OUT + r"\cal_card3.png")

# 整页全景
tab.js("window.scrollTo(0,0); const p=document.querySelector('.phone__screen'); if(p) p.scrollTop=0;")
time.sleep(0.5)
tab.shot(OUT + r"\cal_page_top.png")
tab.js("const p=document.querySelector('.phone__screen'); if(p) p.scrollTop=p.scrollHeight;")
time.sleep(0.5)
tab.shot(OUT + r"\cal_page_bottom.png")

print(f"\n{passed} passed, {len(failed)} failed: {failed}")
