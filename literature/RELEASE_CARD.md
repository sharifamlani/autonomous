# Release card: *Verification, Not Capability* (review article, November 2026)

**What it is.** A review article in the style of the *Annual Review of Political Science*:
*Verification, Not Capability: What the Evidence Says About Autonomous Agents That Build Software and
Do Research*, by Sharif Amlani. PDF: [`literature/LITERATURE_REVIEW.pdf`](LITERATURE_REVIEW.pdf). LaTeX
source: [`literature/review/`](review/).

**The argument in one sentence.** Agents succeed where an external signal they cannot edit decides
success, and fail, often silently, where they grade their own work. AI for software engineering and
automated science fail in the same ways and are fixed by the same structures.

**What it covers.** 286 distinct papers and reports and 237 open-source repositories were surveyed.
The article cites 162 papers and 28 repositories across nine themes, in 16 sections, with 4 tables and
2 figures.

**How it was checked** (numbers from `literature/qa/PHASE8_SCORECARD.md` and
`literature/qa/LITERATURE_REVIEW_qa.md`):
- **Evidence file** ([`LITERATURE_REVIEW_EVIDENCE.md`](LITERATURE_REVIEW_EVIDENCE.md)): 1,048 entries,
  one per claim or citation, each with a verbatim quote and its exact location. 757 quotes were found
  verbatim on the stated PDF page by script; 291 (web pages, GitHub issues, repo files) were checked by
  hand. 0 failing.
- **QA:** five QA passes by agents that did not write the paper found 135 issues (11 blockers). All
  were fixed, and a separate re-checker confirmed every fix against its source.
- **Independent evaluator** (did none of the work): 7/7 pre-registered criteria PASS, including 20 of 20
  randomly drawn numbers matching their sources and 20 of 20 evidence spot checks.
  - The length criterion was raised from 9,000–11,000 to 9,000–15,500 words by the author after the
    grade. The body is 15,043 words.
- **Disclosure:** AI agents (Claude, via Claude Code) drafted the paper under the author's direction.
  The author is building the open-source project discussed in §14.

**Safe-to-post facts** (each is in the paper and the evidence file; phrase each as that study's finding):
the five numbers in the abstract, and any number in Summary Points 1–10, stated with its source and
sample as the paper states it.

**Release:** posting only on Sharif's express go, with the post text and video approved by him in
Marketing's session (Sharif 2026-11-21).
