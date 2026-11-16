"""常用组件补充批：Card 卡片 / Descriptions 描述列表 / Tooltip 文字提示。"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
ensure_edge()
tab = new_tab()
ok = fail = 0


def check(section, name, actual, expect):
    global ok, fail
    good = (
        actual == expect
        or (isinstance(expect, tuple) and actual in expect)
        or (callable(expect) and expect(actual))
    )
    if good:
        ok += 1
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False, default=str)[:120]}")
    else:
        fail += 1
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False, default=str)[:220]}, want {expect}")


def wait_demo(text, timeout=15):
    """滚到含 text 的 demo 并等它出现（首访页面 Vite 冷编译可能较慢）"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        n = tab.js(
            "[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes("
            + json.dumps(text, ensure_ascii=False)
            + "))"
        )
        if n:
            tab.js(
                "(()=>{const p=[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes("
                + json.dumps(text, ensure_ascii=False)
                + "));p.scrollIntoView({block:'center'});})()"
            )
            time.sleep(0.6)
            return True
        time.sleep(1)
    return False


def center_of(selector_js):
    return tab.js(
        "(()=>{const el=" + selector_js + ";if(!el)return null;"
        "const r=el.getBoundingClientRect();"
        "return {x:r.left+r.width/2, y:r.top+r.height/2};})()"
    )


def hover(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x - 60, "y": y - 60})
    time.sleep(0.15)
    tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    time.sleep(0.6)


def panels():
    return tab.js(
        "[...document.querySelectorAll('.jm-tooltip__panel')].map(p=>(p.textContent||'').trim().slice(0,20))"
    )


# ============================ Card ============================
tab.goto(f"{BASE}/components/card", wait=6)
check("card", "page has demos", wait_demo("零基础学 Vue 3"), True)
time.sleep(1)

info = tab.js(
    """(()=>{const cards=[...document.querySelectorAll('.jm-card')];
return {
  total: cards.length,
  top: cards.filter(c=>c.classList.contains('jm-card--top')).length,
  left: cards.filter(c=>c.classList.contains('jm-card--left')).length,
  prices: cards.map(c=>c.querySelector('.jm-card__price-now')?.textContent.trim()).filter(Boolean),
  origins: cards.map(c=>c.querySelector('.jm-card__price-origin')?.textContent.trim()).filter(Boolean),
  tags: [...document.querySelectorAll('.jm-card__tag')].length,
  footers: [...document.querySelectorAll('.jm-card__footer')].length,
  roles: cards.map(c=>c.getAttribute('role')),
  lazy: [...document.querySelectorAll('.jm-card__img')].map(i=>i.getAttribute('loading')),
};})()"""
)
check("card", "5 cards rendered (3 top + 2 left)", (info["top"], info["left"], info["total"]), (3, 2, 5))
check("card", "price formatted", info["prices"], ["¥199.00", "¥128.00", "¥39.90", "¥68.00"])
check("card", "origin price line-through source", info["origins"], ["¥399.00", "¥268.00"])
check("card", "tags rendered", info["tags"], 4)
check("card", "footers rendered", info["footers"], 4)
check("card", "clickable cards are buttons", info["roles"], lambda v: v.count("button") == 4)
check("card", "thumb images lazy", sorted(set(info["lazy"])), ["lazy"])

# left 布局：缩略图固定 96px 宽
lw = tab.js(
    "[...document.querySelectorAll('.jm-card--left .jm-card__thumb')].map(t=>Math.round(t.getBoundingClientRect().width))"
)
check("card", "left thumb fixed width", lw, [96, 96])

# 键盘触发整卡点击：用 list demo 里绑了 @click 的订单卡，看 tip 文本变化
tip_before = tab.js(
    "[...document.querySelectorAll('.demo-tip')].map(t=>t.textContent.trim()).find(t=>t.includes('打开订单')) || ''"
)
tab.js(
    "(()=>{const c=[...document.querySelectorAll('.jm-card')].find(x=>x.textContent.includes('青柠气泡水'));c.focus();})()"
)
tab.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
tab.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
time.sleep(0.3)
tip_after = tab.js(
    "[...document.querySelectorAll('.demo-tip')].map(t=>t.textContent.trim()).find(t=>t.includes('打开订单')) || ''"
)
check("card", "keyboard Enter triggers card click", tip_after != tip_before and "JM20261116001" in tip_after, True)

# ============================ Descriptions ============================
tab.goto(f"{BASE}/components/descriptions", wait=6)
check("desc", "page has demos", wait_demo("订单信息"), True)
time.sleep(1)

info = tab.js(
    """(()=>{const dls=[...document.querySelectorAll('dl.jm-descriptions')];
const first=dls[0];
const labels=[...first.querySelectorAll('dt')];
const values=[...first.querySelectorAll('dd')];
return {
  dls: dls.length,
  labelTag: labels[0]?.tagName,
  valueTag: values[0]?.tagName,
  labelCount: labels.length,
  valueCount: values.length,
  labelX: [...new Set(labels.map(l=>Math.round(l.getBoundingClientRect().left)))],
  colon: getComputedStyle(labels[0], '::after').content,
  border: dls.some(d=>d.classList.contains('is-border')),
  spanValue: [...document.querySelectorAll('.jm-descriptions__value')].map(v=>v.style.gridColumn).filter(s=>s&&s!=='span 1'),
};})()"""
)
check("desc", "dl/dt/dd semantics", (info["labelTag"], info["valueTag"]), ("DT", "DD"))
check("desc", "6 label/value pairs", (info["labelCount"], info["valueCount"]), (6, 6))
check("desc", "labels left-aligned in one column", info["labelX"], lambda v: len(v) == 1)
check("desc", "colon via ::after", info["colon"], '"："')
check("desc", "border mode used", info["border"], True)
check("desc", "span=2 occupies 3 grid columns", info["spanValue"], ["span 3"])

# 两列 demo：第二列的标签与第一列同行且 x 更大
two = tab.js(
    """(()=>{const d=[...document.querySelectorAll('dl.jm-descriptions')][1];
const labels=[...d.querySelectorAll('dt')];
const xs=[...new Set(labels.map(l=>Math.round(l.getBoundingClientRect().left)))];
return {cols: xs.length, align: getComputedStyle(labels[0]).textAlign};})()"""
)
check("desc", "two columns present", two["cols"], 2)
check("desc", "label-align right applied", two["align"], "right")

# vertical：标签在值上方
vert = tab.js(
    """(()=>{const d=[...document.querySelectorAll('dl.jm-descriptions')].find(x=>x.classList.contains('jm-descriptions--vertical'));
const l=d.querySelector('dt'); const v=d.querySelector('dd');
return {vertical: !!d, lAboveV: l.getBoundingClientRect().bottom <= v.getBoundingClientRect().top,
  smallerFont: parseFloat(getComputedStyle(l).fontSize) < parseFloat(getComputedStyle(v).fontSize)};})()"""
)
check("desc", "vertical layout exists", vert["vertical"], True)
check("desc", "label above value", vert["lAboveV"], True)
check("desc", "vertical label font smaller", vert["smallerFont"], True)

# ============================ Tooltip ============================
tab.goto(f"{BASE}/components/tooltip", wait=6)
check("tooltip", "page has demos", wait_demo("纯图标按钮"), True)
time.sleep(1)

# 受控 / 缺省时 show 不应被 Boolean cast 成 false
controlled = tab.js(
    """(()=>{const el=document.querySelector('.demo-page .jm-tooltip');
const c=el.__vueParentComponent;
return {show: c.props.show === undefined ? "__undef__" : c.props.show,
  ariaHidden: el.querySelector('.jm-tooltip__panel') !== null};})()"""
)
check("tooltip", "show prop stays undefined by default", controlled["show"], "__undef__")
check("tooltip", "panel not rendered initially", controlled["ariaHidden"], False)

# hover 出现 / 移开消失
box = center_of("document.querySelector('.demo-page .jm-tooltip')")
hover(box["x"], box["y"])
ps = panels()
check("tooltip", "hover opens panel", ps, ["刷新数据"])
desc_id = tab.js("document.querySelector('.jm-tooltip__panel').id")
linked = tab.js(
    "(()=>{const el=document.querySelector('.jm-tooltip.is-open');"
    "return el && el.getAttribute('aria-describedby') === " + json.dumps(desc_id) + ";})()"
)
check("tooltip", "aria-describedby linked", linked, True)
role = tab.js("document.querySelector('.jm-tooltip__panel').getAttribute('role')")
check("tooltip", "role=tooltip", role, "tooltip")
pe = tab.js("getComputedStyle(document.querySelector('.jm-tooltip__panel')).pointerEvents")
check("tooltip", "panel ignores pointer events", pe, "none")

tab.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 30, "y": 300})
time.sleep(0.4)
check("tooltip", "mouseleave closes panel", panels(), [])

# 四个方向
dirs = tab.js(
    """(()=>{const tips=[...document.querySelectorAll('.jm-tooltip')].filter(t=>/^(top|bottom|left|right)$/.test(t.textContent.trim()));
return tips.map(t=>[t.textContent.trim(), t.className.match(/is-(top|bottom|left|right)/)?.[1]]);})()"""
)
check("tooltip", "four placements", dirs, [["top", "top"], ["bottom", "bottom"], ["left", "left"], ["right", "right"]])

# 自动翻转：钉到视口右边缘后 align 应从 center 修正为 end
pin = tab.js(
    """(()=>{const el=document.querySelector('.jm-tooltip');
el.style.position='fixed'; el.style.right='4px'; el.style.bottom='10px'; el.dataset.pinned='1';
const r=el.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2};})()"""
)
time.sleep(0.2)
hover(pin["x"], pin["y"])
flip = tab.js("document.querySelector('.jm-tooltip[data-pinned]').className")
check("tooltip", "auto-flip adjusts align at right edge", "is-align-end" in flip, True)
check("tooltip", "flip keeps top placement (space above)", "is-top" in flip, True)
tab.js("document.querySelector('.jm-tooltip[data-pinned]').style.cssText=''")
time.sleep(0.3)

# 长按触发 + 抬手自动消失
wait_demo("长按这行字")
lp = center_of("[...document.querySelectorAll('.jm-tooltip')].find(e=>e.textContent.includes('长按这行字'))")
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": lp["x"], "y": lp["y"], "id": 0}]})
time.sleep(0.15)
check("tooltip", "longpress waits before opening", panels(), [])
time.sleep(0.6)
check("tooltip", "longpress opens panel", panels(), ["设备编号 JM-A12-0031"])
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.3)
check("tooltip", "panel stays right after touch end", panels(), ["设备编号 JM-A12-0031"])
time.sleep(2.0)
check("tooltip", "auto-hides 1.6s after release", panels(), [])

# 滚动打断长按
lp2 = center_of("[...document.querySelectorAll('.jm-tooltip')].find(e=>e.textContent.includes('长按这行字'))")
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": lp2["x"], "y": lp2["y"], "id": 0}]})
time.sleep(0.1)
tab.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": lp2["x"] - 50, "y": lp2["y"] - 80, "id": 0}]})
time.sleep(0.7)
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.2)
check("tooltip", "scroll gesture cancels longpress", panels(), [])

# click 触发切换
wait_demo("点我查看说明")
ck = center_of("[...document.querySelectorAll('.jm-tooltip')].find(e=>e.textContent.includes('点我查看说明'))")
tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": ck["x"], "y": ck["y"], "button": "left", "clickCount": 1})
tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": ck["x"], "y": ck["y"], "button": "left", "clickCount": 1})
time.sleep(0.4)
check("tooltip", "click opens", len(panels()), 1)
tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": ck["x"], "y": ck["y"], "button": "left", "clickCount": 1})
tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": ck["x"], "y": ck["y"], "button": "left", "clickCount": 1})
time.sleep(0.4)
check("tooltip", "click toggles closed", panels(), [])

# light 主题（theme class 渲染在打开后的面板上，直接验证组件 props 与面板 class）
light = tab.js(
    "(()=>{const t=[...document.querySelectorAll('.jm-tooltip')]"
    ".find(e=>e.textContent.includes('再试一个'));"
    "return t ? t.__vueParentComponent.props.theme : null;})()"
)
check("tooltip", "light theme prop", light, "light")

# 键盘聚焦触发（hover 模式下 focusin 立即显示）
kb = center_of("document.querySelector('.demo-page .jm-tooltip')")
tab.js("document.querySelector('.demo-page .jm-tooltip button').focus()")
time.sleep(0.3)
check("tooltip", "keyboard focus opens panel", panels(), ["刷新数据"])
tab.js("document.activeElement.blur()")
time.sleep(0.3)
check("tooltip", "blur closes panel", panels(), [])

# ============================ 汇总 ============================
print(f"\n=== interactions15: {ok} passed, {fail} failed ===")
sys.exit(1 if fail else 0)
