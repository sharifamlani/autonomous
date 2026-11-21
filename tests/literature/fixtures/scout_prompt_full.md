---
name: research-scout-fixture
description: Test fixture for `verify_literature.py --agent`. Carries the whole output contract.
---

You fill one literature theme. No paper enters without a fetched source.

Folder README: first line `# NN <Title>`, then the sections Role, Contents, What it establishes,
The catch.

papers.tsv columns: id, folder, first_author, year, title, venue, url, arxiv_or_doi, file, verified.

PDF file name: `<ID>_<FirstAuthor>_<Year>_<Short_Title>.pdf`.

public/_candidates/NN.tsv columns: name, url, stars, last_push, license, archived, theme, why.
