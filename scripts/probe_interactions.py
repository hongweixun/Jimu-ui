"""交互功能回归：手势、点击、拖拽、加载，全部用合成 PointerEvent 在真实页面里跑。"""
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
    good = actual == expect or (isinstance(expect, tuple) and actual in expect) or (
        callable(expect) and expect(actual)
    )
    if good:
        ok += 1
        print(f"  PASS {page}/{name}: {json.dumps(actual, ensure_ascii=False)[:120]}")
    else:
        fail += 1
        print(f"  FAIL {page}/{name}: got {json.dumps(actual, ensure_ascii=False)[:200]}, want {expect}")


def drag(selector, dx, dy, steps=8, hold=0.03, offset_x=None, offset_y=None):
    """在元素中心按住并拖动，模拟 pointerdown → move… → up"""
    expr = f"""
    (async () => {{
      const el = document.querySelector('{selector}');
      if (!el) return 'no-el';
      const r = el.getBoundingClientRect();
      const x0 = {offset_x if offset_x is not None else "r.left + r.width/2"};
      const y0 = {offset_y if offset_y is not None else "r.top + r.height/2"};
      const opts = (x, y, type) => new PointerEvent(type, {{bubbles:true, cancelable:true, pointerId:9, pointerType:'touch', isPrimary:true, clientX:x, clientY:y, buttons:1}});
      el.dispatchEvent(opts(x0, y0, 'pointerdown'));
      for (let i=1;i<={steps};i++) {{
        el.dispatchEvent(opts(x0 + {dx} * i/{steps}, y0 + {dy} * i/{steps}, 'pointermove'));
        await new Promise(r => setTimeout(r, {int(hold*1000)}));
      }}
      el.dispatchEvent(opts(x0 + {dx}, y0 + {dy}, 'pointerup'));
      return 'done';
    }})()
    """
    return tab.js(expr)


def sleep(sec):
    time.sleep(sec)


# ---------------- Grid ----------------
tab.goto(f"{BASE}/components/grid", wait=2.5)
tab.js("document.querySelectorAll('.jm-grid__item')[1].dispatchEvent(new MouseEvent('click',{bubbles:true}))")
sleep(0.3)
check("grid", "click 2nd updates note", "课程" in str(tab.js("document.body.innerText.match(/最近点击：[^\\n]*/)?.[0]")), True)

# ---------------- Swipe ----------------
tab.goto(f"{BASE}/components/swipe", wait=2.5)
root_sel = ".jm-swipe"
def px(v):
    try:
        return float(str(v).split("(")[1].split("px")[0])
    except Exception:
        return None

t0 = px(tab.js("document.querySelector('.jm-swipe__track').style.transform"))
drag(root_sel, -200, 0)
sleep(0.6)
t1 = px(tab.js("document.querySelector('.jm-swipe__track').style.transform"))
check("swipe", "drag left advances one page", t1, t0 - 308)
drag(root_sel, 200, 0)
sleep(0.6)
t2 = px(tab.js("document.querySelector('.jm-swipe__track').style.transform"))
check("swipe", "drag right returns", t2, t0)
# 点击指示点跳转
tab.js("[...document.querySelectorAll('.jm-swipe')][0].querySelectorAll('.jm-swipe__dot')[2].click()")
sleep(0.6)
check("swipe", "dot click go to 3rd", tab.js("[...document.querySelectorAll('.jm-swipe')][0].querySelector('.jm-swipe__dot.is-active') === [...document.querySelectorAll('.jm-swipe')][0].querySelectorAll('.jm-swipe__dot')[2]"), True)
# 从第 3 张继续往后翻 → 循环归位到第 1 张
drag(root_sel, -260, 0)
sleep(0.8)
idx_after = tab.js("[...[...document.querySelectorAll('.jm-swipe')][0].querySelectorAll('.jm-swipe__dot')].findIndex(d=>d.classList.contains('is-active'))")
check("swipe", "loop wraps 3 -> 1", idx_after, 0)

# ---------------- Picker ----------------
tab.goto(f"{BASE}/components/picker", wait=2.5)
tab.js("document.querySelector('.jm-cell.is-clickable').click()")
sleep(0.5)
check("picker", "popup opens", tab.js("!!document.querySelector('.jm-picker__columns')"), True)
# 拖动年份列：向下拖 = 往前翻（值变小）
drag(".jm-picker-column", 0, 88)
sleep(0.8)
check("picker", "column drag changes selection", tab.js("document.querySelector('.jm-picker-column__item.is-selected')?.textContent?.trim()"), "2024")
# 点击选项切换
tab.js("[...document.querySelectorAll('.jm-picker-column')][1].querySelectorAll('.jm-picker-column__item')[4].click()")
sleep(0.5)
check("picker", "click option selects", tab.js("[...document.querySelectorAll('.jm-picker-column')][1].querySelector('.is-selected')?.textContent?.trim()"), "05")
tab.js("document.querySelector('.jm-picker__action.is-confirm').click()")
sleep(0.5)
check("picker", "confirm closes & syncs cell", "2024-05" in str(tab.js("document.querySelector('.jm-cell__value')?.textContent")), True)

# ---------------- Uploader ----------------
tab.goto(f"{BASE}/components/uploader", wait=2.5)
n0 = tab.js("document.querySelectorAll('.jm-uploader')[0].querySelectorAll('.jm-uploader__item').length")
tab.js("document.querySelectorAll('.jm-uploader')[0].querySelector('.jm-uploader__delete').click()")
sleep(0.4)
n1 = tab.js("document.querySelectorAll('.jm-uploader')[0].querySelectorAll('.jm-uploader__item').length")
check("uploader", "delete removes item", n1, n0 - 1)
tab.js("document.querySelectorAll('.jm-uploader')[0].querySelector('.jm-uploader__thumb').click()")
sleep(0.5)
check("uploader", "preview popup shows", tab.js("!!document.querySelector('.jm-uploader__preview')"), True)
tab.js("document.querySelector('.jm-popup__mask')?.click()")
sleep(0.5)
check("uploader", "preview closes", tab.js("!document.querySelector('.jm-uploader__preview')"), True)

# ---------------- PullRefresh ----------------
tab.goto(f"{BASE}/components/pull-refresh", wait=2.5)
st0 = tab.js("document.querySelector('.jm-pull-refresh__head').className")
drag(".jm-pull-refresh", 0, 150, steps=10, offset_y=30)
sleep(0.4)
st1 = tab.js("document.querySelector('.jm-pull-refresh__head').className")
check("pull-refresh", "drag down enters loading", "is-loading" in st1, True)
sleep(2.5)
rows = tab.js("document.querySelectorAll('.jm-pull-refresh')[0].querySelectorAll('.row').length")
check("pull-refresh", "refresh rebuilds items", rows, 12)
check("pull-refresh", "head resets", tab.js("document.querySelector('.jm-pull-refresh__head').className"), st0)

# ---------------- List ----------------
tab.goto(f"{BASE}/components/list", wait=2.5)
r0 = tab.js("document.querySelectorAll('.jm-list .row').length")
tab.js("const s=document.querySelector('.scroller'); s.scrollTop = s.scrollHeight")
sleep(2.0)
r1 = tab.js("document.querySelectorAll('.jm-list .row').length")
check("list", "scroll to bottom loads more", r1 > r0, True)

print(f"\nRESULT: {ok} passed, {fail} failed")
tab.ws.close()
