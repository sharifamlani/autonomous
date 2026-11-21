# C15 OpenAI (2026): Why we no longer evaluate SWE-bench Verified

- **Citation:** OpenAI. (2026, February 23). *Why SWE-bench Verified no longer measures frontier coding capabilities* (page title: "Why we no longer evaluate SWE-bench Verified"). OpenAI blog.
- **Link:** https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- **Fetched:** 2026-11-21 (page fetched twice: once through the page reader, once as raw HTML to check the numbers below; title and date checked on the page).
- **Why no PDF:** a vendor blog post; there is no PDF or arXiv version. Vendor-authored: OpenAI both created Verified (with the SWE-bench authors, 2024) and sells models scored on it.

## What it says (quoted from the page)

- Flawed tests: "We audited a 27.6% subset of the dataset that models often failed to solve and
  found that at least 59.4% of the audited problems have flawed test cases that reject functionally
  correct submissions".
- Audit method: "138 SWE-bench Verified problems that OpenAI o3 did not consistently solve over 64
  independent runs. Each case was independently reviewed by at least six experienced software
  engineers." Breakdown: 35.5% of the audited tasks have strict test cases that enforce specific
  implementation details; 18.8% have wide tests that check functionality the issue does not specify;
  5.1% are miscellaneous.
- Contamination: "it is important that they are never trained on problems and solutions they are
  evaluated on"; frontier models could "reproduce the original, human-written bug fix used as the
  ground-truth reference, known as the gold patch, or verbatim problem statement specifics for
  certain tasks, indicating that all of them have seen at least some of the problems and solutions
  during training". "Models that have seen the problems during training are more likely to succeed,
  because they have additional information needed to pass the underspecified tests."
- Recommendation: stop reporting Verified and urge other developers to do the same; "Until we have
  those, OpenAI recommends reporting results for SWE-bench Pro."
- Scores: state of the art "improving from 74.9% to 80.9% in the last 6 months".

## Limits

- The page I fetched carries no correction. However, C12 (Section 2) cites a later OpenAI post,
  "Separating signal from noise in coding evaluations", that "estimat[es] that about 30% of
  SWE-Bench Pro tasks are broken", so the Pro recommendation here should not be relied on. I did not
  fetch that later post.
- The 59.4% is of a subset chosen because models failed it, not of all 500 tasks. No data or code for
  the audit is released on the page.
