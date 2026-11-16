"""第七批组件（Notify/Popover/Segmented/Fab/BackTop/CheckTag/Pagination）与
Dialog before-close / Switch before-change 的交互回归。"""
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


def pointer(sel, tab, ev="pointerdown"):
    tab.js(
        f"(()=>{{const e=document.querySelector({json.dumps(sel)});"
        f"if(e) e.dispatchEvent(new PointerEvent({json.dumps(ev)}, {{bubbles:true, pointerId:1}}))}})()"
    )


def text_of(tab, sel, index=0):
    return tab.js(f"document.querySelectorAll({json.dumps(sel)})[{index}]?.textContent?.trim()")


def click_by_text(tab, sel, keyword):
    tab.js(
        f"[...document.querySelectorAll({json.dumps(sel)})]"
        f".find(e=>e.textContent.trim() === {json.dumps(keyword)})"
        f"?.dispatchEvent(new MouseEvent('click', {{bubbles:true}}))"
    )


def count(tab, sel):
    return tab.js(f"document.querySelectorAll({json.dumps(sel)}).length")


ensure_edge()
tab = new_tab()

# ---------- Notify ----------
tab.goto(f"{BASE}/components/notify", wait=3)
check("notify", "函数式挂载点存在", tab.js("!!document.querySelector('.notify-stage')"), True)
click_by_text(tab, ".demo-page .jm-button", "普通通知")
time.sleep(0.4)
check("notify", "点普通通知弹出 primary 通知", count(tab, ".jm-notify--primary"), 1)
check("notify", "通知文案透传", "课程提醒" in str(text_of(tab, ".jm-notify--primary")), True)
click_by_text(tab, ".demo-page .jm-button", "全部关闭")
time.sleep(0.5)
check("notify", "关闭全部后清空", count(tab, ".jm-notify-host .jm-notify"), 0)
click_by_text(tab, ".demo-page .jm-button", "连续两条堆叠")
time.sleep(0.4)
check("notify", "堆叠两条", count(tab, ".jm-notify-host .jm-notify"), 2)
click_by_text(tab, ".demo-page .jm-button", "全部关闭")
time.sleep(0.5)
check("notify", "关闭全部后清空（二）", count(tab, ".jm-notify-host .jm-notify"), 0)
click_by_text(tab, ".demo-page .jm-button", "显示顶部通知")
time.sleep(0.4)
check("notify", "组件式通知出现", count(tab, ".jm-notify.is-inline"), 1)

# ---------- Popover ----------
tab.goto(f"{BASE}/components/popover", wait=3)
click(tab, ".jm-popover__reference", 0)
time.sleep(0.35)
check("popover", "点触发器展开深色气泡", count(tab, ".jm-popover__panel.is-dark"), 1)
check("popover", "气泡文案", "深色气泡" in str(text_of(tab, ".jm-popover__panel")), True)
pointer("body", tab)
time.sleep(0.35)
check("popover", "点外部收起", count(tab, ".jm-popover__panel"), 0)
click_by_text(tab, ".jm-popover__reference .jm-button", "更多操作")
time.sleep(0.35)
check("popover", "菜单展开", count(tab, ".jm-popover__panel .menu__item"), 3)
click_by_text(tab, ".menu__item", "编辑")
time.sleep(0.35)
check("popover", "点菜单项后关闭", count(tab, ".jm-popover__panel"), 0)
check("popover", "菜单项回调生效", "编辑" in str(text_of(tab, ".demo-page")), True)

# ---------- Segmented ----------
tab.goto(f"{BASE}/components/segmented", wait=3)
check("segmented", "四组共 16 段", count(tab, ".jm-segmented__item"), 16)
click(tab, ".jm-segmented .jm-segmented__item", 1)
time.sleep(0.35)
check("segmented", "选中态切换", text_of(tab, ".jm-segmented .jm-segmented__item.is-active"), "进行中")
check(
    "segmented",
    "滑块位移到第二段",
    tab.js(
        "(()=>{const t=getComputedStyle(document.querySelector('.jm-segmented__indicator')).transform;"
        "return t==='none'?0:Math.round(new DOMMatrix(t).m41)>0})()"
    ),
    True,
)
check("segmented", "禁用整组不响应", tab.js("!!document.querySelector('.jm-segmented.is-disabled')"), True)

# ---------- Fab ----------
tab.goto(f"{BASE}/components/fab", wait=3)
check("fab", "三个悬浮按钮", count(tab, ".jm-fab"), 3)
check("fab", "inline 定位生效", tab.js("document.querySelector('.jm-fab').classList.contains('is-inline')"), True)
click(tab, ".jm-fab", 0)
time.sleep(0.4)
check("fab", "点击抛出 toast", "新建" in str(tab.js("document.querySelector('.jm-toast')?.textContent")), True)
click(tab, ".jm-fab", 2)
time.sleep(0.5)
check("fab", "激活态切换图标", tab.js("document.querySelectorAll('.jm-fab')[2].classList.contains('is-active')"), True)

# ---------- BackTop ----------
tab.goto(f"{BASE}/components/back-top", wait=3)
check("back-top", "初始不显示", count(tab, ".jm-backtop"), 0)
tab.js(
    "(()=>{const s=document.querySelectorAll('.scroll-demo__body')[0];s.scrollTop=180;"
    "s.dispatchEvent(new Event('scroll',{bubbles:false}));})()"
)
time.sleep(0.4)
check("back-top", "滚动后出现", count(tab, ".jm-backtop"), 1)
click(tab, ".jm-backtop", 0)
time.sleep(0.6)
check("back-top", "点击回顶", tab.js("document.querySelectorAll('.scroll-demo__body')[0].scrollTop"), 0)

# ---------- CheckTag ----------
tab.goto(f"{BASE}/components/check-tag", wait=3)
check("check-tag", "八个科目", tab.js("document.querySelectorAll('.tags')[0].children.length"), 8)
check("check-tag", "默认选中两个", tab.js("document.querySelectorAll('.tags')[0].querySelectorAll('.is-checked').length"), 2)
click_by_text(tab, ".tags .jm-checktag", "语文")
time.sleep(0.3)
check("check-tag", "点选新增", tab.js("document.querySelectorAll('.tags')[0].querySelectorAll('.is-checked').length"), 3)
click_by_text(tab, ".tags .jm-checktag", "一年级")
time.sleep(0.3)
check(
    "check-tag",
    "单选互斥",
    tab.js(
        "(()=>{const g=document.querySelectorAll('.tags')[1];"
        "const on=[...g.querySelectorAll('.is-checked')];return [on.length,on[0]?.textContent.trim()]})()"
    ),
    [1, "一年级"],
)

# ---------- Pagination ----------
tab.goto(f"{BASE}/components/pagination", wait=3)
check(
    "pagination",
    "10 页折叠成 5 个页码",
    tab.js(
        "document.querySelectorAll('.jm-pagination')[0].querySelectorAll('.jm-pagination__page').length"
    ),
    5,
)
check(
    "pagination",
    "省略号可点",
    tab.js(
        "document.querySelectorAll('.jm-pagination')[1].querySelectorAll('.jm-pagination__more').length"
    ),
    2,
)
click(tab, ".jm-pagination__page", 2)
time.sleep(0.3)
check("pagination", "切页生效", text_of(tab, ".jm-pagination__page.is-active"), "3")
click(tab, ".jm-pagination__next", 1)
time.sleep(0.3)
check(
    "pagination",
    "下一页",
    tab.js(
        "document.querySelectorAll('.jm-pagination')[1].querySelector('.jm-pagination__page.is-active')?.textContent.trim()"
    ),
    "7",
)
check("pagination", "简单模式页数", "10" in str(text_of(tab, ".jm-pagination__summary")), True)

# ---------- Dialog before-close ----------
tab.goto(f"{BASE}/components/dialog", wait=3)
click_by_text(tab, ".demo-page .jm-button", "提交作业")
time.sleep(0.5)
check("dialog", "弹窗打开", count(tab, ".jm-dialog"), 1)
click(tab, ".jm-dialog__button--primary", 0)
time.sleep(0.25)
check("dialog", "before-close 期间按钮转圈", count(tab, ".jm-dialog__spinner"), 1)
time.sleep(1.1)
check("dialog", "放行后关闭", count(tab, ".jm-dialog"), 0)
check(
    "dialog",
    "上一次结果已回写",
    tab.js(
        "[...document.querySelectorAll('.demo-page')]"
        ".find(d=>d.textContent.includes('上一次结果'))?.textContent.includes('已提交')"
    ),
    True,
)

# ---------- Switch before-change ----------
tab.goto(f"{BASE}/components/switch", wait=3)
SW = "[...document.querySelectorAll('.jm-switch')].find(s=>s.parentElement.textContent.includes('会员免广告'))"
check("switch", "before-change 场景开关存在", tab.js(f"!!({SW})"), True)
tab.js(f"({SW})?.dispatchEvent(new MouseEvent('click',{{bubbles:true}}))")
time.sleep(0.3)
check("switch", "异步期间转圈", tab.js(f"!!({SW})?.querySelector('.jm-switch__loading')"), True)
time.sleep(1.0)
check("switch", "放行后打开", tab.js(f"({SW})?.classList.contains('is-checked')"), True)

print("\n" + "=" * 46)
failed = [r for r in results if not r[2]]
print(f"共 {len(results)} 项，通过 {len(results) - len(failed)}，失败 {len(failed)}")
for r in failed:
    print("  FAIL:", r[0], r[1], r[3], "!=", r[4])
sys.exit(1 if failed else 0)
