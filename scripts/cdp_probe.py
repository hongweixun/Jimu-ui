"""轻量 CDP 探针：打开页面 → 等待渲染 → 执行若干表达式 → 打印结果。"""
import json
import subprocess
import sys
import time
import urllib.request

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def ensure_edge(port=9222):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2)
        return
    except Exception:
        pass
    subprocess.Popen(
        [
            EDGE,
            "--headless=new",
            f"--remote-debugging-port={port}",
            "--user-data-dir=C:\\Windows\\Temp\\edge-cdp-probe",
            "--window-size=1400,900",
            "--hide-scrollbars",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
            return
        except Exception:
            continue
    raise RuntimeError("Edge 未能启动")


class Tab:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, max_size=20 * 1024 * 1024)
        self.id = 0
        self.send("Page.enable")
        self.send("Runtime.enable")

    def send(self, method, params=None):
        self.id += 1
        msg = {"id": self.id, "method": method, "params": params or {}}
        self.ws.send(json.dumps(msg))
        while True:
            data = json.loads(self.ws.recv())
            if data.get("id") == self.id:
                return data

    def goto(self, url, wait=2.5):
        self.send("Page.navigate", {"url": url})
        time.sleep(wait)

    def js(self, expr):
        r = self.send(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": True},
        )
        res = r.get("result", {})
        if "exceptionDetails" in res:
            return {"__error__": res["exceptionDetails"].get("text"), "detail": str(res["exceptionDetails"])[:400]}
        return res.get("result", {}).get("value")

    def shot(self, path):
        r = self.send("Page.captureScreenshot", {"format": "png"})
        data = r.get("result", {}).get("data")
        if data:
            import base64

            open(path, "wb").write(base64.b64decode(data))
            return path
        return None


def new_tab(port=9222):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
    r = urllib.request.urlopen(req, timeout=5)
    return Tab(json.loads(r.read())["webSocketDebuggerUrl"])
