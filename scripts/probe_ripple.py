#!/usr/bin/env python3
"""水波纹真机时序复现探针：量化「有时有波纹、有时只有 :active 变色」的成因。

模拟真机触摸（Input.dispatchTouchEvent → 浏览器合成 pointerdown/up）：
  1. 极快轻点（10ms 内松手）—— 24ms 延迟窗口内被取消
  2. 正常轻点（60ms 松手）
  3. 轻点带手指抖动（按下后漂移 10px）
  4. 明显滑动（30px，应判为滚动不画波纹）
"""
import json
import sys
import time

sys.path.insert(0, r"E:\jimu-ui\scripts")
from cdp_probe import ensure_edge, new_tab  # noqa: E402

ensure_edge()
tab = new_tab()

tab.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
tab.send("Emulation.setDeviceMetricsOverride", {"width": 420, "height": 860, "deviceScaleFactor": 2, "mobile": True})
tab.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})

passed = 0
failed = []


def check(group, name, got, want):
    global passed
    ok = got == want
    if ok:
        passed += 1
        print(f"  PASS {group}/{name}")
    else:
        failed.append(f"{group}/{name}")
        print(f"  FAIL {group}/{name}: got {got!r}, want {want!r}")


tab.goto("http://localhost:5173/components/button", wait=10)

# 在页面里装一个波纹插入计数器（波纹 320ms 后就移除，靠轮询会漏，必须监听 DOM 插入）
tab.js(
    """(()=>{
      window.__ripple = 0;
      window.__tapCount = 0;
      new MutationObserver(ms=>{
        for (const m of ms) for (const n of m.addedNodes) {
          if (n.nodeType===1 && n.classList && n.classList.contains('jm-ripple')) window.__ripple++;
        }
      }).observe(document.body, {childList:true, subtree:true});
      document.addEventListener('click', ()=>{ window.__tapCount++ }, true);
      return 'ok';
    })()"""
)

# 找一个实心主色按钮，滚到视口中央
box = json.loads(
    tab.js(
        """(()=>{
          const b=[...document.querySelectorAll('.jm-button')].find(x=>x.classList.contains('jm-button--solid') && !x.classList.contains('jm-button--default') && !x.disabled);
          if(!b) return JSON.stringify(null);
          b.scrollIntoView({block:'center'});
          const r=b.getBoundingClientRect();
          return JSON.stringify({x:r.left+r.width/2, y:r.top+r.height/2, w:r.width, h:r.height});
        })()"""
    )
)
print("    [btn]", box)
assert box, "no button found"
bx, by = box["x"], box["y"]


def reset():
    tab.js("window.__ripple=0; window.__tapCount=0")


def stats():
    return json.loads(tab.js("JSON.stringify({r:window.__ripple, t:window.__tapCount})"))


def touch_tap(delay_ms, drift_px=0, drift_steps=2):
    """真机式触摸：按下 →（可选漂移）→ 停留 delay → 抬起"""
    tab.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": bx, "y": by}]})
    if drift_px:
        for i in range(1, drift_steps + 1):
            tab.send(
                "Input.dispatchTouchEvent",
                {
                    "type": "touchMove",
                    "touchPoints": [{"x": bx + drift_px * i / drift_steps, "y": by}],
                },
            )
            time.sleep(0.012)
    if delay_ms:
        time.sleep(delay_ms / 1000.0)
    tab.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.5)


# ---------- 场景 ----------
print("== 1. 极快轻点（10ms）==")
reset()
touch_tap(10)
s = stats()
print("    ", s)
check("ripple", "fast tap draws ripple", s["r"] >= 1, True)
check("ripple", "fast tap still fires click", s["t"] >= 1, True)

print("== 2. 正常轻点（60ms）==")
reset()
touch_tap(60)
s = stats()
print("    ", s)
check("ripple", "normal tap draws ripple", s["r"] >= 1, True)

print("== 3. 轻点带抖动（漂移 10px）==")
reset()
touch_tap(40, drift_px=10)
s = stats()
print("    ", s)
check("ripple", "tap with 10px jitter draws ripple", s["r"] >= 1, True)
check("ripple", "tap with jitter still fires click", s["t"] >= 1, True)

print("== 4. 明显滑动（30px，应视为滚动）==")
reset()
touch_tap(30, drift_px=30, drift_steps=4)
s = stats()
print("    ", s)
check("ripple", "swipe does not leave ripple", s["r"] <= 1, True)

# ---------- 结论输出 ----------
print(f"\n==== {passed} passed, {len(failed)} failed ====")
if failed:
    print("failed:", failed)
