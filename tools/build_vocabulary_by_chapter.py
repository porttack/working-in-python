#!/usr/bin/env python3
"""Annotate vocabulary-by-chapter.md/.html with AP tags and cross-chapter footnotes.

Parses the existing alignment/vocabulary-by-chapter.md (term/definition text
is the source of truth and is preserved verbatim -- this script only adds
presentation metadata, it never rewrites a definition) and regenerates both
files with:

- an AP superscript badge on every term that also appears on the AP CSP exam's
  vocabulary list (from build_vocabulary_glossary.py's ENTRIES table -- the
  same table used for ap-vocabulary-glossary.{md,html}, so the two pages can't
  disagree about which terms are AP-tested)
- a footnote linking to any OTHER chapter where the same term is also defined
  (e.g. "attribute" in ch. 9 gets a note pointing to ch. 14, and vice versa),
  skipped where the existing hand-written note already covers the same ground
  (anything already mentioning "chapter")
- the same "AP-tested only" filter toggle as ap-vocabulary-glossary.html

No PDF and no print-specific column layout for this page -- unlike the merged
A-Z glossary, printing this one isn't a priority (per maintainer, 2026-08-18).

Regenerate with: python3 tools/build_vocabulary_by_chapter.py (or `make vocab-by-chapter`)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_vocabulary_glossary as glossary  # noqa: E402

MD_PATH = ROOT / "alignment" / "vocabulary-by-chapter.md"
HTML_PATH = ROOT / "alignment" / "vocabulary-by-chapter.html"
SITE = glossary.SITE

BANNER_MD = (
    "<!-- Term/definition text is hand-authored and preserved verbatim across regeneration. -->\n"
    "<!-- AP badges and cross-chapter footnotes below are generated. -->\n"
    "<!-- Regenerate with: python3 tools/build_vocabulary_by_chapter.py (or `make vocab-by-chapter`) -->\n\n"
)


def esc(s):
    return html.escape(s, quote=False)


def parse_existing():
    """Returns (preamble_lines, sections). Each section is a dict:
    {kind: "chapter"|"interlude", number: "1".."18" or None, anchor: "ch01".."ch18b",
     title: subtitle after the em dash, intro_lines: [str, ...], terms: [(term, definition), ...]}
    """
    text = MD_PATH.read_text()
    lines = text.split("\n")

    heading_re = re.compile(r"^## (Chapter (\d+)|Interlude) — (.+)$")
    # Matches both the original 2-column table ("| **term** | definition |")
    # and this script's own 3-column output ("| **term** | AP | definition |"),
    # so re-running against previously-generated output is safe.
    row_re = re.compile(r"^\| \*\*(.+?)\*\* \| (?:(?:AP)? \| )?(.+) \|$")
    auto_note_re = re.compile(r"\s*\*\(Also ch\. [^)]*\)\*\s*$")

    # Strip any banner comment lines this script itself added on a prior run.
    while lines and lines[0].startswith("<!--"):
        lines.pop(0)
    while lines and lines[0] == "":
        lines.pop(0)

    preamble = []
    i = 0
    while i < len(lines) and not lines[i].startswith("## "):
        preamble.append(lines[i])
        i += 1

    sections = []
    interlude_count = 0
    while i < len(lines):
        m = heading_re.match(lines[i])
        if not m:
            i += 1
            continue
        kind = "chapter" if m.group(2) else "interlude"
        number = m.group(2)
        title = m.group(3)
        if kind == "chapter":
            anchor = "ch" + number.zfill(2)
            label = number.zfill(2)
        else:
            interlude_count += 1
            label = "06b" if interlude_count == 1 else "07b"
            anchor = "ch" + label
        i += 1
        intro_lines = []
        while i < len(lines) and not lines[i].startswith("| Term"):
            if lines[i].strip():
                intro_lines.append(lines[i])
            i += 1
        # skip "| Term | Definition |" and the "|---|---|" separator
        i += 2
        terms = []
        while i < len(lines) and lines[i].startswith("|"):
            rm = row_re.match(lines[i])
            if rm:
                definition = auto_note_re.sub("", rm.group(2))
                terms.append((rm.group(1), definition))
            i += 1
        sections.append({
            "kind": kind, "number": number, "label": label, "anchor": anchor,
            "title": title, "intro_lines": intro_lines, "terms": terms,
        })
    return preamble, sections


def build_lookup_tables(sections):
    ap_by_term = {term.lower(): ap for term, ap, _def, _note in glossary.ENTRIES}
    chapters_by_term = {}
    for sec in sections:
        for term, _definition in sec["terms"]:
            chapters_by_term.setdefault(term.lower(), []).append(sec["label"])
    return ap_by_term, chapters_by_term


def other_chapters(term, current_label, chapters_by_term):
    return [c for c in chapters_by_term.get(term.lower(), []) if c != current_label]


def chapter_note_text(others):
    if not others:
        return None
    labels = [f"ch. {c.lstrip('0') or c}" for c in others]
    if len(labels) == 1:
        return f"Also {labels[0]}."
    return f"Also {', '.join(labels[:-1])} and {labels[-1]}."


def write_markdown(preamble, sections, ap_by_term, chapters_by_term):
    out = [BANNER_MD.rstrip("\n"), ""]
    out.extend(preamble)
    for sec in sections:
        heading = f"Chapter {sec['number']}" if sec["kind"] == "chapter" else "Interlude"
        out.append(f"## {heading} — {sec['title']}")
        out.append("")
        out.extend(sec["intro_lines"])
        if sec["intro_lines"]:
            out.append("")
        out.append("| Term | AP | Definition |")
        out.append("|---|---|---|")
        for term, definition in sec["terms"]:
            ap_mark = "AP" if ap_by_term.get(term.lower(), False) else ""
            others = other_chapters(term, sec["label"], chapters_by_term)
            note = chapter_note_text(others)
            d = definition
            if note and "chapter" not in definition.lower():
                d += f" *({note})*"
            out.append(f"| **{term}** | {ap_mark} | {d} |")
        out.append("")
    MD_PATH.write_text("\n".join(out))


def md_inline_to_html(text):
    """Minimal Markdown inline rendering for definition cells: code spans,
    bold, italics. These files only ever use these three, verified against
    the current source (no links, no images inside definitions)."""
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


def build_html(preamble, sections, ap_by_term, chapters_by_term):
    total_terms = sum(len(sec["terms"]) for sec in sections)
    ap_count = sum(
        1 for sec in sections for term, _d in sec["terms"] if ap_by_term.get(term.lower(), False)
    )

    nav_links = []
    section_html = []
    for sec in sections:
        chapter_ap_count = sum(1 for term, _d in sec["terms"] if ap_by_term.get(term.lower(), False))
        nav_links.append(
            f'<a href="#{sec["anchor"]}" data-ap-count="{chapter_ap_count}">{sec["label"].lstrip("0") or sec["label"]}</a>'
        )
        heading_link_text = f"Chapter {sec['number']}" if sec["kind"] == "chapter" else "Interlude"
        chap_url = f"{SITE}/chap{sec['label']}.html"
        rows = []
        for term, definition in sec["terms"]:
            ap = ap_by_term.get(term.lower(), False)
            others = other_chapters(term, sec["label"], chapters_by_term)
            note = chapter_note_text(others)
            sup = '<sup class="ap">AP</sup>' if ap else ""
            def_html = md_inline_to_html(definition)
            if note and "chapter" not in definition.lower():
                if len(others) == 1:
                    link = f'<a href="#ch{others[0]}">ch. {others[0].lstrip("0") or others[0]}</a>'
                    note_html = f"Also {link}."
                else:
                    links = [f'<a href="#ch{c}">ch. {c.lstrip("0") or c}</a>' for c in others]
                    note_html = f"Also {', '.join(links[:-1])} and {links[-1]}."
                def_html += f' <i class="note">({note_html})</i>'
            rows.append(
                f'<tr class="{"is-ap" if ap else ""}"><td class="code">{esc(term)}{sup}</td><td>{def_html}</td></tr>'
            )
        section_html.append(f"""
<section id="{sec['anchor']}" data-ap-count="{chapter_ap_count}">
  <div class="bigidea-head">
    <h2><a href="{chap_url}">{heading_link_text}</a> &mdash; {esc(sec['title'])}</h2>
    <span class="name" data-total="{len(sec['terms'])}" data-ap="{chapter_ap_count}">{len(sec['terms'])} term{'s' if len(sec['terms']) != 1 else ''}</span>
  </div>
  <div class="tablewrap">
    <table>
      <thead><tr><th style="width:220px">Term</th><th>Definition</th></tr></thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</section>""")

    n_chapters = sum(1 for s in sections if s["kind"] == "chapter")
    n_interludes = sum(1 for s in sections if s["kind"] == "interlude")

    doc = f"""<title>Vocabulary by Chapter — Working in Python</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{glossary.SHARED_TOKENS_CSS}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--paper); color: var(--ink); font-family: var(--sans);
  font-size: 15.5px; line-height: 1.55; -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--accent-ink); text-decoration: none; border-bottom: 1px solid currentColor; opacity: 0.9; }}
a:hover {{ opacity: 1; }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}

.page {{ max-width: 920px; margin: 0 auto; padding: 0 24px 96px; }}

header.masthead {{ padding: 40px 0 28px; border-bottom: 1px solid var(--line); }}
.eyebrow {{
  display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap;
  font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.09em; text-transform: uppercase;
  color: var(--ink-soft); margin: 0 0 14px;
}}
.eyebrow a {{ border-bottom: 1px dotted currentColor; text-transform: none; letter-spacing: 0.02em; }}
h1 {{
  font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 4.2vw, 38px);
  line-height: 1.12; margin: 0 0 12px; text-wrap: balance; color: var(--ink);
}}
.lede {{ margin: 0; max-width: 62ch; color: var(--ink-soft); font-size: 16px; }}
.lede code {{ font-family: var(--mono); font-size: 0.92em; background: var(--line-soft); padding: 0.1em 0.35em; border-radius: 4px; }}

.stats {{
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line);
  border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin-top: 28px;
}}
.stat {{ background: var(--paper-raised); padding: 16px 18px; }}
.stat .n {{ font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 26px; font-weight: 600; line-height: 1; }}
.stat .label {{ margin-top: 6px; font-size: 12.5px; color: var(--ink-soft); }}
.stat.book .n {{ color: var(--strong); }}
.stat.planned .n {{ color: var(--partial); }}
.stat.elsewhere .n {{ color: var(--elsewhere); }}

nav.jump {{
  position: sticky; top: 0; z-index: 10; background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(6px); border-bottom: 1px solid var(--line); margin: 0 -24px 40px; padding: 0 24px;
}}
.jump-inner {{
  max-width: 920px; margin: 0 auto; display: flex; gap: 4px; overflow-x: auto; padding: 10px 0;
  scrollbar-width: none;
}}
.jump-inner::-webkit-scrollbar {{ display: none; }}
.jump a {{
  border-bottom: none; font-size: 13px; font-weight: 500; color: var(--ink-soft); padding: 6px 11px;
  border-radius: 999px; white-space: nowrap; flex-shrink: 0;
}}
.jump a:hover {{ color: var(--ink); background: var(--line-soft); }}
.jump a.external {{ margin-left: auto; color: var(--accent-ink); }}

section {{ margin: 48px 0; }}
section > .bigidea-head h2 {{
  font-family: var(--serif); font-size: 23px; font-weight: 600; margin: 0 0 6px; color: var(--ink); scroll-margin-top: 60px;
}}
.bigidea-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 6px; }}
.bigidea-head .name {{ font-size: 13.5px; color: var(--ink-soft); }}

.tablewrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; margin-bottom: 8px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13.8px; background: var(--paper-raised); }}
th, td {{ padding: 10px 14px; text-align: left; vertical-align: top; }}
thead th {{
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--ink-soft); border-bottom: 1px solid var(--line); font-weight: 600; white-space: nowrap;
}}
tbody tr + tr td {{ border-top: 1px solid var(--line-soft); }}
td.code {{ font-family: var(--mono); font-weight: 600; white-space: nowrap; }}

sup.ap {{
  font-family: var(--mono); font-size: 9.5px; font-weight: 700; letter-spacing: 0.02em;
  color: var(--accent-ink); background: var(--accent-soft); border-radius: 3px; padding: 0 3px;
  vertical-align: super; margin-left: 3px;
}}
i.note {{ color: var(--ink-soft); font-style: italic; }}
i.note a {{ color: var(--ink-soft); border-bottom: 1px dotted currentColor; }}
i.note a:hover {{ color: var(--accent-ink); }}

.legend2 {{ display: flex; gap: 18px; flex-wrap: wrap; font-size: 13px; color: var(--ink-soft); margin: 14px 0 0; }}

.filterbar {{
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  margin-top: 18px; padding: 12px 16px; background: var(--paper-raised);
  border: 1px solid var(--line); border-radius: 10px;
}}
.filter-label {{ font-size: 13.5px; font-weight: 600; color: var(--ink); }}
.segmented {{ display: inline-flex; background: var(--line-soft); border-radius: 999px; padding: 3px; gap: 2px; }}
.seg-btn {{
  font-family: var(--sans); font-size: 13px; font-weight: 500; color: var(--ink-soft);
  background: transparent; border: none; border-radius: 999px; padding: 7px 14px; cursor: pointer;
}}
.seg-btn:hover {{ color: var(--ink); }}
.seg-btn[aria-pressed="true"] {{ background: var(--accent); color: var(--paper); }}
.filter-count {{ font-size: 12.5px; color: var(--ink-soft); font-family: var(--mono); margin-left: auto; }}
body.ap-only tr:not(.is-ap) {{ display: none; }}

footer {{ margin-top: 64px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 12.5px; color: var(--ink-soft); }}
footer code {{ font-family: var(--mono); background: var(--line-soft); padding: 0.1em 0.35em; border-radius: 4px; }}

@media print {{ nav.jump, .filterbar {{ display: none; }} }}
</style>

<div class="page">

<header class="masthead">
  <p class="eyebrow">
    <span>Working in Python &middot; Book Vocabulary</span>
    <a href="{SITE}/alignment/ap-vocabulary-coverage.html">&#8618; AP CSP Vocabulary Coverage</a>
    <a href="{SITE}/alignment/ap-vocabulary-glossary.html">&#8618; A-Z Glossary (merged)</a>
  </p>
  <h1>Vocabulary by Chapter</h1>
  <p class="lede">Every term from Downey's own chapter-ending <code>Glossary</code> sections, chapters 1&ndash;18, plus any interludes' own glossaries, in reading order. This is the book's own vocabulary, exactly as written &mdash; not a paraphrase, not a standards crosswalk.</p>
  <div class="stats">
    <div class="stat book">
      <div class="n">{total_terms}</div>
      <div class="label">glossary terms, chapters 1&ndash;18 + {n_interludes} interludes</div>
    </div>
    <div class="stat planned">
      <div class="n">{n_chapters}</div>
      <div class="label">chapters with a Glossary section (plus {n_interludes} interludes)</div>
    </div>
    <div class="stat elsewhere">
      <div class="n">{ap_count}</div>
      <div class="label">on the AP CSP exam's own vocabulary list</div>
    </div>
  </div>
  <p class="legend2">
    <span><sup class="ap">AP</sup> on the AP CSP exam's vocabulary list</span>
    <span><i>(Also ch. N.)</i> also defined in another chapter &mdash; link jumps there</span>
  </p>
  <div class="filterbar">
    <span class="filter-label">Studying for the exam?</span>
    <div class="segmented" role="group" aria-label="Vocabulary filter">
      <button type="button" class="seg-btn" data-filter="all" aria-pressed="true">All {total_terms} terms</button>
      <button type="button" class="seg-btn" data-filter="ap" aria-pressed="false">AP-tested only &middot; {ap_count}</button>
    </div>
    <span class="filter-count" id="filterCount"></span>
  </div>
</header>

<nav class="jump">
  <div class="jump-inner">
    {''.join(nav_links)}
    <a class="external" href="{SITE}/alignment/ap-vocabulary-coverage.html">AP CSP coverage &#8599;</a>
  </div>
</nav>

{''.join(section_html)}

<footer>
  Full definitions and provenance in the repo-local twin of this page. Cross-links: the
  <code>alignment/glossary-map.md</code> (concept-level crosswalk, Pass 3, repo-only),
  the <a href="{SITE}/alignment/ap-practices-bigideas-coverage.html">AP CSP Coverage Map</a>
  (topic-level), and the <a href="{SITE}/alignment/apcsp-standards-reference.html">AP CSP Standards Reference</a>.
</footer>

</div>

<script>
(function() {{
  var STORAGE_KEY = "apVocabFilterMode";
  var AP_TOTAL = {ap_count};
  var ALL_TOTAL = {total_terms};
  var buttons = document.querySelectorAll(".seg-btn");
  var countEl = document.getElementById("filterCount");

  function applyMode(mode) {{
    document.body.classList.toggle("ap-only", mode === "ap");
    for (var i = 0; i < buttons.length; i++) {{
      var b = buttons[i];
      b.setAttribute("aria-pressed", b.getAttribute("data-filter") === mode ? "true" : "false");
    }}
    var sections = document.querySelectorAll("section[data-ap-count]");
    for (var j = 0; j < sections.length; j++) {{
      var sec = sections[j];
      var apCount = parseInt(sec.getAttribute("data-ap-count"), 10) || 0;
      sec.style.display = (mode === "ap" && apCount === 0) ? "none" : "";
      var nameEl = sec.querySelector(".name");
      if (nameEl) {{
        var total = nameEl.getAttribute("data-total");
        var apHere = nameEl.getAttribute("data-ap");
        nameEl.textContent = mode === "ap"
          ? (apHere + (apHere === "1" ? " AP term" : " AP terms"))
          : (total + (total === "1" ? " term" : " terms"));
      }}
    }}
    var jumpLinks = document.querySelectorAll(".jump a[data-ap-count]");
    for (var k = 0; k < jumpLinks.length; k++) {{
      var a = jumpLinks[k];
      var apLinkCount = parseInt(a.getAttribute("data-ap-count"), 10) || 0;
      a.style.display = (mode === "ap" && apLinkCount === 0) ? "none" : "";
    }}
    if (countEl) {{
      countEl.textContent = mode === "ap" ? ("showing " + AP_TOTAL + " AP-tested terms") : ("showing all " + ALL_TOTAL + " terms");
    }}
    try {{ localStorage.setItem(STORAGE_KEY, mode); }} catch (e) {{}}
  }}

  for (var m = 0; m < buttons.length; m++) {{
    buttons[m].addEventListener("click", function(ev) {{ applyMode(ev.currentTarget.getAttribute("data-filter")); }});
  }}

  var saved = "all";
  try {{ saved = localStorage.getItem(STORAGE_KEY) || "all"; }} catch (e) {{}}
  applyMode(saved);
}})();
</script>
"""
    HTML_PATH.write_text(doc)


def main():
    preamble, sections = parse_existing()
    ap_by_term, chapters_by_term = build_lookup_tables(sections)
    total_terms = sum(len(sec["terms"]) for sec in sections)
    ap_count = sum(
        1 for sec in sections for term, _d in sec["terms"] if ap_by_term.get(term.lower(), False)
    )
    print(f"sections={len(sections)} total_terms={total_terms} ap={ap_count}")

    write_markdown(preamble, sections, ap_by_term, chapters_by_term)
    build_html(preamble, sections, ap_by_term, chapters_by_term)
    print(f"wrote {MD_PATH.relative_to(ROOT)}")
    print(f"wrote {HTML_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
