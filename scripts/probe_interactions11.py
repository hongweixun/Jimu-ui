"""异步交互回填批（Uploader 进度 / Tabs beforeChange / SwipeCell beforeClose /
CheckboxGroup max-min / Toast 图标与关闭 / Popup beforeClose）回归。"""
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


def add_files(wall_expr, names):
    """用 DataTransfer 造 File 并触发 input change（等价于用户选文件）"""
    js = f"""(()=>{{
  const root = {wall_expr};
  const input = root.querySelector('input[type=file]');
  const dt = new DataTransfer();
  {names}
  input.files = dt.files;
  input.dispatchEvent(new Event('change', {{ bubbles: true }}));
  return dt.files.length;
}})()"""
    return tab.js(js)


def add(files):
    return "\n  ".join(
        f"dt.items.add(new File([new Blob(['x'], {{ type: 'image/png' }})], '{n}', {{ type: 'image/png' }}));"
        for n in files
    )


def wait_for(expr, timeout=4.0, interval=0.08):
    end = time.time() + timeout
    while time.time() < end:
        if tab.js(expr):
            return True
        time.sleep(interval)
    return False


# ---------------- Uploader：自动上传 / 进度 / 失败重试 ----------------
tab.goto(f"{BASE}/components/uploader", wait=4)
auto = f"{page('自动上传：选完立刻传')}.querySelectorAll('.jm-uploader')[0]"

add_files(auto, add(["ok.png"]))
time.sleep(0.15)
check("upload", "progress overlay appears", tab.js(f"!!{auto}.querySelector('.jm-uploader__progress')"), True)
check("upload", "progress has percent text", tab.js(
    f"{auto}.querySelector('.jm-uploader__progress-num')?.textContent"
), lambda v: isinstance(v, str) and v.endswith("%"))
check("upload", "progress aria value", tab.js(
    f"{auto}.querySelector('.jm-uploader__progress')?.getAttribute('aria-valuenow')"
), lambda v: v is not None and 0 <= int(v) <= 100)

done = wait_for(f"!{auto}.querySelector('.jm-uploader__progress')", timeout=4)
check("upload", "progress finishes and clears", done, True)
check("upload", "success event updates log", tab.js(f"{page('自动上传：选完立刻传')}.querySelector('.state').textContent"), "ok.png 上传成功")

# 失败：文件名带 fail，第一次必失败
add_files(auto, add(["fail.png"]))
time.sleep(0.2)
wait_for(f"!!{auto}.querySelector('.jm-uploader__retry')", timeout=4)
check("upload", "failed file shows retry", tab.js(
    f"{auto}.querySelector('.jm-uploader__retry')?.textContent.trim()"
), "重试")
check("upload", "error event carries message", tab.js(
    f"{page('自动上传：选完立刻传')}.querySelector('.state').textContent"
), lambda v: "失败" in str(v) and "网络异常" in str(v))

# 点重试 → 第二次成功
tab.js(f"{auto}.querySelector('.jm-uploader__retry').click()")
time.sleep(0.15)
check("upload", "retry restarts progress", tab.js(f"!!{auto}.querySelector('.jm-uploader__progress')"), True)
retry_ok = wait_for(
    f"!!{page('自动上传：选完立刻传')}.querySelector('.state') && "
    f"{page('自动上传：选完立刻传')}.querySelector('.state').textContent.includes('上传成功')",
    timeout=5,
)
check("upload", "retry succeeds", retry_ok, True)
check("upload", "retry success log", tab.js(
    f"{page('自动上传：选完立刻传')}.querySelector('.state').textContent"
), "fail.png 上传成功")

# 手动上传
manual = f"{page('自动上传：选完立刻传')}.querySelectorAll('.jm-uploader')[1]"
add_files(manual, add(["a.png", "b.png"]))
time.sleep(0.3)
check("upload", "manual mode shows pending badges", tab.js(
    f"[...{manual}.querySelectorAll('.jm-uploader__badge')].map(b=>b.textContent.trim())"
), ["待上传", "待上传"])
check("upload", "manual mode not uploading yet", tab.js(f"!{manual}.querySelector('.jm-uploader__progress')"), True)
check("upload", "submit button counts pending", tab.js(
    f"{page('自动上传：选完立刻传')}.querySelector('.jm-button')?.textContent.replace(/\\s+/g,'')"
), lambda v: "2个待上传" in str(v))

tab.js(f"[...{page('自动上传：选完立刻传')}.querySelectorAll('.jm-button')].find(b=>b.textContent.includes('开始上传')).click()")
time.sleep(0.25)
check("upload", "submit starts uploads", tab.js(f"{manual}.querySelectorAll('.jm-uploader__progress').length"), 2)
wait_for(f"!{manual}.querySelector('.jm-uploader__badge')", timeout=6)
check("upload", "pending badges cleared after submit", tab.js(
    f"{manual}.querySelectorAll('.jm-uploader__badge').length"
), 0)

# ---------------- Tabs beforeChange ----------------
tab.goto(f"{BASE}/components/tabs", wait=3.5)
tabs_demo = page("第 1 步：填资料")
check("tabs", "initial active is basic", tab.js(
    f"{tabs_demo}.querySelector('.jm-tabs__item.is-active')?.textContent.trim()"
), "基本信息")

tab.js(f"[...{tabs_demo}.querySelectorAll('.jm-tabs__item')].find(t=>t.textContent.includes('提交结果')).click()")
time.sleep(0.4)
check("tabs", "dialog asks before leaving", tab.js("!!document.querySelector('.jm-dialog')"), True)
check("tabs", "tab not switched while asking", tab.js(
    f"{tabs_demo}.querySelector('.jm-tabs__item.is-active')?.textContent.trim()"
), "基本信息")

tab.js("document.querySelector('.jm-dialog__button--cancel')?.click()")
time.sleep(0.4)
check("tabs", "cancel keeps tab", tab.js(
    f"{tabs_demo}.querySelector('.jm-tabs__item.is-active')?.textContent.trim()"
), "基本信息")
check("tabs", "cancel counted as blocked", tab.js(
    f"{tabs_demo}.querySelector('.state')?.textContent"
), lambda v: "已拦截 1 次" in str(v))

tab.js(f"[...{tabs_demo}.querySelectorAll('.jm-tabs__item')].find(t=>t.textContent.includes('提交结果')).click()")
time.sleep(0.35)
tab.js("document.querySelector('.jm-dialog__button--primary')?.click()")
time.sleep(0.5)
check("tabs", "confirm switches tab", tab.js(
    f"{tabs_demo}.querySelector('.jm-tabs__item.is-active')?.textContent.trim()"
), "提交结果")

# ---------------- SwipeCell beforeClose ----------------
tab.goto(f"{BASE}/components/swipe-cell", wait=3.5)
sc = page("左滑 → 点「删除」")
rows = f"{sc}.querySelectorAll('.jm-swipe-cell')"
check("swipe", "three rows", tab.js(f"{rows}.length"), 3)

box = tab.js(f"(()=>{{const el={rows}[0];el.scrollIntoView({{block:'center'}});"
          f"const r=el.getBoundingClientRect();return {{x:r.left+r.width*0.8,y:r.top+r.height/2}}}})()")
time.sleep(0.3)
tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": box["x"], "y": box["y"]}]})
for i in range(1, 7):
    tab.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": box["x"] - 20 * i, "y": box["y"]}]})
    time.sleep(0.02)
tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
time.sleep(0.5)
open_offset = tab.js(f"{rows}[0].querySelector('.jm-swipe-cell__track').style.getPropertyValue('--jm-swipe-cell-offset')")
check("swipe", "row opens on swipe", open_offset, lambda v: v and float(str(v).replace("px", "")) < -40)

tab.js(f"{rows}[0].querySelector('.action').click()")
time.sleep(0.4)
check("swipe", "confirm dialog appears", tab.js("!!document.querySelector('.jm-dialog')"), True)
check("swipe", "cell stays open before confirm", tab.js(
    f"!!{rows}[0].querySelector('.jm-swipe-cell__track')"
), True)
check("swipe", "row not deleted yet", tab.js(f"{rows}.length"), 3)

tab.js("document.querySelector('.jm-dialog__button--cancel')?.click()")
time.sleep(0.4)
check("swipe", "cancel keeps row", tab.js(f"{rows}.length"), 3)
check("swipe", "cancel keeps cell open", tab.js(
    f"{rows}[0].querySelector('.jm-swipe-cell__track').style.getPropertyValue('--jm-swipe-cell-offset')"
), lambda v: v and float(str(v).replace("px", "")) < -40)

tab.js(f"{rows}[0].querySelector('.action').click()")
time.sleep(0.35)
tab.js("document.querySelector('.jm-dialog__button--primary')?.click()")
time.sleep(0.6)
check("swipe", "confirm deletes row", tab.js(f"{rows}.length"), 2)

# ---------------- CheckboxGroup max / min ----------------
tab.goto(f"{BASE}/components/checkbox", wait=3.5)
cb = page("最多选 3 门")
items = f"{cb}.querySelectorAll('.jm-checkbox')"
check("checkbox", "five options", tab.js(f"{items}.length"), 5)

tab.js(f"{items}[1].click()")
time.sleep(0.15)
tab.js(f"{items}[2].click()")
time.sleep(0.25)
check("checkbox", "three selected", tab.js(f"{cb}.querySelectorAll('.jm-checkbox.is-checked').length"), 3)

tab.js(f"{items}[3].click()")
time.sleep(0.35)
check("checkbox", "fourth blocked by max", tab.js(f"{cb}.querySelectorAll('.jm-checkbox.is-checked').length"), 3)
check("checkbox", "toast tells max", tab.js("document.querySelector('.jm-toast__text')?.textContent"), "最多选 3 门，先取消一门再选")

time.sleep(2.2)  # 等 toast 消失
# 取消两个，剩 1 个（min=1），再取消应被拦
tab.js(f"{items}[1].click()")
time.sleep(0.15)
tab.js(f"{items}[2].click()")
time.sleep(0.25)
check("checkbox", "back to one selected", tab.js(f"{cb}.querySelectorAll('.jm-checkbox.is-checked').length"), 1)
tab.js(f"{items}[0].click()")
time.sleep(0.4)
check("checkbox", "min blocks unchecking last", tab.js(f"{cb}.querySelectorAll('.jm-checkbox.is-checked').length"), 1)
check("checkbox", "toast tells min", tab.js("document.querySelector('.jm-toast__text')?.textContent"), "至少保留 1 门")

# ---------------- Toast：图标 / 点击关闭 / onClose ----------------
tab.goto(f"{BASE}/components/toast", wait=3.5)
ts = page("自定义图标")
tab.js(f"[...{ts}.querySelectorAll('.jm-button')].find(b=>b.textContent.includes('自定义图标')).click()")
time.sleep(0.4)
check("toast", "custom icon replaces default", tab.js(
    f"{ts}.querySelectorAll('.jm-toast__icon svg path').length > 0"
), True)
check("toast", "icon uses requested glyph", tab.js(
    f"{ts}.querySelector('.jm-toast__icon svg')?.getAttribute('viewBox')"
), "0 0 24 24")

tab.js(f"[...{ts}.querySelectorAll('.jm-button')].find(b=>b.textContent.includes('点击关闭')).click()")
time.sleep(0.4)
check("toast", "closeOnClick makes it clickable", tab.js(
    f"{ts}.querySelector('.jm-toast')?.classList.contains('is-clickable')"
), True)
check("toast", "clickOnClick pointer events auto", tab.js(
    f"getComputedStyle({ts}.querySelector('.jm-toast')).pointerEvents"
), "auto")
tab.js(f"{ts}.querySelector('.jm-toast').click()")
time.sleep(0.4)
check("toast", "click closes toast", tab.js(f"!!{ts}.querySelector('.jm-toast')"), False)
check("toast", "onClose fired on click", tab.js(f"{ts}.querySelector('.state')?.textContent"), "手动点击关闭，回调已触发")

# 自动消失也会回调
tab.js(f"[...{ts}.querySelectorAll('.jm-button')].find(b=>b.textContent.includes('自定义图标')).click()")
time.sleep(2.6)
check("toast", "onClose fired on auto dismiss", tab.js(f"{ts}.querySelector('.state')?.textContent"), lambda v: "自动消失" in str(v))

# ---------------- Popup beforeClose ----------------
tab.goto(f"{BASE}/components/popup", wait=3.5)
pp = page("关闭前拦截：有未保存内容时先确认")
tab.js(f"[...{pp}.querySelectorAll('.jm-button')].find(b=>b.textContent.includes('打开弹层')).click()")
time.sleep(0.5)
check("popup", "popup opens", tab.js(f"!!{pp}.querySelector('.jm-popup')"), True)

tab.js(f"{pp}.querySelector('.jm-popup__mask').click()")
time.sleep(0.45)
check("popup", "mask click asks first", tab.js("!!document.querySelector('.jm-dialog')"), True)
check("popup", "popup stays open while asking", tab.js(f"!!{pp}.querySelector('.jm-popup')"), True)

tab.js("document.querySelector('.jm-dialog__button--cancel')?.click()")
time.sleep(0.45)
check("popup", "cancel keeps popup open", tab.js(f"!!{pp}.querySelector('.jm-popup')"), True)
check("popup", "cancel message shown", tab.js(f"{pp}.querySelector('.state')?.textContent"), "取消关闭，弹层还在")

tab.js(f"{pp}.querySelector('.jm-popup__mask').click()")
time.sleep(0.4)
tab.js("document.querySelector('.jm-dialog__button--primary')?.click()")
time.sleep(0.6)
check("popup", "confirm closes popup", tab.js(f"!!{pp}.querySelector('.jm-popup')"), False)
check("popup", "close callback runs", tab.js(f"{pp}.querySelector('.state')?.textContent"), "已关闭（beforeClose 放行）")

print(f"\n合计 {ok + fail} 项：PASS {ok}，FAIL {fail}")
sys.exit(1 if fail else 0)
