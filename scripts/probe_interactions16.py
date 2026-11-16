# -*- coding: utf-8 -*-
"""第十七批（0.19.0）新增组件探针：Tree / TreeSelect / LoadingBar / Transfer / Table"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab

BASE = "http://localhost:5173"
fails = []
total = 0


def check(section, name, actual, expect):
    global total
    total += 1
    ok = False
    if callable(expect):
        ok = bool(expect(actual))
    else:
        ok = actual == expect
    if ok:
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False, default=str)[:100]}")
    else:
        fails.append(f"{section}/{name}")
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False, default=str)[:200]}, want {expect}")


def press_button(text):
    tab.js(
        "(()=>{const b=[...document.querySelectorAll('button')]"
        ".find(x=>x.textContent.trim().includes('" + text + "'));"
        "if(b){b.focus();b.click()}})()"
    )


def wait_for(expr, timeout=6.0):
    end = time.time() + timeout
    while time.time() < end:
        v = tab.js(expr)
        if v:
            return v
        time.sleep(0.15)
    return None


VK = {"ArrowDown": 40, "ArrowUp": 38, "ArrowLeft": 37, "ArrowRight": 39, "End": 35, "Home": 36, "Enter": 13}


def key(key_name):
    vk = VK.get(key_name, 0)
    tab.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": key_name, "code": key_name, "windowsVirtualKeyCode": vk})
    tab.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": key_name, "code": key_name, "windowsVirtualKeyCode": vk})


def js(code, page=0):
    """把 __P__ 替换为第 page 个 demo 容器再执行"""
    return tab.js(code.replace("__P__", "document.querySelectorAll('.demo-page')[" + str(page) + "]"))


def set_input(selector_expr, value, page=0):
    return js(
        "(()=>{const input=" + selector_expr + ";"
        "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
        "setter.call(input,'" + value + "');"
        "input.dispatchEvent(new Event('input',{bubbles:true}));})()",
        page,
    )


ensure_edge()
tab = new_tab()
tab.send("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 1000, "deviceScaleFactor": 1, "mobile": False})


def goto(path):
    tab.goto(BASE + path, wait=6)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")

# ================= Tree =================
goto("/components/tree")
wait_for("document.querySelectorAll('.jm-tree').length >= 3")
time.sleep(1.5)
print("== tree ==")

info = js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const nodes=[...root.querySelectorAll('[role=treeitem]')];
  return {visible:nodes.length,
    selected:root.querySelector('.is-selected .jm-tree__label')?.textContent.trim(),
    ariaLevel:nodes[1]?.getAttribute('aria-level'),
    line:root.classList.contains('is-line'),
    disabledOk:[...root.querySelectorAll('[role=treeitem]')]
      .filter(n=>n.textContent.includes('第三章'))
      .every(n=>n.getAttribute('aria-disabled')==='true')};})()""")
check("tree", "visible nodes (c1:5 + c2:4 + c3:1)", info["visible"], 10)
check("tree", "selected label", info["selected"], "1.2 模板语法与指令")
check("tree", "aria-level on child", info["ariaLevel"], "2")
check("tree", "show-line class", info["line"], True)
check("tree", "disabled chapter aria-disabled", info["disabledOk"], True)

js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const row=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.textContent.includes('第一章'));
  row.querySelector('.jm-tree__arrow').click();})()""")
time.sleep(0.4)
check("tree", "collapse hides children", js("__P__.querySelectorAll('[role=treeitem]').length"), 6)

js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const row=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.textContent.includes('第一章'));
  row.click();})()""")
time.sleep(0.4)
check("tree", "row click expands + selects", js("__P__.querySelectorAll('[role=treeitem]').length"), 10)
check("tree", "row click also selects",
      js("__P__.querySelector('.is-selected .jm-tree__label')?.textContent.trim()"), "第一章 走进 Vue 3")

js("(()=>{__P__.querySelector('.jm-tree').__vueParentComponent.exposed.collapseAll();})()")
time.sleep(0.3)
check("tree", "collapseAll()", js("__P__.querySelectorAll('[role=treeitem]').length"), 3)
js("(()=>{__P__.querySelector('.jm-tree').__vueParentComponent.exposed.expandAll();})()")
time.sleep(0.3)
check("tree", "expandAll()", js("__P__.querySelectorAll('[role=treeitem]').length"), 12)

# 键盘导航
js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const row=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.textContent.includes('第一章'));
  row.focus();})()""")
key("ArrowDown")
time.sleep(0.2)
check("tree", "ArrowDown moves focus", js(
    "__P__.querySelector('[role=treeitem]:focus .jm-tree__label')?.textContent.trim()"),
    "1.1 环境搭建与项目结构")
key("ArrowUp")
key("End")
time.sleep(0.2)
check("tree", "End jumps to last visible", js(
    "__P__.querySelector('[role=treeitem]:focus .jm-tree__label')?.textContent.trim()"),
    "3.2 单元测试入门")
key("Enter")
time.sleep(0.3)
check("tree", "Enter selects focused node",
      js("__P__.querySelector('.is-selected .jm-tree__label')?.textContent.trim()"),
      "3.2 单元测试入门")

# --- demo2 复选 ---
js("document.querySelectorAll('.demo-page')[1].scrollIntoView({block:'center'})")
time.sleep(0.6)
info2 = js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const checks=[...root.querySelectorAll('.jm-tree__check')];
  const tsRow=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.textContent.includes('TypeScript'));
  return {hasCheck:checks.length>0,
    indeterminate0:checks.filter(c=>c.classList.contains('is-indeterminate')).length,
    checked0:checks.filter(c=>c.classList.contains('is-checked')).length,
    disabledLeaf:tsRow?tsRow.getAttribute('aria-disabled')==='true':null};})()""", 1)
check("tree", "checkbox rendered", info2["hasCheck"], True)
check("tree", "initial: fe half-checked", info2["indeterminate0"], 1)
check("tree", "initial: 1 leaf checked", info2["checked0"], 1)
check("tree", "disabled leaf aria", info2["disabledLeaf"], True)

js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const row=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.querySelector('.jm-tree__label')?.textContent.trim()==='前端基础');
  row.querySelector('.jm-tree__check').click();})()""", 1)
time.sleep(0.4)
after_check = js("""(()=>{const root=__P__.querySelector('.jm-tree');
  const fe=[...root.querySelectorAll('[role=treeitem]')].find(n=>n.querySelector('.jm-tree__label')?.textContent.trim()==='前端基础');
  return {feState:fe.querySelector('.jm-tree__check').className.includes('is-checked')?'checked':'other',
    checkedCount:root.querySelectorAll('.jm-tree__check.is-checked').length,
    tip:__P__.querySelector('.demo-tip')?.textContent.trim()};})()""", 1)
check("tree", "checking parent checks whole subtree",
      (after_check["feState"], after_check["checkedCount"]), ("checked", 4))
check("tree", "check event updates tip", "已选 4 项" in after_check["tip"], True)

# 受控值回写由 v-model 完成；直接从组件读 props 验证双向
check("tree", "checked-values synced", js(
    "__P__.querySelector('.jm-tree').__vueParentComponent.props.checkedValues.length", 1), 4)

press_button("推荐全选")
time.sleep(0.5)
check("tree", "setCheckedValues fills subtree (disabled leaf stays half)",
      js("__P__.querySelectorAll('.jm-tree__check.is-checked').length", 1), 6)

# --- demo3 懒加载 ---
js("document.querySelectorAll('.demo-page')[2].scrollIntoView({block:'center'})")
time.sleep(0.5)
js("""(()=>{const root=__P__.querySelector('.jm-tree');
  [...root.querySelectorAll('[role=treeitem]')][0].querySelector('.jm-tree__arrow').click();})()""", 2)
time.sleep(0.25)
check("tree", "lazy loading spinner", js("__P__.querySelector('.jm-tree__spin') !== null", 2), True)
time.sleep(1.3)
check("tree", "lazy children arrive", js("__P__.querySelectorAll('[role=treeitem]').length", 2), 6)

js("""(()=>{const root=__P__.querySelector('.jm-tree');
  [...root.querySelectorAll('[role=treeitem]')][0].querySelector('.jm-tree__arrow').click();})()""", 2)
time.sleep(0.3)
js("""(()=>{const root=__P__.querySelector('.jm-tree');
  [...root.querySelectorAll('[role=treeitem]')][0].querySelector('.jm-tree__arrow').click();})()""", 2)
time.sleep(0.5)
check("tree", "second expand uses cache (no spinner)",
      js("__P__.querySelector('.jm-tree__spin') === null", 2), True)
check("tree", "cached children still there",
      js("__P__.querySelectorAll('[role=treeitem]').length", 2), 6)

js("""(()=>{const root=__P__.querySelector('.jm-tree');
  [...root.querySelectorAll('[role=treeitem]')].find(n=>n.textContent.includes('第二章'))
    .querySelector('.jm-tree__arrow').click();})()""", 2)
time.sleep(1.5)
check("tree", "c2 loaded too", js("__P__.querySelectorAll('[role=treeitem]').length", 2), 8)

# 过滤
set_input("__P__.querySelector('input')", "插槽", 2)
time.sleep(1.0)
filtered = js("""(()=>{const page=__P__;
  const treeComp=page.querySelector('.jm-tree').__vueParentComponent;
  const labels=[...page.querySelectorAll('.jm-tree__label')].map(l=>l.textContent.trim());
  return {count:labels.length,hit:labels.some(l=>l.includes('插槽')),mark:page.querySelectorAll('.jm-tree__hit').length,
    kw:page.__vueParentComponent.setupState.keyword,
    filterProp:treeComp.props.filter};})()""", 2)
print("  diag filter:", json.dumps(filtered, ensure_ascii=False))
check("tree", "filter keeps matched branch", filtered["count"], 2)
check("tree", "filter hit present", filtered["hit"], True)
check("tree", "filter highlights", filtered["mark"], 1)

# ================= TreeSelect =================
print("== tree-select ==")
goto("/components/tree-select")
wait_for("document.querySelectorAll('.jm-tree-select').length")
time.sleep(1.5)
info_ts = js("""(()=>{const triggers=[...__P__.querySelectorAll('.jm-tree-select')];
  return {path:triggers[0].querySelector('.jm-tree-select__value')?.textContent.trim(),
    placeholder:triggers[1].querySelector('.jm-tree-select__value')?.textContent.trim(),
    disabled:triggers[2].querySelector('.jm-tree-select__trigger').disabled};})()""")
check("tree-select", "trigger shows full path", info_ts["path"], "数学 / 函数 / 二次函数")
check("tree-select", "placeholder when empty", info_ts["placeholder"], "未选择时显示占位文案")
check("tree-select", "disabled trigger", info_ts["disabled"], True)

js("__P__.querySelectorAll('.jm-tree-select__trigger')[0].click()")
time.sleep(0.8)
panel = js("""(()=>{const p=__P__.querySelector('.jm-tree-select__panel');
  if(!p) return null;
  const tree=p.querySelector('.jm-tree');
  return {open:!!p,
    title:p.querySelector('.jm-tree-select__title')?.textContent.trim(),
    search:!!p.querySelector('input'),
    selectedInTree:!!tree.querySelector('.is-selected'),
    expandedAncestors:[...tree.querySelectorAll('[aria-expanded=true] .jm-tree__label')].map(l=>l.textContent.trim())};})()""")
check("tree-select", "panel opens", panel["open"], True)
check("tree-select", "panel title", panel["title"], "选择知识点")
check("tree-select", "search box present", panel["search"], True)
check("tree-select", "selected highlighted in tree", panel["selectedInTree"], True)
check("tree-select", "ancestors auto-expanded", panel["expandedAncestors"], ["数学", "函数"])

set_input("__P__.querySelector('.jm-tree-select__panel input')", "立体")
time.sleep(0.6)
search_hit = js("""(()=>{const p=__P__.querySelector('.jm-tree-select__panel');
  return [...p.querySelectorAll('.jm-tree__label')].map(l=>l.textContent.trim());})()""")
check("tree-select", "search keeps matched path", search_hit, ["数学", "立体几何"])

js("""(()=>{const p=__P__.querySelector('.jm-tree-select__panel');
  const row=[...p.querySelectorAll('[role=treeitem]')].find(n=>n.querySelector('.jm-tree__label')?.textContent.includes('立体几何'));
  row.click();})()""")
time.sleep(0.8)
after_pick = js("""(()=>{const trigger=__P__.querySelectorAll('.jm-tree-select__trigger')[0];
  return {closed:!__P__.querySelector('.jm-tree-select__panel'),
    value:trigger.querySelector('.jm-tree-select__value')?.textContent.trim()};})()""")
check("tree-select", "panel closes after pick", after_pick["closed"], True)
check("tree-select", "trigger updates", after_pick["value"], "数学 / 立体几何")

js("__P__.querySelectorAll('.jm-tree-select__clear')[0].click()")
time.sleep(0.4)
after_clear = js("""(()=>{const trigger=__P__.querySelectorAll('.jm-tree-select__trigger')[0];
  const v=trigger.querySelector('.jm-tree-select__value');
  return {text:v.textContent.trim(),isPlaceholder:v.classList.contains('is-placeholder')};})()""")
check("tree-select", "clear resets to placeholder",
      (after_clear["text"], after_clear["isPlaceholder"]), ("请选择", True))

# ================= LoadingBar =================
print("== loading-bar ==")
goto("/components/loading-bar")
wait_for("document.querySelectorAll('.demo-page button').length")
time.sleep(1.5)

press_button("失败")
time.sleep(1.7)
fail_state = js("""(()=>{const bar=document.querySelector('.jm-loading-bar');
  return {visible:bar?.classList.contains('is-visible'),failed:bar?.classList.contains('is-failed')};})()""")
check("loading-bar", "error state shows red", (fail_state["visible"], fail_state["failed"]), (True, True))
time.sleep(1.0)
check("loading-bar", "bar hides after settle",
      js("document.querySelector('.jm-loading-bar').classList.contains('is-visible') === false"), True)

press_button("成功")
time.sleep(0.6)
check("loading-bar", "bar visible while pending",
      js("document.querySelector('.jm-loading-bar').classList.contains('is-visible')"), True)
mid = js("Number(document.querySelector('.jm-loading-bar').getAttribute('aria-valuenow'))")
check("loading-bar", "auto progress below 94", mid, lambda v: 0 < v < 94)
time.sleep(2.4)
check("loading-bar", "finished and reset",
      js("Number(document.querySelector('.jm-loading-bar').getAttribute('aria-valuenow') || 0)"), 0)

# 并发：demo 里的「两个并发任务」，0.9s 收一个、2s 收另一个
press_button("两个并发任务")
time.sleep(1.3)
check("loading-bar", "first finish keeps bar alive",
      js("document.querySelector('.jm-loading-bar').classList.contains('is-visible')"), True)
time.sleep(1.4)
check("loading-bar", "last finish hides bar",
      js("document.querySelector('.jm-loading-bar').classList.contains('is-visible') === false"), True)

# ================= Transfer =================
print("== transfer ==")
goto("/components/transfer")
wait_for("document.querySelectorAll('.jm-transfer').length")
time.sleep(1.5)

t0 = js("""(()=>{const p=__P__.querySelectorAll('.jm-transfer__panel');
  return {left:p[0].querySelectorAll('.jm-transfer__item').length,
    right:p[1].querySelectorAll('.jm-transfer__item').length};})()""")
check("transfer", "initial 6 left / 2 right", (t0["left"], t0["right"]), (6, 2))

js("""(()=>{const items=__P__.querySelectorAll('.jm-transfer__panel')[0].querySelectorAll('.jm-transfer__item');
  items[0].click();items[1].click();})()""")
time.sleep(0.3)
check("transfer", "add button counts selection", js(
    "[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('添加'))?.textContent.trim()"),
    "添加 2")
js("[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('添加')).click()")
time.sleep(0.4)
t1 = js("""(()=>{const p=__P__.querySelectorAll('.jm-transfer__panel');
  return {left:p[0].querySelectorAll('.jm-transfer__item').length,
    right:p[1].querySelectorAll('.jm-transfer__item').length};})()""")
check("transfer", "moved to right", (t1["left"], t1["right"]), (4, 4))
check("transfer", "change event fired",
      "移入 2 项" in js("__P__.querySelector('.demo-tip')?.textContent.trim()"), True)

js("__P__.querySelectorAll('.jm-transfer__panel')[0].querySelector('.jm-transfer__all').click()")
time.sleep(0.3)
check("transfer", "select all counts (disabled excluded)", js(
    "[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('添加'))?.textContent.trim()"),
    "添加 3")

set_input("__P__.querySelectorAll('.jm-transfer__panel')[0].querySelector('input')", "插槽")
time.sleep(0.4)
check("transfer", "search filters left list",
      js("__P__.querySelectorAll('.jm-transfer__panel')[0].querySelectorAll('.jm-transfer__item').length"), 1)

# 移除一项（先清左侧搜索框，否则计数是被过滤后的）
set_input("__P__.querySelectorAll('.jm-transfer__panel')[0].querySelector('input')", "")
time.sleep(0.4)

# 禁用项不可勾选（l8 留在左侧面板）
disabled_ok = js("""(()=>{const items=__P__.querySelectorAll('.jm-transfer__panel')[0].querySelectorAll('.jm-transfer__item');
  const disabled=[...items].find(i=>i.classList.contains('is-disabled'));
  if(!disabled) return 'no-disabled';
  disabled.click();
  return __P__.querySelectorAll('.jm-transfer__item.is-checked.is-disabled').length > 0;})()""")
check("transfer", "disabled item cannot be checked", disabled_ok, False)

js("""(()=>{const items=__P__.querySelectorAll('.jm-transfer__panel')[1].querySelectorAll('.jm-transfer__item');
  items[0].click();})()""")
time.sleep(0.25)
js("[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('移除')).click()")
time.sleep(0.4)
t2 = js("""(()=>{const p=__P__.querySelectorAll('.jm-transfer__panel');
  return {left:p[0].querySelectorAll('.jm-transfer__item').length,
    right:p[1].querySelectorAll('.jm-transfer__item').length};})()""")
check("transfer", "moved back to left", (t2["left"], t2["right"]), (5, 3))

# ================= Table =================
print("== table ==")
goto("/components/table")
wait_for("document.querySelectorAll('.jm-table').length >= 2")
time.sleep(1.5)

info_tb = js("""(()=>{const wrap=__P__.querySelector('.jm-table__wrap');
  const table=wrap.querySelector('.jm-table');
  const firstRow=table.querySelector('tbody tr');
  return {headers:[...table.querySelectorAll('thead th')].map(t=>t.textContent.trim()),
    rows:table.querySelectorAll('tbody tr').length,
    amountRight:!!table.querySelector('td.is-right'),
    tag:!!firstRow.querySelector('.jm-tag'),
    stripe:table.classList.contains('is-stripe')};})()""")
check("table", "columns rendered", info_tb["headers"], ["订单号", "商品", "金额", "状态"])
check("table", "4 rows", info_tb["rows"], 4)
check("table", "amount column right aligned", info_tb["amountRight"], True)
check("table", "status cell uses slot with Tag", info_tb["tag"], True)
check("table", "stripe enabled", info_tb["stripe"], True)

js("__P__.querySelectorAll('.jm-table tbody tr')[1].click()")
time.sleep(0.3)
check("table", "row click fires",
      js("__P__.querySelector('.demo-tip')?.textContent.trim()").startswith("打开订单 JM20261116002"), True)

wide = js("""(()=>{const wrap=__P__.querySelector('.jm-table__wrap');
  return {scrollable:wrap.scrollWidth>wrap.clientWidth,
    headers:wrap.querySelectorAll('thead th').length};})()""", 1)
check("table", "wide table scrollable", wide["scrollable"], True)
check("table", "wide table 7 columns", wide["headers"], 7)

js("(()=>{__P__.querySelector('.jm-table__wrap').scrollLeft=200;})()", 1)
time.sleep(0.4)
fixed_col = js("""(()=>{const wrap=__P__.querySelector('.jm-table__wrap');
  const first=wrap.querySelector('tbody td');
  const r=first.getBoundingClientRect();
  const wrapR=wrap.getBoundingClientRect();
  return {staysLeft:r.left-wrapR.left<30,hasShadow:getComputedStyle(first).boxShadow!=='none'};})()""", 1)
check("table", "fixed first column stays visible", fixed_col["staysLeft"], True)
check("table", "fixed column has divider shadow", fixed_col["hasShadow"], True)

press_button("清空数据")
time.sleep(0.5)
check("table", "empty state text",
      js("__P__.querySelector('.jm-table__empty')?.textContent.trim()", 1), "本学期还没有成绩记录")
press_button("填回数据")
time.sleep(0.4)
check("table", "data restored", js("__P__.querySelectorAll('.jm-table tbody tr').length", 1), 4)

# 全局错误
check("global", "no page errors", tab.js("JSON.stringify(window.__errs)"), "[]")

print()
print("total=%d fail=%d" % (total, len(fails)))
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL PASS")
