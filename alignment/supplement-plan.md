# Supplement Plan

What this book carries, what's taught outside it, and by what — stated plainly so the
boundary is legible rather than accidental. Built from `standards/apcsp.json` and
`standards/castandards.json`'s carrier fields after this pass's corrections.

## The division of labor

**A Python Notebook carries:**
- AP Big Idea 3 (Algorithms and Programming) almost entirely — 14 of 18 topics, and every
  topic in the 30–35%-of-the-exam weight band that this course actually reaches.
- AP Big Idea 1 (Creative Development) partially — 3 of 4 topics, with the 4th
  (Collaboration) handled outside the book (see below).
- CA's AP.12–22 strand heavily — 7 of 11 standards directly.
- AP Big Idea 2 (Data) partially — 2 of 4 topics, via chap12/chap13's text-analysis and
  file/database work. Not binary numbers, not data compression.

**Little Brother carries** (per `CLAUDE.md`'s course context, confirmed by this pass —
not a new decision, just verified against the indexes):
- AP Big Ideas 4 and 5 entirely (Computer Systems and Networks; Impact of Computing).
- CA's NI and IC strands entirely (all 4 NI standards, all 8 IC standards).
- One AP↔CA pair worth flagging: **AP 1.1 (Collaboration) and CA IC.27** cover
  overlapping ground (working with people from different backgrounds/cultures) but sit in
  different big ideas on each side, and this book's own Collaboration carrier (below) is
  not Little Brother. Don't assume IC.27 is automatically covered just because 1.1 is
  handled elsewhere — they're related, not identical (see `standards/crosswalk.json`).

**CS50T Multimedia carries:**
- AP 2.1 (Binary Numbers) and 2.2 (Data Compression).
- CA DA.8 (representing real-world data as bits) and DA.9 (storage/format tradeoffs,
  whose own worked example is image-compression quality-vs-size — the same territory as
  AP 2.2).

**The November algorithms block carries:**
- AP 3.11 (Binary Search), 3.16 (Simulations), 3.17 (Algorithmic Efficiency), 3.18
  (Undecidable Problems).
- No direct CA standard maps cleanly onto this group except a "related" (not "strong")
  link between 3.16 and CA DA.11, and between 3.17 and CA AP.14's performance clause — see
  `standards/crosswalk.json`. Don't assume the November block automatically satisfies
  those CA standards; check the crosswalk note before claiming credit.

**Lab pair work and the Create Performance Task carry:**
- AP 1.1 (Collaboration) and CA AP.21 (team roles, collaborative tools) — a strong,
  direct match, both realized the same way: continuously, not as a standalone lesson.

## What has no assigned carrier anywhere (real gaps, not yet supplemented)

These don't have a home in this book, Little Brother, CS50T Multimedia, the November
block, or lab practice. Listed here so they don't quietly stay uncovered:

- **AP CRD-2.H / CA AP.19** — crediting or licensing code taken from another source.
  Notable because chap04 and chap08 *use* borrowed libraries without ever discussing this.
- **CA AP.15** — event-driven/GUI programming. No event loop anywhere in the book.
- **CA AP.18** — designing for a broad audience using their feedback. chap04's process
  never leaves the solo/technical track.
- **CA CS.1, CS.2, CS.3** — hardware/systems abstraction and systems-level
  troubleshooting. Outside both this book's and Little Brother's remit as currently
  scoped.
- **CA DA.10** — data visualization. No charting/plotting anywhere in the book.
- **CA DA.11** — refining a computational model against real data.

None of these are large enough on their own to justify a new supplement course the way
CS50T Multimedia or the November block do — they're individual standards, not whole
strands. Whether to patch them with a short lesson, fold them into an existing
supplement, or accept the gap is a call for whoever owns the course calendar, not this
pass.

## The one coverage question that cuts across all of the above

**AP 3.8 / CA AP.14, iteration:** this book has no `while` loop anywhere — recursion
stands in for indefinite iteration throughout. This isn't a missing-carrier problem the
way the list above is (python_notebook does carry the topic), so it doesn't show up as a gap
in the carrier fields, but it's the single largest coverage risk this pass found. See
`alignment/standards_alignment.md`'s "load-bearing finding" note before assuming this
topic is fully closed.
