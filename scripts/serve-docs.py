#!/usr/bin/env python3
"""Build the docs, then review them exactly like GitHub Pages will serve them.

GitHub Pages publishes this project repo at a sub-path:

    https://<user>.github.io/ai-journey/            → repo root
    https://<user>.github.io/ai-journey/docs/…      → the built site

This server mirrors that: it mounts the repo root under a base path (default
`/ai-journey`) so every *relative* link / image resolves the same locally as in
production. Opening `/` or `/ai-journey/` redirects to the hub.

Usage:

    python3 scripts/serve-docs.py                 # build + serve + open browser
    python3 scripts/serve-docs.py --port 9000
    python3 scripts/serve-docs.py --no-build      # serve existing docs/
    python3 scripts/serve-docs.py --no-open
    python3 scripts/serve-docs.py --base /ai-journey  # change sub-path
"""

from __future__ import annotations

import argparse
import functools
import http.server
import importlib.util
import socketserver
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_build() -> None:
    """Execute scripts/build-docs.py:main() in-process."""
    spec = importlib.util.spec_from_file_location("build_docs", ROOT / "scripts" / "build-docs.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


def make_handler(base: str):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

        def _hub(self) -> str:
            return f"{base}/docs/index.html"

        def translate_path(self, path: str) -> str:
            # strip the base sub-path so /ai-journey/docs/x → /docs/x under ROOT
            clean = path.split("?", 1)[0].split("#", 1)[0]
            if clean == base or clean.startswith(base + "/"):
                path = path[len(base):] or "/"
            return super().translate_path(path)

        def do_GET(self) -> None:
            clean = self.path.split("?", 1)[0]
            if clean in ("/", base, base + "/"):
                self.send_response(302)
                self.send_header("Location", self._hub())
                self.end_headers()
                return
            super().do_GET()

        def log_message(self, fmt, *args):  # quieter, keep errors
            if args and str(args[0]).startswith(("4", "5")):
                super().log_message(fmt, *args)

    return Handler


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    ap = argparse.ArgumentParser(description="Build + review the AI Journey docs under a GitHub-Pages-like sub-path.")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--base", default="/ai-journey", help="sub-path to mount under (default /ai-journey)")
    ap.add_argument("--no-build", dest="build", action="store_false", help="skip rebuild, serve existing docs/")
    ap.add_argument("--no-open", dest="open", action="store_false", help="don't auto-open the browser")
    args = ap.parse_args()

    base = "/" + args.base.strip("/")

    if args.build:
        run_build()

    handler = make_handler(base)
    port = args.port
    for _ in range(20):
        try:
            httpd = Server(("127.0.0.1", port), handler)
            break
        except OSError:
            port += 1
    else:
        raise SystemExit("No free port found")

    url = f"http://127.0.0.1:{port}{base}/docs/index.html"
    print(f"\nReview → {url}")
    print(f"  (mirrors https://<user>.github.io{base}/docs/… — relative links resolve like prod)")
    print("  Ctrl+C to stop.\n")

    if args.open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
