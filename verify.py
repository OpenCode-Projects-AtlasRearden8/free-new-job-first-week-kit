#!/usr/bin/env python3
"""Verify the First-Week-of-Work freebie kit is complete and well-formed.

Local-only: reads files in this folder, network access never needed.
Run: python3 verify.py
"""

import html.parser
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PRINTABLES = [
    "01-first-week-checklist",
    "02-papers-keep-or-shred",
    "03-w4-direct-deposit-checklist",
    "04-benefits-deadline-tracker",
    "05-badge-photo-tips",
    "06-first-90-day-reflections",
]

ERRORS: list[str] = []


def check(cond: bool, ok: str, fail: str) -> None:
    if cond:
        print(f"  PASS  {ok}")
    else:
        ERRORS.append(fail)
        print(f"  FAIL  {fail}")


class HTMLProbe(html.parser.HTMLParser):
    """Collects structure facts about one HTML file."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "source", "track", "wbr", "textarea"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype: str = ""
        self.lang: str = ""
        self.charset_ok = False
        self.title = ""
        self.in_title = False
        self.checkboxes = 0
        self.text_inputs = 0
        self.heading_count = 0
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.external_refs: list[str] = []

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower().startswith("doctype html"):
            self.doctype = decl.strip()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        attrs_d = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = attrs_d.get("lang", "")
        if tag == "meta":
            if attrs_d.get("charset", "").lower().replace("-", "") == "utf8":
                self.charset_ok = True
        if tag == "title":
            self.in_title = True
        if tag == "input":
            if attrs_d.get("type") == "checkbox":
                self.checkboxes += 1
            elif attrs_d.get("type", "text") == "text":
                self.text_inputs += 1
        if tag.startswith("h") and tag[1:2].isdigit():
            self.heading_count += 1
        for akey in ("src", "href"):
            val = attrs_d.get(akey, "")
            if re.match(r"https?://|//", val):
                self.external_refs.append(val)
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"unexpected </{tag}> at line {self.getpos()[0]}")
            return
        open_tag, open_line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> (opened line {open_line})"
            )
    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data

    def close(self) -> None:  # called by html.parser at end
        super().close()
        if self.in_title:
            self.errors.append("unterminated <title>")
        if self.stack:
            leftover = self.stack[-1]
            self.errors.append(f"unclosed <{leftover[0]}> opened at line {leftover[1]}")
        self.title = " ".join(self.title.split())


def verify_structure() -> None:
    print("== files & layout ==")
    expected = (
        ["README.md", "LICENSE", "verify.py", "print/index.html"]
        + [f"guides/{n}.md" for n in PRINTABLES]
        + [f"print/{n}.html" for n in PRINTABLES]
    )
    for rel in expected:
        check((ROOT / rel).is_file(), f"exists: {rel}", f"missing file: {rel}")
    print("== html structure ==")
    for name in PRINTABLES + ["index"]:
        if name == "index":
            path, label = ROOT / "print/index.html", "print/index.html"
        else:
            path, label = ROOT / f"print/{name}.html", f"print/{name}.html"
        if not path.is_file():
            continue
        probe = HTMLProbe()
        probe.feed(path.read_text(encoding="utf-8"))
        probe.close()
        check(not probe.errors, f"{label}: tags balanced",
              f"{label}: {probe.errors}")
        check(probe.doctype != "", f"{label}: DOCTYPE present",
              f"{label}: missing DOCTYPE")
        check(probe.lang == "en", f"{label}: lang=en",
              f"{label}: <html lang> not 'en'")
        check(probe.charset_ok, f"{label}: charset utf-8",
              f"{label}: missing <meta charset=\"utf-8\">")
        check(probe.title != "", f"{label}: <title> present",
              f"{label}: missing <title>")
        check(not probe.external_refs, f"{label}: self-contained (no external refs)",
              f"{label}: external refs {probe.external_refs}")
        if name != "index":
            has_fields = (probe.checkboxes + probe.text_inputs) > 0
            check(has_fields, f"{label}: fillable fields present",
                  f"{label}: no fillable fields (checkbox/text)")
    print("== current count ==")
    htmls = sorted(p.name for p in (ROOT / "print").glob("0*.html"))
    guides = sorted(p.name for p in (ROOT / "guides").glob("0*.md"))
    check(len(htmls) == len(guides) == 6,
          "guides and printables stay in sync (6 each)",
          f"count mismatch: guides={guides} print={htmls}")


def verify_license() -> None:
    print("== license ==")
    lic = ROOT / "LICENSE"
    if not lic.is_file():
        check(False, "LICENSE exists", "LICENSE missing")
        return
    text = lic.read_text(encoding="utf-8")
    check("Copyright (c) 2026 Asdale Dynamics, LLC" in text,
          "LICENSE copyright line exact",
          "LICENSE copyright line wrong/exact string missing")
    check("Permission is hereby granted, free of charge" in text,
          "LICENSE is MIT", "LICENSE is not the MIT license text")


def verify_credit() -> None:
    print("== credit ==")
    check((ROOT / "README.md").is_file(), "README exists", "README missing")
    if not (ROOT / "README.md").is_file():
        return
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("Asdale Dynamics, LLC" in readme,
          "README credits Asdale Dynamics, LLC",
          "README does not credit Asdale Dynamics, LLC")
    print("== credit footer in print sheets ==")
    for name in PRINTABLES:
        path = ROOT / f"print/{name}.html"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        check("Asdale Dynamics, LLC" in text,
              f"print/{name}.html credits Asdale Dynamics, LLC",
              f"print/{name}.html missing credit")


SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style API key"),
    (r"ghp_[A-Za-z0-9]{30,}", "GitHub PAT"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"(?<![0-9])[0-9]{3}-[0-9]{2}-[0-9]{4}(?![0-9])",
     "real-format SSN (fake/example digits can still match — review before shipping)"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|org|net)\b",
     "bare email address — remove personal emails before publishing"),
]


def verify_no_secrets() -> None:
    print("== no secrets / personal data ==")
    files = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and p.name not in {"LICENSE", "verify.py"}
        and ".git" not in p.parts
    )
    found_any = False
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, text):
                found_any = True
                print(f"  FAIL  {label} in {path.relative_to(ROOT)}"
                      f" near: {text[max(0, m.start() - 30):m.end() + 30]!r}")
                ERRORS.append(f"{label} found in {path}")
    if not found_any:
        print("  PASS  no obvious API keys / tokens / SSNs / personal emails")


def main() -> int:
    verify_structure()
    verify_license()
    verify_credit()
    verify_no_secrets()
    print("")
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} problem(s)")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("OK: kit verified end-to-end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
