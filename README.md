# Can AI Agents Read Scientific Papers?

## TL;DR

Open access is not the same as agent-readable.

- Both **Claude** and **Codex** reliably read `arXiv` HTML/PDF, `PubMed Central`, `PLOS ONE`, `ACL Anthology` PDFs, `NeurIPS` PDFs, and plain `GitHub Pages`.
- **Codex** additionally succeeded on `DIVA Portal`, `F1000Research`, and `OpenReview` PDFs.
- **Claude** succeeded on the direct `Internet Archive` PDF that **Codex** currently fails to fetch.
- The main failure modes are not copyright or paywalls. They are bot protection, JavaScript-heavy delivery, and fetch/runtime incompatibilities.

For authors who want the broadest agent accessibility today, **arXiv HTML/PDF remains the safest target**. `PubMed Central`, `PLOS ONE`, `ACL Anthology` PDF, and `NeurIPS` PDF are also strong.

## Scope

This repo contains **agent-readable paper accessibility measurements** across multiple AI agents using the same URL matrix and the same status taxonomy.

The question is simple:

> Given a URL to a paper or paper landing page, can an AI agent fetch enough content to read the actual paper body and recover the first sentence of the conclusion?

If the answer is no because of 403s, anti-bot middleware, JS-only rendering, or tool failures, that paper is effectively missing from many agent-assisted research workflows.

## Method

We test 41 URLs across 30 major preprint servers, repositories, publisher sites, conference proceedings, and discovery platforms.

Status codes:

- `FULL_TEXT` — paper body retrieved
- `ABSTRACT_ONLY` — landing page loaded, but only abstract/metadata visible
- `OVERFLOW` — content loaded, but exceeded the model/tool context window
- `BLOCKED` — access denied, anti-bot gate, login wall, or equivalent fetch restriction
- `ERROR` — fetch/runtime failure that did not cleanly expose paper content

### Claude dataset

- Date: `2026-05-19`
- Tool: `web_fetch_20260209`
- Model: `claude-haiku-4-5-20251001`
- Harness: [`test_webfetch_providers.py`](/home/martin/workspace/prototypes/webfetch-papers/test_webfetch_providers.py)
- Raw data: [`webfetch_preprint_status.json`](/home/martin/workspace/prototypes/webfetch-papers/webfetch_preprint_status.json)

### Codex dataset

- Date: `2026-06-27`
- Tool: Codex built-in web access
- Model surface: GPT-5 Codex in this session
- Method: same URL matrix, manually classified from direct Codex fetch results
- Raw data: [`codex_web_status.json`](/home/martin/workspace/prototypes/webfetch-papers/codex_web_status.json)

## Summary Counts

| Agent | FULL_TEXT | ABSTRACT_ONLY | OVERFLOW | BLOCKED | ERROR | Total |
|------|----------:|--------------:|---------:|--------:|------:|------:|
| Claude | 8 | 7 | 1 | 3 | 22 | 41 |
| Codex | 11 | 7 | 0 | 17 | 6 | 41 |

Interpretation:

- **Claude** is more likely to collapse hostile or incompatible sites into `ERROR`.
- **Codex** exposes hard access restrictions more clearly as `BLOCKED`.
- Both agents agree on the most robust hosts: `arXiv`, `PMC`, `PLOS ONE`, `ACL PDF`, `NeurIPS PDF`.

## Headline Findings

### Strong targets for agent-readable hosting

- `arXiv` HTML and PDF
- `PubMed Central`
- `PLOS ONE`
- `ACL Anthology` PDF
- `NeurIPS` PDF
- static long-form pages such as `github.io`

### Mixed or agent-specific

- `Internet Archive`: Claude reads the direct PDF; Codex currently errors on the same direct PDF but can read the item page metadata.
- `OpenReview`: Codex reads the PDF, but Claude returned `ERROR` for both the forum page and PDF in this dataset.
- `F1000Research`: Claude returned `ERROR`; Codex reached full text.
- `DIVA Portal`: Claude was `BLOCKED`; Codex read the PDF.

### Consistently hostile or fragile

- `bioRxiv`, `medRxiv`, `SSRN`, `TechRxiv`, `ChemRxiv`
- `HAL`, `IEEE Xplore`, `ACM DL`
- `OSF`-backed and JS/anti-bot-heavy properties such as `PsyArXiv`, `Semantic Scholar`

## Per-URL Comparison

| Provider | URL type | Claude | Codex |
|----------|----------|:------:|:-----:|
| arXiv | abstract page | ⚠️ `ABSTRACT_ONLY` | ⚠️ `ABSTRACT_ONLY` |
| arXiv | HTML full text | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| arXiv | PDF | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| ar5iv | HTML | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| bioRxiv | HTML full text | ❌ `ERROR` | 🚫 `BLOCKED` |
| bioRxiv | PDF | ❌ `ERROR` | 🚫 `BLOCKED` |
| medRxiv | HTML full text | ❌ `ERROR` | 🚫 `BLOCKED` |
| SSRN | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| TechRxiv | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| ChemRxiv | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| PsyArXiv | abstract page | ⚠️ `ABSTRACT_ONLY` | 🚫 `BLOCKED` |
| EarthArXiv | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| OSF Preprints | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| PhilArchive | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| PREPRINTS.org | abstract page | ⚠️ `ABSTRACT_ONLY` | ⚠️ `ABSTRACT_ONLY` |
| Internet Archive | item page | ⚠️ `ABSTRACT_ONLY` | ⚠️ `ABSTRACT_ONLY` |
| Internet Archive | PDF direct | ✅ `FULL_TEXT` | ❌ `ERROR` |
| Zenodo | record page | 📦 `OVERFLOW` | ⚠️ `ABSTRACT_ONLY` |
| figshare | direct download | ❌ `ERROR` | ❌ `ERROR` |
| HAL | record page | 🚫 `BLOCKED` | 🚫 `BLOCKED` |
| HAL | PDF direct | 🚫 `BLOCKED` | 🚫 `BLOCKED` |
| DIVA Portal | PDF direct | 🚫 `BLOCKED` | ✅ `FULL_TEXT` |
| CORE | reader page | ❌ `ERROR` | ❌ `ERROR` |
| Europe PMC | article page | ❌ `ERROR` | ❌ `ERROR` |
| PubMed Central | article page | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| PLOS ONE | article page | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| eLife | article page | ❌ `ERROR` | ❌ `ERROR` |
| F1000Research | article page | ❌ `ERROR` | ✅ `FULL_TEXT` |
| PeerJ | article page | ❌ `ERROR` | ❌ `ERROR` |
| OpenReview | forum page | ❌ `ERROR` | ⚠️ `ABSTRACT_ONLY` |
| OpenReview | PDF | ❌ `ERROR` | ✅ `FULL_TEXT` |
| IEEE Xplore | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| IEEE Xplore | PDF (stamp) | ❌ `ERROR` | 🚫 `BLOCKED` |
| ACM DL | abstract page | ❌ `ERROR` | 🚫 `BLOCKED` |
| ACM DL | PDF | ❌ `ERROR` | 🚫 `BLOCKED` |
| ACL Anthology | abstract page | ⚠️ `ABSTRACT_ONLY` | ⚠️ `ABSTRACT_ONLY` |
| ACL Anthology | PDF | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| NeurIPS | Paper PDF | ✅ `FULL_TEXT` | ✅ `FULL_TEXT` |
| Semantic Scholar | paper page | ⚠️ `ABSTRACT_ONLY` | 🚫 `BLOCKED` |
| GitHub Pages | github.io page | ⚠️ `ABSTRACT_ONLY` | ✅ `FULL_TEXT` |
| ResearchGate | paper page | ❌ `ERROR` | ⚠️ `ABSTRACT_ONLY` |

## Notes On Interpretation

- These results are **agent-surface specific**, not universal truths about the domains.
- A site can be legally open access and still be practically unreadable to agents.
- `BLOCKED` and `ERROR` are both failures from a user point of view; the distinction matters because `BLOCKED` usually implies deliberate infrastructure friction rather than incidental parsing/runtime failure.
- The `GitHub Pages` row is a useful control: generic static pages are very easy for agents to read even when they are not formal paper hosts.

## Reproducing The Claude Experiment

The Claude harness is the script [`test_webfetch_providers.py`](/home/martin/workspace/prototypes/webfetch-papers/test_webfetch_providers.py). It reads a Claude session token from `~/.claude/.credentials.json`, calls `web_fetch_20260209` for each URL in `TESTS`, and writes results to [`webfetch_preprint_status.json`](/home/martin/workspace/prototypes/webfetch-papers/webfetch_preprint_status.json).

Requirements:

```bash
pip install anthropic
```

Run:

```bash
python3 test_webfetch_providers.py
```

## Reproducing The Codex Dataset

There is no repo-local automation for Codex in this version of the project. The Codex dataset was recorded by opening the same URLs through Codex web access and classifying the result into the same taxonomy.

If you want this repo to support scripted Codex/OpenAI reruns, the next step is to add a second harness that uses the OpenAI Responses API plus whatever web access surface is available for the target environment, then emit a normalized combined JSON file for both agents.
