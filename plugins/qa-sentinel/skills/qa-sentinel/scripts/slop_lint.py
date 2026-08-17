#!/usr/bin/env -S uv run python
# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4"]
# ///
"""
slop-lint -- deterministic AI-slop design detector (qa-sentinel).

A STATIC/LAB pre-filter, not a verdict. It mechanically counts the AI-slop
fingerprints enumerated in qa-sentinel's failure-catalog/ai-slop-aesthetic.md and
premium-web-design's reference/ai-slop.md. It catches the mechanical tells; the
"layout grammar is generic" judgment stays with the designer lens (an LLM).

Gate rule (matches ai-slop-aesthetic.md): >= 3 distinct fingerprints == confirmed
slop -> non-zero exit. Tune with --threshold.

Honesty: works best on SELF-CONTAINED HTML/CSS (inline <style> + style attrs),
which is exactly what premium-web-design and mirror-rebuilds produce. Tailwind-
utility / React source hides the signals in class names and external files -- for
those, lint the RENDERED HTML (--url) instead of raw JSX. External <link>
stylesheets are NOT fetched; the report notes when it saw them.

Usage:
  uv run slop_lint.py page.html
  uv run slop_lint.py ./dist            # all *.html under a dir
  uv run slop_lint.py --url https://example.com
  uv run slop_lint.py page.html --json  # machine-readable
"""
from __future__ import annotations
import argparse, colorsys, json, os, re, sys, urllib.request
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    # Exit cleanly rather than re-raising: this runs from a PostToolUse hook, where a
    # traceback is noise and the one-line instruction is the whole actionable message.
    print("slop-lint needs beautifulsoup4; run via `uv run` so PEP 723 deps resolve.", file=sys.stderr)
    sys.exit(1)

UA = "Mozilla/5.0 (slop-lint; qa-sentinel)"  # browser UA -- some WAFs 403 bare python

# ---- color helpers -----------------------------------------------------------
_HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")
_RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", re.I)

def _hex_to_rgb(h: str):
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    elif len(h) in (6, 8):
        h = h[:6]
    else:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None

def _colors(css: str):
    out = []
    for m in _HEX.finditer(css):
        rgb = _hex_to_rgb(m.group(0))
        if rgb:
            out.append(rgb)
    for m in _RGB.finditer(css):
        r, g, b = (min(255, int(x)) / 255 for x in m.groups())
        out.append((r, g, b))
    return out

def _hls(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return h * 360, l, s  # hue degrees, lightness 0-1, saturation 0-1

# ---- detectors ---------------------------------------------------------------
# Each returns (fired: bool, detail: str).
EMOJI = re.compile(
    "[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF" "\U00002B00-\U00002BFF" "\U0000FE0F" "]"
)

def detect(raw: str, text: str):
    findings = []

    def add(rule, fired, detail):
        if fired:
            findings.append({"rule": rule, "detail": detail})

    n_glass = len(re.findall(r"(?i)backdrop-filter\s*:\s*[^;{}]*blur\s*\(", raw))
    add("glassmorphism-overuse", n_glass >= 2, f"{n_glass} backdrop-filter:blur() uses")

    add("gradient-text", bool(re.search(r"(?i)background-clip\s*:\s*text", raw)),
        "background-clip:text (gradient/clipped text)")

    fonts = set(m.lower() for m in re.findall(
        r"(?i)font-family\s*:\s*[^;{}]*?\b(Inter|Roboto|Arial|Open Sans)\b", raw))
    add("banned-default-font", bool(fonts), "overused font(s): " + ", ".join(sorted(fonts)))

    add("three-col-equal-grid",
        bool(re.search(r"(?i)grid-template-columns\s*:\s*(repeat\(\s*3\s*,\s*(1fr|minmax\([^)]*\)|33(\.\d+)?%)\s*\)|(1fr\s+){2}1fr|(33(\.\d+)?%\s*){3})", raw)),
        "3-column equal-fraction grid")

    big_radius = any(
        (float(v) >= 16 if u == "px" else float(v) >= 1)
        for v, u in re.findall(r"(?i)border-radius\s*:\s*(\d+(?:\.\d+)?)(px|rem)", raw))
    has_shadow = bool(re.search(r"(?i)box-shadow\s*:\s*[^;{}]*\dpx", raw))
    add("rounded-plus-shadow-cards", big_radius and has_shadow,
        "large border-radius + drop-shadow (generic card look)")

    add("pure-black-white",
        bool(re.search(r"(?i)(#000\b|#000000\b|#fff\b|#ffffff\b|rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))", raw)),
        "pure #000 / #fff (never tinted)")

    add("full-viewport-height",
        bool(re.search(r"(?i)((min-)?height\s*:\s*100vh\b|\bh-screen\b)", raw)) and "100dvh" not in raw and "min-h-[100dvh]" not in raw,
        "100vh / h-screen without dvh (iOS viewport jump)")

    # palette analysis
    cols = _colors(raw)
    accent_hues = set()
    dark_bg = False
    cyan = False
    for rgb in cols:
        hue, l, s = _hls(rgb)
        if l < 0.18:
            dark_bg = True
        if s > 0.35 and 0.2 < l < 0.85:
            accent_hues.add(int(hue // 30))  # 30-degree buckets
            if 170 <= hue <= 200:
                cyan = True
    add("multiple-accent-colors", len(accent_hues) > 1,
        f"{len(accent_hues)} distinct accent hues (pick one)")
    add("cyan-on-dark", dark_bg and cyan, "cyan accent on near-black background (classic AI palette)")

    emojis = sorted(set(EMOJI.findall(text)))
    add("emoji-in-ui", bool(emojis), "emoji in UI text: " + " ".join(emojis[:8]))

    return findings

# ---- io ----------------------------------------------------------------------
def load(src: str, is_url: bool) -> str:
    if is_url:
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (trusted, user-supplied)
            return r.read().decode("utf-8", "replace")
    return Path(src).read_text(encoding="utf-8", errors="replace")

def lint_one(name: str, raw: str):
    soup = BeautifulSoup(raw, "html.parser")
    text = soup.get_text(" ")
    findings = detect(raw, text)
    ext_links = len(soup.find_all("link", rel=lambda v: v and "stylesheet" in v))
    return {
        "target": name,
        "fingerprints": len(findings),
        "findings": findings,
        "external_stylesheets_unscanned": ext_links,
    }

def run_hook(threshold: int) -> int:
    """PostToolUse hook mode: read the tool payload from stdin, lint only a
    just-written HTML file, and print a one-line advisory when it trips the
    threshold. Always exits 0 (informational, never blocks). Silent on
    non-HTML, unreadable files, or when SLOP_LINT_HOOK_DISABLED is set."""
    if os.environ.get("SLOP_LINT_HOOK_DISABLED", "").strip().lower() in ("1", "true", "yes", "on"):
        return 0
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # no/!json stdin (e.g. async without payload) -> no-op, never error
    fp = ((payload.get("tool_input") or {}).get("file_path") or "").strip()
    if not fp.lower().endswith((".html", ".htm")):
        return 0
    try:
        raw = Path(fp).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return 0
    r = lint_one(fp, raw)
    if r["fingerprints"] >= threshold:
        rules = ", ".join(f["rule"] for f in r["findings"])
        print(f"[slop-lint] {r['fingerprints']} AI-slop fingerprint(s) in {Path(fp).name}: {rules}. "
              f"Static/lab signal -- run `uv run slop_lint.py \"{fp}\"` for detail, or /qa run for the full gate.")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic AI-slop design linter (static/lab pre-filter).")
    ap.add_argument("path", nargs="?", help="HTML file or directory")
    ap.add_argument("--url", help="fetch and lint a live page instead of a local file")
    ap.add_argument("--threshold", type=int, default=3, help="fingerprints to flag as slop (default 3)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--hook", action="store_true", help="PostToolUse hook mode: read the tool payload from stdin, lint a just-written HTML file, advise if slop (never blocks)")
    a = ap.parse_args()

    if a.hook:
        return run_hook(a.threshold)

    targets = []  # (name, raw)
    if a.url:
        targets.append((a.url, load(a.url, True)))
    elif a.path:
        p = Path(a.path)
        files = sorted(p.rglob("*.html")) if p.is_dir() else [p]
        for f in files:
            targets.append((str(f), load(str(f), False)))
    else:
        ap.error("give a file/dir path or --url")

    results = [lint_one(n, r) for n, r in targets]
    worst = max((r["fingerprints"] for r in results), default=0)
    verdict = "SLOP" if worst >= a.threshold else ("SUSPECT" if worst > 0 else "CLEAN")
    payload = {"verdict": verdict, "threshold": a.threshold, "signal": "static/lab (pre-filter, not a verdict)", "results": results}

    if a.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"slop-lint: {verdict}  (threshold {a.threshold}; static/lab signal, not a verdict)\n")
        for r in results:
            head = f"  {r['target']}: {r['fingerprints']} fingerprint(s)"
            print(head)
            for f in r["findings"]:
                print(f"    - {f['rule']}: {f['detail']}")
            if r["external_stylesheets_unscanned"]:
                print(f"    ! {r['external_stylesheets_unscanned']} external stylesheet(s) NOT scanned "
                      f"(lint the rendered page with --url for full coverage)")
            print()
        print("Next: the designer lens judges these against the goal. Fingerprints flag candidates, "
              "they do not certify taste.")
    return 1 if worst >= a.threshold else 0

if __name__ == "__main__":
    sys.exit(main())
