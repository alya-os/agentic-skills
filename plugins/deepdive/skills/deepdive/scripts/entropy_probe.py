#!/usr/bin/env python3
"""Compression-based entropy profiler for source files.

Usage: python3 entropy_probe.py <source_file> [--sections 20] [--output json|text] [--save <path>]
"""
# Entropy profiling adapted from avilum/minrlm, MIT License,
# Copyright (c) 2026 Avi Lumelsky. Source: https://github.com/avilum/minrlm
# Full licence text in NOTICE.md at the repository root.

from __future__ import annotations
import argparse, json, sys, zlib
from pathlib import Path

_MICRO_CHUNK = 500
_MIN_CONTEXT = 2000


def compute_entropy_profile(text: str, num_sections: int = 20) -> dict | None:
    """Return structured entropy profile, or None if text is too short."""
    if not text or len(text) < _MIN_CONTEXT:
        return None
    micro = _MICRO_CHUNK
    n_micros = len(text) // micro
    if n_micros < num_sections:
        micro = max(len(text) // num_sections, 100)
        n_micros = len(text) // micro
    if n_micros < 2:
        return None

    # Phase 1: micro-chunk compression ratios
    micro_ratios: list[float] = []
    for i in range(n_micros):
        raw = text[i * micro : (i + 1) * micro].encode("utf-8", errors="replace")
        compressed = zlib.compress(raw, level=1)
        micro_ratios.append(len(compressed) / max(len(raw), 1))

    # Phase 2: aggregate into macro-sections
    per_sec = max(n_micros // num_sections, 1)
    sections: list[dict] = []
    for s in range(num_sections):
        mi_start = s * per_sec
        mi_end = mi_start + per_sec if s < num_sections - 1 else n_micros
        seg = micro_ratios[mi_start:mi_end]
        if not seg:
            continue
        char_start, char_end = mi_start * micro, min(mi_end * micro, len(text))
        mx, md = round(max(seg), 3), round(sorted(seg)[len(seg) // 2], 3)
        max_micro_pos = (mi_start + seg.index(max(seg))) * micro
        sections.append({"start": char_start, "end": char_end, "max_ratio": mx,
                         "median_ratio": md, "_mpos": max_micro_pos})
    if not sections:
        return None

    max_vals = [sec["max_ratio"] for sec in sections]
    overall_median = sorted(max_vals)[len(max_vals) // 2]
    overall_mean = sum(max_vals) / len(max_vals)
    std_dev = round((sum((v - overall_mean) ** 2 for v in max_vals) / len(max_vals)) ** 0.5, 4)
    spike_thr = round(
        max(overall_median + 1.5 * std_dev, overall_median * 1.3)
        if std_dev > 0.01 else overall_median * 1.3, 4)

    spike_indices: list[int] = []
    for idx, sec in enumerate(sections):
        is_spike = sec["max_ratio"] >= spike_thr and std_dev > 0.01
        sec["is_spike"] = is_spike
        if is_spike:
            spike_indices.append(idx)
            sec["excerpt"] = text[sec["_mpos"] : sec["_mpos"] + 100]
    for sec in sections:
        sec.pop("_mpos", None)

    return {"sections": sections, "spike_threshold": spike_thr,
            "overall_median": round(overall_median, 4), "std_dev": std_dev,
            "spikes": spike_indices}


def compute_context_preview(text: str, head: int = 400, mid: int = 300, tail: int = 500) -> dict | None:
    """Return head/mid/tail preview dict, or None if text is too short."""
    if not text or len(text) < 500:
        return None
    m_start = len(text) // 2 - mid // 2
    return {"head": text[:head], "mid": text[m_start : m_start + mid], "tail": text[-tail:]}


def format_text_output(file_path: str, result: dict) -> str:
    """Format result dict as human-readable text (minrlm style)."""
    emap = result["entropy_map"]
    sections = emap["sections"]
    lines: list[str] = []

    # Section size label
    sec_chars = (sections[0]["end"] - sections[0]["start"]) if sections else 0
    if sec_chars >= 1_000_000:
        sz = f"{sec_chars / 1_000_000:.1f}M"
    elif sec_chars >= 1_000:
        sz = f"{sec_chars // 1_000}K"
    else:
        sz = str(sec_chars) if sec_chars else "?"

    lines.append(f"Entropy map ({len(sections)} sections x ~{sz} chars, "
                 f"higher=unique lower=repetitive):")
    tags = []
    for sec in sections:
        tag = f"{sec['max_ratio']:.2f}"
        if sec.get("is_spike"):
            tag += "\u2191"
        tags.append(tag)
    lines.append("  [" + ", ".join(tags) + "]")

    spike_indices = emap["spikes"]
    if spike_indices:
        labels = [f"sec {i} ({sections[i]['start']}:{sections[i]['end']})" for i in spike_indices]
        lines.append(f"  Spikes (distinctive content): {'; '.join(labels)}")
        for idx in spike_indices:
            excerpt = sections[idx].get("excerpt", "")
            if excerpt:
                lines.append(f"  sec {idx}: ...{excerpt.replace(chr(10), chr(92) + 'n')}...")
    elif emap["std_dev"] < 0.01:
        lines.append("  Uniform - content is consistent throughout")

    lines.append("")
    lines.append(f"File: {file_path}")
    lines.append(f"Size: {result['chars']} chars, {result['lines']} lines")
    lines.append(f"Stats: median={emap['overall_median']}, std_dev={emap['std_dev']}, "
                 f"spike_threshold={emap['spike_threshold']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Compression-based entropy profiler.")
    ap.add_argument("source_file", help="Path to the file to profile")
    ap.add_argument("--sections", type=int, default=20, help="Number of sections (default: 20)")
    ap.add_argument("--output", choices=["json", "text"], default="text", help="Output format")
    ap.add_argument("--save", default=None, help="Write JSON results to this path")
    args = ap.parse_args()

    src = Path(args.source_file)
    if not src.exists():
        sys.stderr.write(f"Error: file not found: {src}\n")
        return 1
    try:
        text = src.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        sys.stderr.write(f"Error reading file: {exc}\n")
        return 1

    entropy = compute_entropy_profile(text, num_sections=args.sections)
    preview = compute_context_preview(text)
    empty_map = {"sections": [], "spike_threshold": 0, "overall_median": 0, "std_dev": 0, "spikes": []}
    result: dict = {
        "file": str(src),
        "chars": len(text),
        "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
        "entropy_map": entropy or empty_map,
        "preview": preview or {"head": "", "mid": "", "tail": ""},
    }

    if args.output == "json":
        out = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        out = format_text_output(str(src), result)
    print(out)

    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        sys.stderr.write(f"Saved to: {save_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
