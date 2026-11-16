"""第六批组件（DatePicker/IndexBar/CountDown/Circle/NumberKeyboard/PasswordInput/Result/Watermark）交互回归。"""
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


def dispatch(tab, sel, event, x=None, y=None):
    box = tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(!e) return null; const r=e.getBoundingClientRect();"
        f"return {{x:r.left+r.width/2, y:r.top+r.height/2}}}})()"
    )
    if not box:
        return
    opts = {"bubbles": True, "pointerId": 1, "isPrimary": True,
            "clientX": x if x is not None else box["x"],
            "clientY": y if y is not None else box["y"]}
    tab.js(f"document.querySelector({json.dumps(sel)}).dispatchEvent("
           f"new PointerEvent({json.dumps(event)}, {json.dumps(opts)}))")


def drag(tab, sel, dx, dy=0, steps=8):
    box = tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(!e) return null; const r=e.getBoundingClientRect();"
        f"return {{x:r.left+r.width/2, y:r.top+r.height/2}}}})()"
    )
    if not box:
        return
    dispatch(tab, sel, "pointerdown")
    for i in range(1, steps + 1):
        dispatch(tab, sel, "pointermove", box["x"] + dx * i / steps, box["y"] + dy * i / steps)
        time.sleep(0.015)
    # pointerup 必须带最终坐标：松手时的 dy 参与吸附计算
    dispatch(tab, sel, "pointerup", box["x"] + dx, box["y"] + dy)


def click(tab, sel):
    tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(e) e.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))}})()"
    )


def text_of(tab, sel):
    return tab.js(f"document.querySelector({json.dumps(sel)})?.textContent?.trim()")


def click_by_text(tab, sel, keyword):
    tab.js(
        f"[...document.querySelectorAll({json.dumps(sel)})]"
        f".find(e=>e.textContent.trim() === {json.dumps(keyword)} || e.textContent.includes({json.dumps(keyword)}))"
        f"?.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))"
    )


ensure_edge()
tab = new_tab()

# ---------- DatePicker ----------
tab.goto(f"{BASE}/components/date-picker", wait=3)
check("date-picker", "弹层未开时 cell 显示默认值", "上课日期" in str(text_of(tab, ".demo-page")), True)
click(tab, ".demo-page .jm-cell")
time.sleep(0.8)
check("date-picker", "弹层打开出现滚轮", tab.js("!!document.querySelector('.jm-popup .jm-date-picker')"), True)
# datetime 内嵌块：第二列月拖动后确认日期联动
click(tab, ".jm-popup .jm-picker__action.is-confirm")
time.sleep(0.5)
check("date-picker", "confirm 后 cell 值保持", text_of(tab, ".demo-page .jm-cell .jm-cell__value"), "2026-11-18")

def cur_note():
    return tab.js("[...document.querySelectorAll('.demo-note')].map(e=>e.textContent.trim()).find(t=>t.startsWith('当前：'))")

note0 = cur_note()
# 内嵌 datetime：拖第三列（日）向上一天
day_col = tab.js("[...document.querySelectorAll('.jm-date-picker')].map(d=>d.querySelectorAll('.jm-picker-column').length)")
check("date-picker", "datetime 共 5 列", day_col[0] if day_col else None, 5)
drag(tab, ".jm-date-picker .jm-picker-column:nth-child(3)", 0, -110, steps=6)
time.sleep(0.8)
note1 = cur_note()
check("date-picker", "拖日列后文案变化", note1 != note0, True)

# ---------- IndexBar ----------
tab.goto(f"{BASE}/components/index-bar", wait=3)
items = tab.js("[...document.querySelectorAll('.jm-index-bar__item')].map(e=>e.textContent)")
check("index-bar", "索引条自动生成", items, ["A", "B", "C", "D", "F", "G", "H", "J", "L", "M", "S", "W", "Z"])
before = tab.js("document.querySelector('#idx-scroll').scrollTop")
b = tab.js("(()=>{const e=[...document.querySelectorAll('.jm-index-bar__item')][3];const r=e.getBoundingClientRect();return {x:r.left+r.width/2, y:r.top+r.height/2}})()")
o = {"bubbles": True, "pointerId": 1, "isPrimary": True, "clientX": b["x"], "clientY": b["y"]}
tab.js("[...document.querySelectorAll('.jm-index-bar__item')][3].dispatchEvent(new PointerEvent('pointerdown', "
       + json.dumps(o).replace(chr(39), chr(34)) + "))")
time.sleep(0.9)
after = tab.js("document.querySelector('#idx-scroll').scrollTop")
check("index-bar", "点 D 后滚动定位", after > before, True)
active = tab.js("document.querySelector('.jm-index-bar__item.is-active')?.textContent")
check("index-bar", "D 高亮", active, "D")

# ---------- CountDown ----------
tab.goto(f"{BASE}/components/count-down", wait=3)
big = tab.js("[...document.querySelectorAll('.jm-count-down')].map(e=>e.textContent.trim())")
check("count-down", "基础 format 拆分", ":" in str(big[0]), True)

def ctl_text():
    return tab.js("[...document.querySelectorAll('.jm-count-down')][3]?.textContent.trim()")

t0 = ctl_text()
click(tab, ".demo-page .actions .jm-button")  # 开始
time.sleep(1.3)
t1 = ctl_text()
click(tab, ".demo-page .actions .jm-button:nth-child(2)")  # 暂停
time.sleep(0.6)
t2 = ctl_text()
time.sleep(0.6)
t3 = ctl_text()
check("count-down", "开始后递减", t1 != t0, True)
check("count-down", "暂停后冻结", t2 == t3, True)
click(tab, ".demo-page .actions .jm-button:nth-child(3)")  # 重置
time.sleep(0.4)
check("count-down", "重置回满值", ctl_text(), t0)

# ---------- Circle ----------
tab.goto(f"{BASE}/components/circle", wait=3)
p0 = text_of(tab, ".jm-circle")
click(tab, ".demo-page .actions .jm-button")
time.sleep(0.6)
p1 = text_of(tab, ".jm-circle")
check("circle", "随机后百分比变化", p0 != p1 and "%" in str(p1), True)
check("circle", "渐变使用 linearGradient",
      tab.js("!!document.querySelector('.jm-circle linearGradient')"), True)
check("circle", "自定义中心渲染", "答对题数" in str(tab.js("document.body.innerText")), True)

# ---------- NumberKeyboard ----------
tab.goto(f"{BASE}/components/number-keyboard", wait=3)
click_by_text(tab, ".demo-page .jm-button", "打开键盘")
time.sleep(0.7)
check("keyboard", "键盘打开", tab.js("!!document.querySelector('.jm-number-keyboard')"), True)
click(tab, ".jm-number-keyboard__grid .jm-number-keyboard__key")
time.sleep(0.3)
check("keyboard", "按键写入 cell", text_of(tab, ".demo-page .jm-cell .jm-cell__value"), "1")
dispatch(tab, ".jm-number-keyboard__key.is-delete", "pointerdown")
dispatch(tab, ".jm-number-keyboard__key.is-delete", "pointerup")
time.sleep(0.3)
check("keyboard", "退格清空", text_of(tab, ".demo-page .jm-cell .jm-cell__value"), "点击输入")
click(tab, ".jm-number-keyboard__close")
time.sleep(0.6)
check("keyboard", "关闭按钮收起", tab.js("!!document.querySelector('.jm-number-keyboard')"), False)

# 自定义键盘
click_by_text(tab, ".demo-page .jm-cell", "快捷金额")
time.sleep(0.7)
click(tab, ".jm-number-keyboard__custom .jm-number-keyboard__key:nth-child(2)")
time.sleep(0.5)
check("keyboard", "自定义按键回填", "¥ 200" in str(text_of(tab, ".demo-page")), True)

# ---------- PasswordInput ----------
tab.goto(f"{BASE}/components/password-input", wait=3)
tab.js("document.querySelector('.jm-password-input').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
time.sleep(0.7)
check("password", "点击唤起键盘", tab.js("!!document.querySelector('.jm-number-keyboard')"), True)
keys = ".jm-number-keyboard__grid .jm-number-keyboard__key"
for k in ["1", "2", "3"]:
    click(tab, keys)
    time.sleep(0.15)
dots = tab.js("document.querySelectorAll('.jm-password-input')[0].querySelectorAll('.jm-password-input__dot:not(.is-plain)').length")
check("password", "输 3 位出现 3 个圆点", dots, 3)
click(tab, ".jm-number-keyboard__key.is-delete")
time.sleep(0.2)
click(tab, keys)  # 重新补第 3 位
click(tab, keys)
click(tab, keys)
time.sleep(0.3)
note = tab.js("[...document.querySelectorAll('.demo-note')].map(e=>e.textContent).find(t=>t.includes('位'))")
check("password", "输满触发 complete", "已输入 6 位" in str(note), True)

# ---------- Result ----------
tab.goto(f"{BASE}/components/result", wait=3)
click(tab, ".demo-page .jm-tag:nth-child(2)")
time.sleep(0.4)
check("result", "切换状态改标题", text_of(tab, ".jm-result__title"), "支付失败")
check("result", "error 配色", tab.js("getComputedStyle(document.querySelector('.jm-result')).getPropertyValue('--jm-result-color')").strip() != "", True)

# ---------- Watermark ----------
tab.goto(f"{BASE}/components/watermark", wait=3)
bg = tab.js("document.querySelector('.jm-watermark__layer')?.style.backgroundImage || ''")
check("watermark", "canvas 平铺图生成", str(bg).startswith('url("data:image/png'), True)
check("watermark", "pointer-events none",
      tab.js("getComputedStyle(document.querySelector('.jm-watermark__layer')).pointerEvents"), "none")

print("\n== 汇总 ==")
fails = [r for r in results if not r[2]]
print(f"{len(results) - len(fails)}/{len(results)} 通过")
for name, desc, ok, actual, expect in fails:
    print("FAIL:", name, "-", desc)
