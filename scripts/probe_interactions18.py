# -*- coding: utf-8 -*-
"""第十九批（0.21.0）探针：Form 自定义校验 / Uploader 双布局与比例 / Scanner 扫描动效"""
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
    ok = actual == expect or (callable(expect) and expect(actual))
    if ok:
        print(f"  PASS {section}/{name}: {json.dumps(actual, ensure_ascii=False, default=str)[:100]}")
    else:
        fails.append(f"{section}/{name}")
        print(f"  FAIL {section}/{name}: got {json.dumps(actual, ensure_ascii=False, default=str)[:220]}, want {expect}")


def js(code, page=0):
    return tab.js(code.replace("__P__", "document.querySelectorAll('.demo-page')[" + str(page) + "]"))


def set_input(sel_expr, value, page=0):
    return js(
        "(()=>{const input=" + sel_expr + ";"
        "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
        "setter.call(input,'" + value + "');"
        "input.dispatchEvent(new Event('input',{bubbles:true}));})()",
        page,
    )


def set_input_until(sel_expr, value, index=None, page=2, timeout=3.0):
    """输入并确认 v-model 生效（clearable 按钮随 modelValue 出现）；事件偶发首丢时重发"""
    end = time.time() + timeout
    idx = ""
    if index is not None:
        idx = "[" + str(index) + "]"
    while time.time() < end:
        set_input("__P__.querySelectorAll('.jm-form .jm-input input')" + idx, value, page)
        time.sleep(0.35)
        ok = js(
            "(()=>{const input=__P__.querySelectorAll('.jm-form .jm-input input')" + idx + ";"
            "return input.value==='" + value + "' && !!input.closest('.jm-input').querySelector('.jm-input__clear');})()",
            page,
        )
        if ok:
            return True
    return False


def press_button(text, page=0):
    js("(()=>{const b=[...__P__.querySelectorAll('button')].find(x=>x.textContent.trim().includes('"
       + text + "'));if(b){b.focus();b.click()}})()", page)


def wait_for(expr, timeout=6.0):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(0.15)
    return False


def goto(path):
    tab.goto(BASE + path, wait=6)
    tab.js("window.__errs=[];window.addEventListener('error',e=>window.__errs.push(String(e.message)))")


def center(expr, page=0):
    return js(
        "(()=>{const el=" + expr + ";if(!el)return null;el.scrollIntoView({block:'center'});"
        "const r=el.getBoundingClientRect();"
        "return {x:r.left+r.width/2,y:r.top+r.height/2};})()",
        page,
    )


def mouse_click(x, y):
    tab.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    tab.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


ensure_edge()
tab = new_tab()
tab.send("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 1000, "deviceScaleFactor": 1, "mobile": False})

# ================= Form 自定义校验 =================
print("== form ==")
goto("/components/form")
wait_for("document.querySelectorAll('.demo-page').length >= 3")

# VitePress 先出 SSG 静态 HTML，Vue hydration 完成后 v-model 才绑定。
# 信号：setter 输入后 Input 的 clearable 按钮出现（showClear 依赖 modelValue 非空）。
def wait_hydrated(timeout=15.0):
    end = time.time() + timeout
    while time.time() < end:
        tab.js("""(()=>{const page=document.querySelectorAll('.demo-page')[2];if(!page)return;
          const input=page.querySelector('.jm-form .jm-input input');if(!input)return;
          const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
          setter.call(input,'probe');
          input.dispatchEvent(new Event('input',{bubbles:true}));})()""")
        time.sleep(0.5)
        bound = tab.js("""(()=>{const page=document.querySelectorAll('.demo-page')[2];
          return !!page.querySelector('.jm-input__clear');})()""")
        tab.js("""(()=>{const page=document.querySelectorAll('.demo-page')[2];
          const input=page.querySelector('.jm-form .jm-input input');
          const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
          setter.call(input,'');
          input.dispatchEvent(new Event('input',{bubbles:true}));})()""")
        time.sleep(0.2)
        if bound:
            time.sleep(0.3)
            return True
    return False

hydrated = wait_hydrated()
print("  hydrated:", hydrated)

P = 2  # validate demo
check("form", "validate demo present", js("!!__P__.querySelector('.jm-form')", P), True)
check("form", "trigger switch buttons", js("[...__P__.querySelectorAll('button')].filter(b=>b.textContent.includes('校验')).length", P), 2)

def errors(page=P):
    return js("[...__P__.querySelectorAll('.jm-form-item__error, .jm-input__error-message')].map(e=>e.textContent.trim())", page)


ERR_SEL = ".jm-form-item__error, .jm-input__error-message"


def wait_error(msg, timeout=4.0, page=P):
    """轮询等待某条错误文案出现"""
    return wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    )


def wait_error_gone(msg, timeout=4.0, page=P):
    """轮询等待某条错误文案消失（false=还在，取反表示通过）"""
    return not wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    )


def blur_input(index, page=P):
    """失焦指定 input；先 focus 再 blur，更接近真实事件序列"""
    js(
        "(()=>{const input=__P__.querySelectorAll('.jm-form .jm-input input')[" + str(index) + "];"
        "input.focus();input.dispatchEvent(new Event('blur',{bubbles:true}));})()",
        page,
    )


def blur_until(msg, index, timeout=2.5, page=P):
    """dispatch blur → 轮询错误出现；超时则重发一次（合成事件偶发首丢）"""
    blur_input(index, page)
    if wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    ):
        return True
    blur_input(index, page)
    return wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    )


def blur_until_gone(msg, index, timeout=2.5, page=P):
    blur_input(index, page)
    if not wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    ):
        return True
    blur_input(index, page)
    return not wait_for(
        "[...document.querySelectorAll('.demo-page')[" + str(page) + "].querySelectorAll('" + ERR_SEL + "')]"
        ".map(e=>e.textContent.trim()).some(t=>t.includes('" + msg + "'))",
        timeout,
    )


# 切到「仅失焦校验」：干净字段输入非法值不应实时报错（wait_hydrated 的清空
# 会在 username 留下 required 错误，属切换前的合法状态；用 password 验证实时性）
press_button("仅失焦校验", P)
time.sleep(0.3)

set_input_until(None, "123", 1, P)
time.sleep(0.6)
check("form", "blur-only mode: no realtime error on input",
      any("至少 6 位" in e for e in errors(P)), False)

# 失焦 → 异步查重（700ms）：admin 被注册，错误文案替换掉 required 提示
set_input_until(None, "admin", 0, P)
check("form", "async validator reports taken name", blur_until("已被注册", 0), True)

# 密码：至少 6 位（上面已填 123）
check("form", "sync validator min length", blur_until("至少 6 位", 1), True)

# 确认密码跨字段：与 password(123) 不一致
set_input_until(None, "abc", 2, P)
check("form", "cross-field validator", blur_until("两次输入的密码不一致", 2), True)

# 手机号 pattern
set_input_until(None, "12", 3, P)
check("form", "pattern rule message", blur_until("1 开头的 11 位", 3), True)

# 切回「失焦+输入校验」，把 password 改对 → 处于 error 态的字段输入过程全量复检立即恢复
press_button("失焦 + 输入校验", P)
time.sleep(0.3)
set_input_until(None, "abc123", 1, P)
check("form", "error-state recheck on change", wait_error_gone("至少 6 位"), True)

set_input_until(None, "abc123", 2, P)
check("form", "cross-field recover", wait_error_gone("两次输入的密码不一致"), True)

set_input_until(None, "13800138000", 3, P)
check("form", "pattern recover", wait_error_gone("1 开头的 11 位"), True)

# username 改合法值 + 失焦 → 查重通过（change 全量复检与 blur 任一生效即可）
set_input_until(None, "wangwu", 0, P)
blur_input(0)
time.sleep(1.0)
check("form", "async validator passes", wait_error_gone("已被注册", 6), True)

# 提交
submit_btn = center("[...__P__.querySelectorAll('button')].find(b=>b.textContent.trim()==='提交')", P)
mouse_click(submit_btn["x"], submit_btn["y"])
ok_submit = wait_for(
    "[...document.querySelectorAll('.demo-page')[2].querySelectorAll('.demo-tip')][0].textContent.startsWith('✅')",
    4,
)
if not ok_submit:
    mouse_click(submit_btn["x"], submit_btn["y"])
    ok_submit = wait_for(
        "[...document.querySelectorAll('.demo-page')[2].querySelectorAll('.demo-tip')][0].textContent.startsWith('✅')",
        4,
    )
check("form", "submit passes after fixes", ok_submit, True)

# ================= Uploader 布局与比例 =================
print("== uploader ==")
goto("/components/uploader")
wait_for("__P__".replace("__P__", "document.querySelectorAll('.demo-page')") + ".length >= 5")
time.sleep(2)

L = 4  # layout demo（phone:false 平铺）
r1 = js("""(()=>{const ups=__P__.querySelectorAll('.jm-uploader');
  const g1=ups[0].querySelector('.jm-uploader__item');
  const g2=ups[1].querySelector('.jm-uploader__item');
  const cs1=getComputedStyle(g1), cs2=getComputedStyle(g2);
  return {ratio1:cs1.aspectRatio, ratio2:cs2.aspectRatio,
    gridTrigger:!!ups[0].querySelector('.jm-uploader__trigger')};})()""", L)
check("uploader", "portrait ratio 3:4", r1["ratio1"], "3 / 4")
check("uploader", "wide ratio 16:9", r1["ratio2"], "16 / 9")
check("uploader", "grid keeps trigger", r1["gridTrigger"], True)

list_info = js("""(()=>{const up=__P__.querySelectorAll('.jm-uploader')[2];
  const rows=up.querySelectorAll('.jm-uploader-list__row');
  const count=up.querySelector('.jm-uploader-list__count');
  return {rows:rows.length, count:count?count.textContent.trim():'',
    addBtn:!!up.querySelector('.jm-uploader-list__add'),
    fileIcon:!!up.querySelector('.jm-uploader-list__fileicon'),
    thumb:!!up.querySelector('.jm-uploader-list__thumb'),
    noGridTrigger:!up.querySelector('.jm-uploader__trigger'),
    delBtns:up.querySelectorAll('.jm-uploader-list__del').length};})()""", L)
check("uploader", "list rows rendered", list_info["rows"], 2)
check("uploader", "list count text", list_info["count"], "已传 2/5")
check("uploader", "list add button", list_info["addBtn"], True)
check("uploader", "no-url file shows file icon", list_info["fileIcon"], True)
check("uploader", "url item shows thumb", list_info["thumb"], True)
check("uploader", "list hides grid trigger", list_info["noGridTrigger"], True)
check("uploader", "list delete buttons", list_info["delBtns"], 2)

# 删除一行 → 计数与行数联动
first_del = center("__P__.querySelectorAll('.jm-uploader-list__del')[0]", L)
mouse_click(first_del["x"], first_del["y"])
time.sleep(0.5)
after_del = js("""(()=>{const up=__P__.querySelectorAll('.jm-uploader')[2];
  return {rows:up.querySelectorAll('.jm-uploader-list__row').length,
    count:up.querySelector('.jm-uploader-list__count').textContent.trim()};})()""", L)
check("uploader", "after delete: 1 row", after_del["rows"], 1)
check("uploader", "after delete: count 1/5", after_del["count"], "已传 1/5")
check("uploader", "delete tip updated",
      js("__P__.querySelector('.demo-tip') ? __P__.querySelector('.demo-tip').textContent.includes('已删除') : false", L), True)

# ================= Scanner 扫描动效 =================
print("== scanner ==")
# 探针机器系统开了「减少动效」，模拟正常偏好再测动画
tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
goto("/components/scanner")
wait_for("document.querySelectorAll('.jm-scanner').length >= 2")
time.sleep(1.5)

scan0 = js("""(()=>{const s=__P__.querySelectorAll('.jm-scanner')[0];
  const line=s.querySelector('.jm-scanner__line');
  const cs=getComputedStyle(line);
  return {count:__P__.querySelectorAll('.jm-scanner').length,
    corners:s.querySelectorAll('.jm-scanner__corner').length,
    anim:cs.animationName, status:s.querySelector('.jm-scanner__status')?.textContent.trim()};})()""")
check("scanner", "two scanners rendered", scan0["count"], 2)
check("scanner", "four corner marks", scan0["corners"], 4)
check("scanner", "sweep animation running", scan0["anim"], "jm-scanner-sweep")
check("scanner", "status pill", scan0["status"], "扫描中…")

scan1 = js("""(()=>{const s=__P__.querySelectorAll('.jm-scanner')[1];
  return {color:s.style.getPropertyValue('--jm-scanner-line-color').trim(),
    grid1:s.classList.contains('has-grid')};})()""")
check("scanner", "custom green line color", scan1["color"], "#34D399")

# 点「停止扫描」→ active=false → 线淡出、状态消失
stop = center("[...__P__.querySelectorAll('button')].find(b=>b.textContent.includes('停止扫描'))")
mouse_click(stop["x"], stop["y"])
time.sleep(0.8)
after = js("""(()=>{const s=document.querySelectorAll('.demo-page')[0].querySelectorAll('.jm-scanner')[0];
  const line=s.querySelector('.jm-scanner__line');
  return {opacity:getComputedStyle(line).opacity,
    statusGone:!s.querySelector('.jm-scanner__status'),
    cornersStay:s.querySelectorAll('.jm-scanner__corner').length===4};})()""")
check("scanner", "line fades out when inactive", float(after["opacity"]) < 0.1, True)
check("scanner", "status pill removed", after["statusGone"], True)
check("scanner", "corners stay visible", after["cornersStay"], True)

# 全局错误
check("global", "no page errors", tab.js("JSON.stringify(window.__errs)"), "[]")

print()
print("total=%d fail=%d" % (total, len(fails)))
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL PASS")
