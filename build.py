#!/usr/bin/env python3
"""Build index.html from src/template.html, inlining day.md and library.md.

The inlined copies let index.html work when opened straight from disk.
When the page is served over http(s) it fetches day.md / library.md instead,
so a host can update day.md alone without rebuilding.
"""
import html
import pathlib

root = pathlib.Path(__file__).resolve().parent
template = (root / "src" / "template.html").read_text(encoding="utf-8")
blocks = "\n".join(
    f'<textarea hidden id="md-{name}">{html.escape((root / f"{name}.md").read_text(encoding="utf-8"))}</textarea>'
    for name in ("library", "day")
)
assert "<!--INLINE-MD-->" in template, "placeholder missing from src/template.html"
(root / "index.html").write_text(template.replace("<!--INLINE-MD-->", blocks, 1), encoding="utf-8")
print("Built index.html")
