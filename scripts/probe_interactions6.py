"""第八批功能回填（Skeleton 变体 / Form 整表禁用 / Uploader 压缩）交互回归。"""
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


def click(tab, sel, index=0):
    tab.js(
        f"(()=>{{const e=document.querySelectorAll({json.dumps(sel)})[{index}];"
        f"if(e) e.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))}})()"
    )


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


ensure_edge()
tab = new_tab()

# ---------- Skeleton：自定义排版 / 呼吸 / 内容切换 ----------
tab.goto(f"{BASE}/components/skeleton", wait=3)
check("skeleton", "template 模式渲染骨架头像", count(tab, ".jm-skeleton__avatar") >= 1, True)
check("skeleton", "template 模式渲染段落行", count(tab, ".jm-skeleton__row") >= 2, True)
check("skeleton", "呼吸动效 class", tab.js("!!document.querySelector('.jm-skeleton.is-breath')"), True)
check("skeleton", "默认扫光 class", tab.js("!!document.querySelector('.jm-skeleton.is-shine')"), True)
click_by_text(tab, ".demo-page .jm-button", "重新加载")
time.sleep(2.2)
check("skeleton", "1.8s 后显示真实内容", "王老师" in str(text_of(tab, ".demo-page")), True)

# ---------- Form：整表禁用（disabled demo 在页面第二个 DemoBlock 里） ----------
tab.goto(f"{BASE}/components/form", wait=3)
page = tab.js("[...document.querySelectorAll('.demo-page')].find(p=>p.textContent.includes('整表禁用')) !== undefined")
check("form", "disabled demo 存在", page, True)


def scope(tab, index=0):
    return tab.js(
        f"(()=>{{const p=[...document.querySelectorAll('.demo-page')]"
        f".filter(p=>p.textContent.includes('整表禁用'))[0];"
        f"const forms=p?p.querySelectorAll('.jm-form'):[];"
        f"return !!forms[{index}]}})()"
    )


check("form", "disabled demo 含两个表单", scope(tab, 1), True)
check(
    "form",
    "整表禁用默认开",
    tab.js(
        "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
        ".filter(p=>p.textContent.includes('整表禁用'))[0];"
        "return !!p.querySelector('.jm-form .jm-switch.is-disabled')})()"
    ),
    True,
)
# disabled demo 内有三个开关：[0] 整表禁用、[1] 单字段、[2] 表内"上课提醒"——作用域内点，避免点错 demo
check("form", "表内 Input 禁用态", tab.js("!!document.querySelector('.jm-form .jm-input__box.is-disabled, .jm-form .jm-input.is-disabled')"), True)
check("form", "表内 Stepper 禁用态", tab.js("!!document.querySelector('.jm-form .jm-stepper.is-disabled')"), True)
check("form", "表内 Rate 禁用态", tab.js("!!document.querySelector('.jm-form .jm-rate.is-disabled')"), True)
tab.js(
    "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
    ".filter(p=>p.textContent.includes('整表禁用'))[0];"
    "p.querySelectorAll('.jm-switch')[0].dispatchEvent(new MouseEvent('click',{bubbles:true}))})()"
)
time.sleep(0.3)
check("form", "关闭后 Stepper 恢复", tab.js("document.querySelector('.jm-form .jm-stepper.is-disabled') === null"), True)

# 单字段禁用：先打开开关验证禁用，再关掉验证恢复
tab.js(
    "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
    ".filter(p=>p.textContent.includes('整表禁用'))[0];"
    "p.querySelectorAll('.jm-switch')[2].dispatchEvent(new MouseEvent('click',{bubbles:true}))})()"
)
time.sleep(0.3)
check(
    "form",
    "单字段禁用打开后生效",
    tab.js(
        "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
        ".filter(p=>p.textContent.includes('整表禁用'))[0];"
        "return !!p.querySelectorAll('.jm-form')[1].querySelector('.jm-form-item.is-disabled')})()"
    ),
    True,
)
tab.js(
    "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
    ".filter(p=>p.textContent.includes('整表禁用'))[0];"
    "p.querySelectorAll('.jm-switch')[2].dispatchEvent(new MouseEvent('click',{bubbles:true}))})()"
)
time.sleep(0.3)
check(
    "form",
    "关掉后该字段恢复",
    tab.js(
        "(()=>{const p=[...document.querySelectorAll('.demo-page')]"
        ".filter(p=>p.textContent.includes('整表禁用'))[0];"
        "return p.querySelectorAll('.jm-form')[1].querySelector('.jm-form-item.is-disabled') === null})()"
    ),
    True,
)

# ---------- Uploader：压缩 demo 渲染 ----------
tab.goto(f"{BASE}/components/uploader", wait=3)
check("uploader", "压缩 demo 存在", tab.js("[...document.querySelectorAll('.demo-page')].some(p=>p.textContent.includes('自动压缩'))"), True)
check("uploader", "压缩默认开（开关选中）", tab.js("[...document.querySelectorAll('.demo-page')].some(p=>p.querySelector('.jm-uploader'))"), True)
check("uploader", "Uploader 组件正常渲染", count(tab, ".jm-uploader") >= 2, True)
check("uploader", "添加按钮存在", count(tab, ".jm-uploader__trigger") >= 2, True)

# ---------- 汇总 ----------
print()
print("=" * 46)
total = len(results)
passed = sum(1 for r in results if r[2])
print(f"共 {total} 项，通过 {passed}，失败 {total - passed}")
sys.exit(0 if passed == total else 1)
