"""第九批（VirtualList 虚拟列表 / Uploader 拖拽排序）交互回归。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
results = []


def check(name, desc, actual, expect):
    ok = actual == expect
    results.append((name, desc, ok, actual, expect))
    print(("PASS" if ok else "FAIL"), name, "-", desc, "" if ok else f"\n   actual={actual!r} expect={expect!r}")


def count(tab, sel):
    return tab.js(f"document.querySelectorAll({json.dumps(sel)}).length")


def text_of(tab, sel, index=0):
    return tab.js(f"document.querySelectorAll({json.dumps(sel)})[{index}]?.textContent?.trim()")


def click_by_text(tab, sel, keyword):
    tab.js(
        f"[...document.querySelectorAll({json.dumps(sel)})]"
        f".find(e=>e.textContent.trim() === {json.dumps(keyword)})"
        f"?.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))"
    )


def press(tab, x, y):
    tab.js(
        f"""
    (() => {{
      const el = document.elementFromPoint({x}, {y})
      if (!el) return
      const mk = (t, cx, cy) => new PointerEvent(t, {{
        bubbles: true, pointerId: 9, isPrimary: true,
        pointerType: 'touch', clientX: cx, clientY: cy, button: 0, buttons: 1,
      }})
      el.dispatchEvent(mk('pointerdown', {x}, {y}))
    }})()
    """
    )


def drag_step(tab, x, y, up=False):
    tab.js(
        f"""
    (() => {{
      const el = document.elementFromPoint({x}, {y}) || document
      const mk = (t, cx, cy) => new PointerEvent(t, {{
        bubbles: true, pointerId: 9, isPrimary: true,
        pointerType: 'touch', clientX: cx, clientY: cy, button: 0, buttons: t === 'pointerup' ? 0 : 1,
      }})
      el.dispatchEvent(mk({json.dumps('pointerup' if up else 'pointermove')}, {x}, {y}))
      document.dispatchEvent(mk({json.dumps('pointerup' if up else 'pointermove')}, {x}, {y}))
    }})()
    """
    )


def drag(tab, x0, y0, x1, y1, steps=8):
    press(tab, x0, y0)
    time.sleep(0.55)  # 等长按 420ms 激活
    for i in range(1, steps + 1):
        x = x0 + (x1 - x0) * i / steps
        y = y0 + (y1 - y0) * i / steps
        drag_step(tab, int(x), int(y))
        time.sleep(0.03)
    drag_step(tab, x1, y1, up=True)


ensure_edge()
tab = new_tab()

# ---------- VirtualList ----------
tab.goto(f"{BASE}/components/virtual-list", wait=3)
check("vlist", "demo 渲染了可视区行（远小于 2000）", 8 <= count(tab, ".jm-virtual-list__item") <= 40, True)
check("vlist", "内容总高度 = 2000 * 56", tab.js("document.querySelector('.jm-virtual-list__content')?.style.height"), "112000px")
check("vlist", "首行编号 1", tab.js("document.querySelector('.jm-virtual-list__item .row__avatar')?.textContent?.trim()"), "1")
click_by_text(tab, ".demo-page .jm-button", "跳到第 1501 行")
time.sleep(0.4)
check("vlist", "scrollToIndex(1500) 后渲染起点=1500-overscan5", tab.js("document.querySelector('.jm-virtual-list__item .row__avatar')?.textContent?.trim()"), "1496")
# 滚动到底触发 scroll-bottom 场景：直接操作滚动容器
tab.js("document.querySelector('.jm-virtual-list').scrollTop = 112000")
time.sleep(0.4)
check("vlist", "滚到底后渲染末尾区间(含 overscan)", tab.js("document.querySelector('.jm-virtual-list__item .row__avatar')?.textContent?.trim()"), "1991")

# ---------- Uploader 拖拽排序 ----------
tab.goto(f"{BASE}/components/uploader", wait=3)
check("uploader", "排序 demo 存在", tab.js("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('长按缩略图'))"), True)

# 定位排序 demo 中第一张缩略图的视口坐标，拖到第三格
tab.js("[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))?.scrollIntoView({block:'center'})")
time.sleep(0.4)
geo = tab.js(
    """
(() => {
  const p = [...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))
  if (!p) return null
  const items = [...p.querySelectorAll('.jm-uploader__item')]
  if (items.length < 5) return null
  const a = items[0].getBoundingClientRect()
  const b = items[2].getBoundingClientRect()
  return JSON.stringify({
    x0: Math.round(a.left + a.width/2), y0: Math.round(a.top + a.height/2),
    x1: Math.round(b.left + b.width/2), y1: Math.round(b.top + b.height/2),
  })
})()
"""
)
if geo and geo != "null":
    import json as _json
    g = _json.loads(geo)
    check("uploader", "拖拽前第一格缩略图 URL", tab.js(
        "[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))"
        ".querySelectorAll('.jm-uploader__item img')[0].src.split('/').slice(-3)[0]"
    ), "jm-a")
    drag(tab, g["x0"], g["y0"], g["x1"], g["y1"])
    time.sleep(0.6)
    check("uploader", "拖拽后顺序变化", tab.js(
        "[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))"
        ".querySelectorAll('.jm-uploader__item img')[2].src.split('/').slice(-3)[0]"
    ), "jm-a")
    check("uploader", "拖拽后第一格变为 jm-b", tab.js(
        "[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))"
        ".querySelectorAll('.jm-uploader__item img')[0].src.split('/').slice(-3)[0]"
    ), "jm-b")
    check("uploader", "无残留让位 transform", tab.js(
        "[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('长按缩略图'))"
        ".querySelectorAll('.jm-uploader__item')[0].style.transform === ''"
    ), True)
else:
    check("uploader", "定位拖拽坐标", False, True)

# ---------- 汇总 ----------
print()
print("=" * 46)
total = len(results)
passed = sum(1 for r in results if r[2])
print(f"共 {total} 项，通过 {passed}，失败 {total - passed}")
sys.exit(0 if passed == total else 1)
