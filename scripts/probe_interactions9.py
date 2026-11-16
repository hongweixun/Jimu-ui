"""Timeline / Statistic / Signature 新组件批交互回归。"""
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
        print(f"  FAIL {page}/{name}: got {json.dumps(actual, ensure_ascii=False)[:220]}, want {expect}")


def page(has_text):
    return (
        f"[...document.querySelectorAll('.demo-page')]"
        f".find(p=>p.textContent.includes('{has_text}'))"
    )


def scroll_top(expr):
    return tab.js(f"(()=>{{const el={expr};const box=el.closest('.demo__phone')||el.parentElement;"
                  f"return box ? box.scrollTop : -1}})()")


def touch_drag(x, y, dx, dy, steps=8, hold=0.02):
    tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
    for i in range(1, steps + 1):
        tab.send(
            "Input.dispatchTouchEvent",
            {
                "type": "touchMove",
                "touchPoints": [{"x": x + dx * i / steps, "y": y + dy * i / steps}],
            },
        )
        time.sleep(hold)
    tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.35)


def center(sel):
    return tab.js(
        f"(()=>{{const el={sel};if(!el)return null;el.scrollIntoView({{block:'center'}});"
        f"const r=el.getBoundingClientRect();return {{x:r.left+r.width/2,y:r.top+r.height/2,"
        f"w:r.width,h:r.height,top:r.top,left:r.left}}}})()"
    )


# ---------------- Timeline ----------------
tab.goto(f"{BASE}/components/timeline", wait=3.5)
tl = f"{page('提交作业')}.querySelectorAll('.jm-timeline')[0]"

check("timeline", "two timelines on page", tab.js(f"{page('提交作业')}.querySelectorAll('.jm-timeline').length"), 2)
check("timeline", "first timeline item count", tab.js(f"{tl}.querySelectorAll('.jm-timeline-item').length"), 4)
check(
    "timeline",
    "has-time item uses 3 columns",
    tab.js(f"getComputedStyle({tl}.querySelector('.jm-timeline-item')).gridTemplateColumns.split(' ').length"),
    3,
)
check(
    "timeline",
    "time column right aligned",
    tab.js(f"getComputedStyle({tl}.querySelector('.jm-timeline-item__time')).textAlign"),
    "right",
)
check(
    "timeline",
    "time column width ~60px",
    tab.js(f"parseFloat(getComputedStyle({tl}.querySelector('.jm-timeline-item__time')).width)"),
    lambda v: 50 <= v <= 65,
)
# 圆点与标题首行对齐（差值应在一行字高以内）
check(
    "timeline",
    "dot aligned with title",
    tab.js(
        f"(()=>{{const it={tl}.querySelector('.jm-timeline-item');"
        f"const d=it.querySelector('.jm-timeline-item__dot').getBoundingClientRect();"
        f"const t=it.querySelector('.jm-timeline-item__title').getBoundingClientRect();"
        f"return Math.round(d.top + d.height/2 - (t.top + t.height/2))}})()"
    ),
    lambda v: -14 <= v <= 14,
)
# 连线穿过节点间距，与下一个圆点相接（不留断口）
check(
    "timeline",
    "line reaches next dot",
    tab.js(
        f"(()=>{{const its={tl}.querySelectorAll('.jm-timeline-item');"
        f"const line=its[0].querySelector('.jm-timeline-item__line').getBoundingClientRect();"
        f"const next=its[1].querySelector('.jm-timeline-item__dot').getBoundingClientRect();"
        f"return Math.round(next.top - line.bottom)}})()"
    ),
    lambda v: v <= 2,
)
check(
    "timeline",
    "last item has no line",
    tab.js(f"getComputedStyle({tl}.lastElementChild.querySelector('.jm-timeline-item__line')).display"),
    "none",
)
check(
    "timeline",
    "success dot differs from default dot",
    tab.js(
        f"getComputedStyle({tl}.querySelector('.jm-timeline-item--success .jm-timeline-item__dot')).backgroundColor"
        f" !== getComputedStyle({tl}.querySelectorAll('.jm-timeline-item')[3].querySelector('.jm-timeline-item__dot')).backgroundColor"
    ),
    True,
)
check(
    "timeline",
    "active title uses primary",
    tab.js(
        f"getComputedStyle({tl}.querySelector('.jm-timeline-item.is-active .jm-timeline-item__title')).color"
    ),
    "rgb(0, 160, 233)",
)
check(
    "timeline",
    "icon dot is 20px",
    tab.js(
        f"getComputedStyle({tl}.querySelector('.jm-timeline-item.has-icon .jm-timeline-item__dot')).width"
    ),
    "20px",
)

tl2 = f"{page('虚线')}.querySelectorAll('.jm-timeline')[1]"
check("timeline", "dashed item count", tab.js(f"{tl2}.querySelectorAll('.jm-timeline-item').length"), 3)
check(
    "timeline",
    "dashed line uses gradient",
    tab.js(f"getComputedStyle({tl2}.querySelector('.jm-timeline-item__line')).backgroundImage"),
    lambda v: "gradient" in str(v),
)
check(
    "timeline",
    "hollow dot has 2px border",
    tab.js(
        f"getComputedStyle({tl2}.querySelector('.jm-timeline-item.is-hollow .jm-timeline-item__dot')).borderTopWidth"
    ),
    "2px",
)

# ---------------- Statistic ----------------
tab.goto(f"{BASE}/components/statistic", wait=1.2)
time.sleep(1.3)  # 等滚动动画落位
st = page("当前在线")
check("statistic", "five statistics", tab.js(f"{st}.querySelectorAll('.jm-statistic').length"), 5)
nums = tab.js(f"[...{st}.querySelectorAll('.jm-statistic__number')].map(n=>n.textContent)")
check("statistic", "numbers formatted", nums, ["1,286", "92.5", "86.4", "1,234,567.89", "—"])
check("statistic", "prefix and suffix", tab.js(
    f"(()=>{{const el=[...{st}.querySelectorAll('.jm-statistic')][3];"
    f"return [el.querySelector('.jm-statistic__prefix').textContent, el.querySelector('.jm-statistic__suffix').textContent]}})()"
), ["¥", "元"])
check("statistic", "lg size larger than md", tab.js(
    f"parseFloat(getComputedStyle([...{st}.querySelectorAll('.jm-statistic__value')][1]).fontSize)"
    f" > parseFloat(getComputedStyle([...{st}.querySelectorAll('.jm-statistic__value')][0]).fontSize)"
), True)
check("statistic", "custom color applied", tab.js(
    f"getComputedStyle([...{st}.querySelectorAll('.jm-statistic')][1].querySelector('.jm-statistic__value')).color"
), "rgb(0, 160, 233)")

# 点按钮：数值在动画中变化，最终无 NaN
# 无头 Edge 默认 prefers-reduced-motion: reduce，先显式声明「不减弱动画」才能测到滚动
tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
# 页内一次采样到底：两次往返之间动画可能已经结束，容易假失败
samples = tab.js(
    "(async()=>{"
    f"const st={st};"
    "const n=()=>st.querySelector('.jm-statistic__number').textContent;"
    "const out=[n()];"
    "[...st.querySelectorAll('button')].find(b=>b.textContent.includes('换一组')).click();"
    "await new Promise(r=>setTimeout(r,150)); out.push(n());"
    "await new Promise(r=>setTimeout(r,1100)); out.push(n());"
    "return out;})()"
)
before, mid, after = samples
check("statistic", "value changed on refresh", after != before, True)
check("statistic", "mid animation differs from final", mid != after, True)
check("statistic", "no NaN after refresh", "NaN" in str(after), False)
check("statistic", "still thousands separated", tab.js(f"{st}.querySelector('.jm-statistic__number').textContent"), lambda v: bool(__import__('re').fullmatch(r'\d{1,3}(,\d{3})*', str(v))))

# 减弱动画偏好下应直接落位（无障碍要求）
tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
tab.js(f"[...{st}.querySelectorAll('button')].find(b=>b.textContent.includes('换一组')).click()")
time.sleep(0.06)
reduced_early = tab.js(f"{st}.querySelector('.jm-statistic__number').textContent")
time.sleep(0.5)
reduced_late = tab.js(f"{st}.querySelector('.jm-statistic__number').textContent")
check("statistic", "reduced motion jumps instantly", reduced_early, reduced_late)
tab.js(f"window.scrollTo(0,0)")

# ---------------- Signature ----------------
tab.goto(f"{BASE}/components/signature", wait=3.5)
sig = f"{page('确认签名')}.querySelector('.jm-signature')"
cv = f"{page('确认签名')}.querySelector('.jm-signature__canvas')"

check("signature", "canvas bitmap scaled by dpr", tab.js(
    f"(()=>{{const c={cv};return Math.round(c.width / c.getBoundingClientRect().width * 100)/100}})()"
), lambda v: 1 <= v <= 3)
check("signature", "placeholder visible when empty", tab.js(
    f"!!{sig}.querySelector('.jm-signature__placeholder')"
), True)
check("signature", "toolbar buttons disabled when empty", tab.js(
    f"[...{sig}.querySelectorAll('.jm-signature__btn')].every(b=>b.disabled)"
), True)
check("signature", "canvas prevents page scroll", tab.js(
    f"getComputedStyle({cv}).touchAction"
), "none")

box = center(f"{cv}")
st_before = scroll_top(f"{page('确认签名')}")
touch_drag(box["x"] - 60, box["y"], 120, 0, steps=10)
st_after = scroll_top(f"{page('确认签名')}")

check("signature", "value emitted after stroke", tab.js(
    f"!!{page('确认签名')}.querySelector('img[alt=\"签名预览\"]')"
), True)
check("signature", "drawing does not scroll page", st_after, st_before)
check("signature", "toolbar enabled after stroke", tab.js(
    f"[...{sig}.querySelectorAll('.jm-signature__btn')].every(b=>!b.disabled)"
), True)
check("signature", "trim crops width smaller than canvas", tab.js(
    f"(()=>{{const img={page('确认签名')}.querySelector('img[alt=\"签名预览\"]');"
    f"const c={cv}.getBoundingClientRect();return img.naturalWidth < c.width*0.98}})()"
), True)

# 撤销回到空
tab.js(f"[...{sig}.querySelectorAll('.jm-signature__btn')][0].click()")
time.sleep(0.25)
check("signature", "undo empties canvas", tab.js(f"!!{sig}.querySelector('.jm-signature__placeholder')"), True)
check("signature", "undo removed preview", tab.js(
    f"!!{page('确认签名')}.querySelector('img[alt=\"签名预览\"]')"
), False)

# 再画一条，验证只读回显不响应触摸
touch_drag(box["x"] - 40, box["y"] + 10, 90, 0, steps=8)
time.sleep(0.3)
src1 = tab.js(f"{page('确认签名')}.querySelector('img[alt=\"签名预览\"]')?.src || ''")
check("signature", "readonly preview rendered", tab.js(
    f"{page('确认签名')}.querySelectorAll('.jm-signature')[1]?.classList.contains('is-readonly')"
), True)
ro_box = center(f"{page('确认签名')}.querySelectorAll('.jm-signature__canvas')[1]")
touch_drag(ro_box["x"], ro_box["y"], 60, 0, steps=6)
time.sleep(0.3)
src2 = tab.js(f"{page('确认签名')}.querySelector('img[alt=\"签名预览\"]')?.src || ''")
check("signature", "readonly ignores touch input", src1 == src2 and bool(src1), True)

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(1 if fail else 0)
