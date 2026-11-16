"""无障碍与键盘回归：Dialog 焦点陷阱 / Esc / 焦点归还、ActionSheet、图片预览方向键、Tabs 与 Segmented 方向键、焦点环令牌。"""
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
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False)[:120]}")
    else:
        fail += 1
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False)[:220]}, want {expect}")


KEYS = {
    'Tab': (9, 'Tab'),
    'Escape': (27, 'Escape'),
    'ArrowLeft': (37, 'ArrowLeft'),
    'ArrowRight': (39, 'ArrowRight'),
    'Home': (36, 'Home'),
    'End': (35, 'End'),
}


def key(name, shift=False):
    code, key_name = KEYS[name]
    mods = 8 if shift else 0
    tab.send(
        "Input.dispatchKeyEvent",
        {
            "type": "keyDown",
            "key": key_name,
            "code": key_name,
            "windowsVirtualKeyCode": code,
            "nativeVirtualKeyCode": code,
            "modifiers": mods,
        },
    )
    tab.send(
        "Input.dispatchKeyEvent",
        {
            "type": "keyUp",
            "key": key_name,
            "code": key_name,
            "windowsVirtualKeyCode": code,
            "nativeVirtualKeyCode": code,
            "modifiers": mods,
        },
    )
    time.sleep(0.12)


def active():
    return tab.js(
        "(()=>{const el=document.activeElement;if(!el)return null;return {"
        "tag:el.tagName,cls:el.className&&String(el.className),txt:(el.textContent||'').trim().slice(0,20),"
        "inDialog:!!el.closest('.jm-dialog'),inSheet:!!el.closest('.jm-action-sheet')}})()"
    )


def press_button(text):
    # 先聚焦再点击：真实用户用键盘 / 鼠标点按钮时焦点都在按钮上，
    # 这样关闭弹层后「焦点归还」才有落点可验
    tab.js(
        "(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().includes("
        + json.dumps(text, ensure_ascii=False)
        + "));if(b){b.focus();b.click()}})()"
    )


# ============================ Dialog ============================
tab.goto(f"{BASE}/components/dialog", wait=4)
time.sleep(1.2)
tab.js("window.scrollTo(0,0)")
press_button('打开表单弹窗')
time.sleep(0.8)

a0 = active()
check("dialog", "focus moved into dialog on open", bool(a0 and a0.get("inDialog")), True)
check("dialog", "initial focus on first field", (a0 or {}).get("cls"), lambda v: v == "jm-input__inner")

labelled = tab.js(
    "(()=>{const d=document.querySelector('.jm-dialog');if(!d)return null;"
    "const id=d.getAttribute('aria-labelledby');"
    "return {id:!!id,text:id?document.getElementById(id)?.textContent.trim():null}})()"
)
check("dialog", "aria-labelledby points to title", labelled, {"id": True, "text": "填写收件人"})

# Tab 连续 8 次，焦点必须一直在弹窗内
inside_all = []
button_rings = set()
input_rings = set()
for _ in range(8):
    key("Tab")
    st = active()
    inside_all.append(bool(st and st.get("inDialog")))
    ring = tab.js(
        "(()=>{const el=document.activeElement;const s=getComputedStyle(el);return {tag:el.tagName,"
        "w:s.outlineWidth,style:s.outlineStyle}})()"
    )
    if isinstance(ring, dict):
        # 只看「有没有画出线」，outline-style:none 时 width 仍是 medium(3px)，不能拿宽度判断
        value = ring["w"] if ring["style"] == "solid" else "none"
        (button_rings if ring["tag"] == "BUTTON" else input_rings).add(value)
check("dialog", "focus never escapes by Tab (8x)", all(inside_all), True)
check("dialog", "buttons show 2px focus ring", sorted(button_rings), ["2px"])
check("dialog", "inputs use border focus, no outline", sorted(input_rings), ["none"])

# Shift+Tab 反向循环同样不跑出去
back_inside = []
for _ in range(3):
    key("Tab", shift=True)
    st = active()
    back_inside.append(bool(st and st.get("inDialog")))
check("dialog", "Shift+Tab stays inside", all(back_inside), True)

key("Escape")
time.sleep(0.9)
check("dialog", "Esc closes dialog", tab.js("!document.querySelector('.jm-dialog')"), True)
check("dialog", "focus returns to trigger", (active() or {}).get("txt", ""), "打开表单弹窗")

# ============================ ActionSheet ============================
tab.goto(f"{BASE}/components/action-sheet", wait=4)
time.sleep(1.0)
press_button('打开动作面板')
time.sleep(0.8)
a1 = active()
check("sheet", "trap active on open", bool(a1 and a1.get("inSheet")), True)
inside_sheet = []
for _ in range(6):
    key("Tab")
    st = active()
    inside_sheet.append(bool(st and st.get("inSheet")))
check("sheet", "focus stays inside sheet (6x Tab)", all(inside_sheet), True)
key("Escape")
time.sleep(0.9)
check("sheet", "Esc closes sheet", tab.js("!document.querySelector('.jm-action-sheet')"), True)
check("sheet", "focus returns to trigger", (active() or {}).get("txt", ""), "打开动作面板")

# ============================ ImagePreview ============================
tab.goto(f"{BASE}/components/photo-wall", wait=4)
time.sleep(1.6)
tab.js("(()=>{const it=document.querySelector('.jm-photo-wall__item');it.focus();it.click()})()")
time.sleep(0.8)
idx = lambda: tab.js("document.querySelector('.jm-image-preview__index')?.textContent.trim()")
check("preview", "opened at 1 / 12", idx(), "1 / 12")
check("preview", "focus inside preview", tab.js(
    "!!document.activeElement?.closest('.jm-image-preview')"
), True)

key("ArrowRight")
time.sleep(0.45)
check("preview", "ArrowRight → next", idx(), "2 / 12")
key("ArrowLeft")
time.sleep(0.45)
check("preview", "ArrowLeft → prev", idx(), "1 / 12")
key("End")
time.sleep(0.5)
check("preview", "End → last", idx(), "12 / 12")
key("End")
time.sleep(0.45)
check("preview", "End at last does not overflow", idx(), "12 / 12")
key("Home")
time.sleep(0.5)
check("preview", "Home → first", idx(), "1 / 12")

live = tab.js(
    "(()=>{const s=document.querySelector('.jm-image-preview .jm-visually-hidden');"
    "return s?{live:s.getAttribute('aria-live'),text:s.textContent.replace(/\\s+/g,' ').trim()}:null})()"
)
check("preview", "aria-live announces index", live, {"live": "polite", "text": "第 1 张，共 12 张"})

key("Escape")
time.sleep(0.8)
check("preview", "Esc closes preview", tab.js("!document.querySelector('.jm-image-preview')"), True)
check("preview", "focus returns to the photo", tab.js(
    "document.activeElement?.classList.contains('jm-photo-wall__item')"
), True)

# ============================ Tabs ============================
tab.goto(f"{BASE}/components/tabs", wait=4)
time.sleep(1.2)
first_tabs = "document.querySelectorAll('.jm-tabs')[0]"
check("tabs", "roving tabindex: one tabbable", tab.js(
    f"{first_tabs}.querySelectorAll('[role=\"tab\"][tabindex=\"0\"]').length"
), 1)
check("tabs", "others are -1", tab.js(
    f"{first_tabs}.querySelectorAll('[role=\"tab\"][tabindex=\"-1\"]').length"
), 3)

tab.js(f"{first_tabs}.querySelector('[role=\"tab\"]').focus()")
key("ArrowRight")
time.sleep(0.4)
check("tabs", "ArrowRight activates next", tab.js(
    f"{first_tabs}.querySelector('[role=\"tab\"][aria-selected=\"true\"] .jm-tabs__label')?.textContent"
), "直播")
check("tabs", "focus follows activation", tab.js(
    "document.activeElement?.textContent.trim()"
), lambda v: v and v.startswith("直播"))

# done → 下一个是 disabled 的「停用」，应环绕回「全部」
key("ArrowRight")
time.sleep(0.35)
key("ArrowRight")
time.sleep(0.4)
check("tabs", "skips disabled and wraps", tab.js(
    f"{first_tabs}.querySelector('[role=\"tab\"][aria-selected=\"true\"] .jm-tabs__label')?.textContent"
), "全部")

key("End")
time.sleep(0.4)
check("tabs", "End → last enabled tab", tab.js(
    f"{first_tabs}.querySelector('[role=\"tab\"][aria-selected=\"true\"] .jm-tabs__label')?.textContent"
), "已结束")
key("Home")
time.sleep(0.4)
check("tabs", "Home → first tab", tab.js(
    f"{first_tabs}.querySelector('[role=\"tab\"][aria-selected=\"true\"] .jm-tabs__label')?.textContent"
), "全部")

# ============================ Segmented ============================
tab.goto(f"{BASE}/components/segmented", wait=4)
time.sleep(1.2)
seg = "document.querySelector('.jm-segmented')"
check("seg", "roving tabindex: one tabbable", tab.js(
    f"{seg}.querySelectorAll('[role=\"tab\"][tabindex=\"0\"]').length"
), 1)
tab.js(f"{seg}.querySelector('[role=\"tab\"]').focus()")
key("ArrowRight")
time.sleep(0.4)
check("seg", "ArrowRight moves selection", tab.js(
    "document.querySelector('.jm-segmented [role=\"tab\"][aria-selected=\"true\"] .jm-segmented__label')?.textContent"
), lambda v: v is not None and v != "")

# ============================ 令牌与工具类 ============================
tab.goto(f"{BASE}/guide/motion-a11y", wait=4)
time.sleep(0.8)
check("a11y", "focus ring tokens defined", tab.js(
    "(()=>{const s=getComputedStyle(document.documentElement);"
    "return [s.getPropertyValue('--jm-focus-ring-width').trim(),s.getPropertyValue('--jm-focus-ring-color').trim()]})()"
), lambda v: v[0] == "2px" and v[1] != "")
check("a11y", "visually-hidden utility works", tab.js(
    "(()=>{const s=document.createElement('span');s.className='jm-visually-hidden';s.textContent='x';"
    "document.body.appendChild(s);const r=s.getBoundingClientRect();"
    "const st=getComputedStyle(s);const out={w:Math.round(r.width),h:Math.round(r.height),clip:st.clipPath};s.remove();return out})()"
), lambda v: v["w"] <= 1 and v["h"] <= 1 and "inset" in v["clip"])

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(0 if fail == 0 else 1)
