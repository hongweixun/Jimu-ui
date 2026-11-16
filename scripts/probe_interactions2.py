"""第三批（ImagePreview / Calendar / CascadePicker）交互回归。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
ensure_edge()
tab = new_tab()
ok = fail = 0


def check(page, name, actual, expect):
    global ok, fail
    good = (
        actual == expect
        or (isinstance(expect, tuple) and actual in expect)
        or (callable(expect) and expect(actual))
    )
    if good:
        ok += 1
        print(f"  PASS {page}/{name}: {json.dumps(actual, ensure_ascii=False)[:110]}")
    else:
        fail += 1
        print(f"  FAIL {page}/{name}: got {json.dumps(actual, ensure_ascii=False)[:200]}, want {expect}")


def drag(selector, dx, dy, steps=8, hold=0.03, index=0):
    expr = f"""
    (async () => {{
      const el = document.querySelectorAll('{selector}')[{index}];
      if (!el) return 'no-el';
      const r = el.getBoundingClientRect();
      const x0 = r.left + r.width/2, y0 = r.top + r.height/2;
      const ev = (x, y, type) => new PointerEvent(type, {{bubbles:true, cancelable:true, pointerId:7, pointerType:'touch', isPrimary:true, clientX:x, clientY:y, buttons:1}});
      el.dispatchEvent(ev(x0, y0, 'pointerdown'));
      for (let i=1;i<={steps};i++) {{
        el.dispatchEvent(ev(x0 + {dx}*i/{steps}, y0 + {dy}*i/{steps}, 'pointermove'));
        await new Promise(r => setTimeout(r, {int(hold*1000)}));
      }}
      el.dispatchEvent(ev(x0 + {dx}, y0 + {dy}, 'pointerup'));
      return 'done';
    }})()
    """
    return tab.js(expr)


# ---------------- Calendar ----------------
tab.goto(f"{BASE}/components/calendar", wait=3)
before = tab.js("document.querySelector('.jm-calendar__summary')?.textContent")
tab.js("document.querySelectorAll('.jm-calendar')[0].querySelectorAll('.jm-calendar__day')[20].click()")
time.sleep(0.4)
after = tab.js("document.querySelector('.jm-calendar__summary')?.textContent")
check("calendar", "single select updates summary", before != after and bool(after), True)
check("calendar", "selected cell moved", tab.js("document.querySelectorAll('.jm-calendar')[0].querySelectorAll('.jm-calendar__day.is-selected').length"), 1)

# 区间：点两天应出现区间带
tab.js("""
(()=>{const c=document.querySelectorAll('.jm-calendar')[1];
 const d=[...c.querySelectorAll('.jm-calendar__day')].filter(x=>x.classList.contains('is-current'));
 d[5].click(); d[9].click(); return d.length})()
""")
time.sleep(0.4)
band = tab.js("document.querySelectorAll('.jm-calendar')[1].querySelectorAll('.jm-calendar__day.is-in-range').length")
check("calendar", "range band renders between days", band, 3)
check("calendar", "range summary", tab.js("document.querySelectorAll('.jm-calendar__summary')[1]?.textContent"), lambda v: "-" in str(v))

# 翻月
m0 = tab.js("document.querySelectorAll('.jm-calendar')[0].querySelector('.jm-calendar__month').textContent")
tab.js("document.querySelectorAll('.jm-calendar')[0].querySelectorAll('.jm-calendar__arrow')[1].click()")
time.sleep(0.3)
m1 = tab.js("document.querySelectorAll('.jm-calendar')[0].querySelector('.jm-calendar__month').textContent")
check("calendar", "next month", (m0, m1), ("2026年11月", "2026年12月"))

# 禁用范围
tab.js("""
(()=>{const c=document.querySelectorAll('.jm-calendar')[2];
 const d=[...c.querySelectorAll('.jm-calendar__day')].filter(x=>x.classList.contains('is-current'));
 d[2].click(); return d[2].disabled})()
""")
time.sleep(0.3)
check("calendar", "min-date disables early days", tab.js("document.querySelectorAll('.jm-calendar')[2].querySelectorAll('.jm-calendar__day.is-disabled').length"), lambda v: v > 0)
check("calendar", "disabled day not selected", tab.js("document.querySelectorAll('.jm-calendar')[2].querySelectorAll('.jm-calendar__day.is-selected').length"), 1)

# 触摸轻点带漂移：必须选中「按下的那一天」——WebView 常把 click 吞掉或派给相邻格
tab.js("[...document.querySelectorAll('.jm-calendar')][2].scrollIntoView({block:'center'})")
time.sleep(0.4)
pos = json.loads(
    tab.js(
        """
(()=>{const c=document.querySelectorAll('.jm-calendar')[2]
 const btn=[...c.querySelectorAll('.jm-calendar__day')].find(b=>b.classList.contains('is-current')&&b.querySelector('.jm-calendar__day-text')?.textContent.trim()==='20')
 const r=btn.getBoundingClientRect()
 return JSON.stringify({x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2)})})()
"""
    )
)
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": pos["x"], "y": pos["y"]}]})
time.sleep(0.05)
tab.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": pos["x"] + 20, "y": pos["y"]}]})
time.sleep(0.06)
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.35)
picked = tab.js(
    """JSON.stringify([...document.querySelectorAll('.jm-calendar')[2]
 .querySelectorAll('.jm-calendar__day.is-selected .jm-calendar__day-text')].map(e=>e.textContent.trim()))"""
)
check("calendar", "touch tap with 20px drift selects pressed day", picked, lambda v: '"20"' in str(v))

# 横滑翻月：60px 左滑 → 下一月，且不误选日期
m_sw_before = tab.js("document.querySelectorAll('.jm-calendar')[2].querySelector('.jm-calendar__month').textContent")
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": pos["x"], "y": pos["y"]}]})
time.sleep(0.05)
tab.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": pos["x"] - 30, "y": pos["y"]}]})
time.sleep(0.04)
tab.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": pos["x"] - 60, "y": pos["y"]}]})
time.sleep(0.06)
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.5)
m_sw_after = tab.js("document.querySelectorAll('.jm-calendar')[2].querySelector('.jm-calendar__month').textContent")
check("calendar", "swipe left flips to next month", (m_sw_before, m_sw_after), ("2026年11月", "2026年12月"))

# ---------------- CascadePicker ----------------
tab.goto(f"{BASE}/components/cascade-picker", wait=3)
check("cascade", "inline picker columns", tab.js("document.querySelectorAll('.jm-picker-column').length"), 3)
check("cascade", "column1 first item", tab.js("document.querySelectorAll('.jm-picker-column')[0].querySelector('.jm-picker-column__item')?.textContent?.trim()"), "浙江省")
tab.js("document.querySelector('.jm-cell.is-clickable').click()")
time.sleep(0.5)
# 向上拖 44px = 换到下一项（江苏省）
drag(".jm-picker-column", 0, -44, steps=6)
time.sleep(0.8)
check("cascade", "drag level1 rebuilds level2", tab.js("[...document.querySelector('.jm-popup .jm-picker__columns').querySelectorAll('.jm-picker-column')].map(c=>c.querySelector('.jm-picker-column__item.is-selected')?.textContent?.trim())"), ["江苏省", "南京市", "鼓楼区"])
tab.js("document.querySelector('.jm-picker__action.is-confirm').click()")
time.sleep(0.5)
check("cascade", "confirm syncs cell label", tab.js("document.querySelector('.jm-cell__value')?.textContent"), "江苏省 / 南京市 / 鼓楼区")

# ---------------- ImagePreview ----------------
tab.goto(f"{BASE}/components/image-preview", wait=3)
tab.js("document.querySelectorAll('.jm-image')[0].dispatchEvent(new MouseEvent('click',{bubbles:true}))")
time.sleep(0.6)
check("preview", "opens on first thumb", tab.js("!!document.querySelector('.jm-image-preview')"), True)
check("preview", "index label", tab.js("document.querySelector('.jm-image-preview__index')?.textContent?.trim()"), "1 / 4")
drag(".jm-image-preview", -220, 0, steps=8)
time.sleep(0.6)
check("preview", "swipe to next", tab.js("document.querySelector('.jm-image-preview__index')?.textContent?.trim()"), "2 / 4")
tab.js("document.querySelector('.jm-image-preview__close').click()")
time.sleep(0.5)
check("preview", "close button hides", tab.js("!document.querySelector('.jm-image-preview')"), True)
# 函数式
tab.js("document.querySelectorAll('.demo-row .jm-button')[1].click()")
time.sleep(0.7)
check("preview", "function api opens at startPosition", tab.js("document.querySelector('.jm-image-preview__index')?.textContent?.trim()"), "3 / 4")
tab.js("document.querySelector('.jm-image-preview__dots .jm-image-preview__dot')?.click()")
time.sleep(0.5)
check("preview", "dot jump", tab.js("document.querySelector('.jm-image-preview__index')?.textContent?.trim()"), "1 / 4")

print(f"\nRESULT: {ok} passed, {fail} failed")
tab.ws.close()
