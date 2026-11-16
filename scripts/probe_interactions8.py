"""Calendar 增强批（方形样式 / 对齐修复 / 月份面板 / 禁用与只读）交互回归。"""
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


def page(has_text):
    return f"[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('{has_text}'))"


tab.goto(f"{BASE}/components/calendar", wait=4)

# ---------- 方形样式 ----------
sq = f"{page('方形选中')}.querySelectorAll('.jm-calendar')[0]"
check(
    "calendar",
    "square root class",
    tab.js(f"{page('方形选中')}.querySelectorAll('.jm-calendar.is-square').length"),
    2,
)
check(
    "calendar",
    "square selected bg = primary",
    tab.js(f"getComputedStyle({sq}.querySelector('.jm-calendar__day.is-selected .jm-calendar__day-main')).backgroundColor"),
    "rgb(0, 160, 233)",
)
check(
    "calendar",
    "square selected radius 4px",
    tab.js(f"getComputedStyle({sq}.querySelector('.jm-calendar__day.is-selected .jm-calendar__day-main')).borderRadius"),
    "4px",
)

rng = f"{page('方形选中')}.querySelectorAll('.jm-calendar')[1]"
check(
    "calendar",
    "square range start radius",
    tab.js(f"getComputedStyle({rng}.querySelector('.jm-calendar__day.is-range-start .jm-calendar__day-main')).borderRadius"),
    "4px 0px 0px 4px",
)
check(
    "calendar",
    "square range end radius",
    tab.js(f"getComputedStyle({rng}.querySelector('.jm-calendar__day.is-range-end .jm-calendar__day-main')).borderRadius"),
    "0px 4px 4px 0px",
)

# ---------- 备注不挤偏数字：同行内有/无备注的数字中心一致 ----------
check(
    "calendar",
    "bottomInfo keeps numbers aligned",
    tab.js(
        f"""
(() => {{
  const cal = {page('方形选中')}.querySelectorAll('.jm-calendar')[0]
  const rows = {{}}
  ;[...cal.querySelectorAll('.jm-calendar__day.is-current')].forEach(d => {{
    const key = Math.round(d.getBoundingClientRect().top)
    ;(rows[key] = rows[key] || []).push(d)
  }})
  let maxDiff = 0
  Object.values(rows).forEach(cells => {{
    const cy = el => {{ const r = el.querySelector('.jm-calendar__day-text').getBoundingClientRect(); return r.top + r.height / 2 }}
    const named = cells.filter(c => c.querySelector('.jm-calendar__day-info'))
    const plain = cells.filter(c => !c.querySelector('.jm-calendar__day-info'))
    if (named.length && plain.length) maxDiff = Math.max(maxDiff, Math.abs(cy(named[0]) - cy(plain[0])))
  }})
  return Math.round(maxDiff * 100) / 100
}})()
""",
    ),
    0,
)
check(
    "calendar",
    "range band centered on number",
    tab.js(
        f"""
(() => {{
  const cal = {rng}
  const mid = cal.querySelector('.jm-calendar__day.is-in-range')
  const mr = mid.querySelector('.jm-calendar__day-main').getBoundingClientRect()
  const tr = mid.querySelector('.jm-calendar__day-text').getBoundingClientRect()
  return Math.round(Math.abs((mr.top + mr.bottom) / 2 - (tr.top + tr.height / 2)) * 100) / 100
}})()
""",
    ),
    0,
)

# ---------- allow-same-day：点已选起点 → 起止同天 ----------
# 完整区间下点击 = 重新开始选起点；再点同一天 = 起止同天（allowSameDay 默认开）
tab.js(f"{page('日期区间')}.querySelectorAll('.jm-calendar')[1].querySelector('.jm-calendar__day.is-range-start').click()")
time.sleep(0.2)
tab.js(f"{page('日期区间')}.querySelectorAll('.jm-calendar')[1].querySelector('.jm-calendar__day.is-range-start').click()")
time.sleep(0.3)
check(
    "calendar",
    "allowSameDay picks start=end",
    tab.js(f"{page('日期区间')}.querySelectorAll('.jm-calendar__summary')[1]?.textContent"),
    "11月10日 - 11月10日",
)

# ---------- 月份面板（month） ----------
sw = page("点标题选月份")
tab.js(f"{sw}.querySelectorAll('.jm-calendar__month.is-switchable')[0].click()")
time.sleep(0.5)
check(
    "calendar",
    "month panel opens",
    tab.js("!!document.querySelector('.jm-calendar__panel')"),
    True,
)
check(
    "calendar",
    "month panel 1 column",
    tab.js("document.querySelector('.jm-calendar__panel').querySelectorAll('.jm-picker-column').length"),
    1,
)
tab.js("(()=>{const col=document.querySelector('.jm-calendar__panel .jm-picker-column');[...col.querySelectorAll('.jm-picker-column__item')].find(e=>e.textContent.trim()==='3月').click()})()")
time.sleep(0.4)
tab.js("document.querySelector('.jm-calendar__panel-action.is-confirm').click()")
time.sleep(0.4)
check(
    "calendar",
    "month panel switches month",
    tab.js(f"{sw}.querySelectorAll('.jm-calendar__month-text')[0].textContent"),
    "2026年3月",
)
check(
    "calendar",
    "month-change event fired",
    tab.js(f"{sw}.querySelector('.demo-note').textContent"),
    "当前展示：2026年3月",
)

# ---------- 年月面板 + 遮罩关闭 ----------
tab.js(f"{sw}.querySelectorAll('.jm-calendar__month.is-switchable')[1].click()")
time.sleep(0.5)
check(
    "calendar",
    "year-month panel 2 columns",
    tab.js("document.querySelector('.jm-calendar__panel').querySelectorAll('.jm-picker-column').length"),
    2,
)
tab.js("document.querySelector('.jm-calendar__panel-mask').click()")
time.sleep(0.4)
check(
    "calendar",
    "mask click closes panel",
    tab.js("document.querySelectorAll('.jm-calendar__panel').length"),
    0,
)

# ---------- 自定义禁用 ----------
dis = page("只能选周末")
check(
    "calendar",
    "disableDate marks weekdays",
    tab.js(f"{dis}.querySelectorAll('.jm-calendar')[0].querySelectorAll('.jm-calendar__day.is-disabled').length"),
    lambda v: v > 20,
)
check(
    "calendar",
    "enabled days are weekends",
    tab.js(
        f"""JSON.stringify([...{dis}.querySelectorAll('.jm-calendar')[0].querySelectorAll('.jm-calendar__day.is-current')]
 .filter(d=>!d.disabled).map(d=>d.querySelector('.jm-calendar__day-text').textContent.trim()))"""
    ),
    lambda v: all(int(x) % 7 in (0, 1) or int(x) in (1, 7, 8, 14, 15, 21, 22, 28, 29) for x in json.loads(v)),
)

# ---------- 只读 ----------
ro = f"{page('只读（可翻月')}.querySelectorAll('.jm-calendar')[0]"
before = tab.js(f"{ro}.querySelector('.jm-calendar__day.is-selected .jm-calendar__day-text').textContent.trim()")
tab.js(f"{ro}.querySelectorAll('.jm-calendar__day.is-current')[10].click()")
time.sleep(0.3)
after = tab.js(f"{ro}.querySelector('.jm-calendar__day.is-selected .jm-calendar__day-text').textContent.trim()")
check("calendar", "readonly keeps selection", (before, after), (before, before))

# 翻月仍然可用
m0 = tab.js(f"{ro}.querySelector('.jm-calendar__month').textContent")
tab.js(f"{ro}.querySelectorAll('.jm-calendar__arrow')[1].click()")
time.sleep(0.4)
m1 = tab.js(f"{ro}.querySelector('.jm-calendar__month').textContent")
check("calendar", "readonly can still switch month", m0 != m1, True)

print(f"\n共 {ok + fail} 项，通过 {ok}，失败 {fail}")
sys.exit(1 if fail else 0)
