# Can Claude Read Papers on Preprint Servers?

## TL;DR

✅ **Claude can read arXiv, Internet Archive, PubMed Central, PLOS ONE, ACL Anthology, NeurIPS.**

❌ **IEEE, ACM, HAL, DIVA, OSF are systematically blocked. bioRxiv, medRxiv, and most publisher sites return errors.**

For hosting papers intended to be read by AI agents, **Internet Archive (direct PDF link) and arXiv are the recommended targets**.

---

## Introduction

As AI assistants and autonomous research agents become common tools in scientific workflows, a new form of accessibility gap is emerging: a paper can be legally open-access yet practically invisible to the AI tools that researchers use to discover, read, and synthesise literature. The `web_fetch` tool — which allows a Claude-powered agent(both Claude.AI and local Claude Code) to retrieve and read the content of a URL at runtime — is a direct proxy for this gap. If a paper's URL returns a 403, requires JavaScript rendering, or overflows the model's context window, the paper is effectively absent from any AI-assisted research workflow, regardless of its open-access licence.

This experiment systematically measures that gap across 30 major open-science platforms and preprint servers. For each provider, a known paper URL was fetched via the `web_fetch_20260209` API tool and the model was asked to return the first sentence of the paper's conclusion — a concrete, falsifiable test of full-text accessibility. The results reveal a striking disparity: platforms that invested in clean, static HTML or PDF serving (arXiv, PubMed Central, PLOS ONE, Internet Archive, NeurIPS) are fully accessible, while others (HAL, ResearchGate, OSF) are not.

This has direct implications for researchers who want their work to reach the widest possible audience, and for platform operators who care about their content being discoverable in the AI era.

---

**Generated:** 2026-05-17  
**Tool:** `web_fetch_20260209` with `allowed_callers: ["direct"]`  
**Model:** `claude-haiku-4-5-20251001`  
**Method:** fetch a known paper URL; ask the model to return the first conclusion sentence or self-classify the failure.

## Quick-reference table

| Provider | URL type | Status |
|----------|----------|:------:|
| **arXiv** | abstract page | ✅ `FULL_TEXT` |
| **arXiv** | HTML full text | ✅ `FULL_TEXT` |
| **arXiv** | PDF | ✅ `FULL_TEXT` |
| **ar5iv** | HTML | ✅ `FULL_TEXT` |
| **bioRxiv** | HTML full text | ❌ `ERROR` |
| **bioRxiv** | PDF | ❌ `ERROR` |
| **medRxiv** | HTML full text | ❌ `ERROR` |
| **SSRN** | abstract page | ❌ `ERROR` |
| **TechRxiv** | abstract page | ❌ `ERROR` |
| **ChemRxiv** | abstract page | ❌ `ERROR` |
| **PsyArXiv** | abstract page | ⚠️ `ABSTRACT_ONLY` |
| **EarthArXiv** | abstract page | ❌ `ERROR` |
| **OSF Preprints** | abstract page | 🚫 `BLOCKED` |
| **PhilArchive** | abstract page | ❌ `ERROR` |
| **PREPRINTS.org** | abstract page | ⚠️ `ABSTRACT_ONLY` |
| **Internet Archive** | item page | ⚠️ `ABSTRACT_ONLY` |
| **Internet Archive** | PDF direct | ✅ `FULL_TEXT` |
| **Zenodo** | record page | ⚠️ `ABSTRACT_ONLY` |
| **figshare** | direct download | ❌ `ERROR` |
| **HAL** | record page | 🚫 `BLOCKED` |
| **HAL** | PDF direct | 🚫 `BLOCKED` |
| **DIVA Portal** | PDF direct | 🚫 `BLOCKED` |
| **CORE** | reader page | ❌ `ERROR` |
| **Europe PMC** | article page | ❌ `ERROR` |
| **PubMed Central** | article page | ✅ `FULL_TEXT` |
| **PLOS ONE** | article page | ✅ `FULL_TEXT` |
| **eLife** | article page | ❌ `ERROR` |
| **F1000Research** | article page | ❌ `ERROR` |
| **PeerJ** | article page | ❌ `ERROR` |
| **OpenReview** | forum page | ❌ `ERROR` |
| **OpenReview** | PDF | ❌ `ERROR` |
| **IEEE Xplore** | abstract page | ❌ `ERROR` |
| **IEEE Xplore** | PDF (stamp) | ❌ `ERROR` |
| **ACM DL** | abstract page | ❌ `ERROR` |
| **ACM DL** | PDF | ❌ `ERROR` |
| **ACL Anthology** | abstract page | ⚠️ `ABSTRACT_ONLY` |
| **ACL Anthology** | PDF | ✅ `FULL_TEXT` |
| **NeurIPS** | Paper PDF | ✅ `FULL_TEXT` |
| **Semantic Scholar** | paper page | ⚠️ `ABSTRACT_ONLY` |
| **GitHub Pages** | github.io page | ✅ `FULL_TEXT` |
| **ResearchGate** | paper page | ❌ `ERROR` |

## Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | `FULL_TEXT` | Paper body retrieved; conclusion sentence returned |
| ⚠️ | `ABSTRACT_ONLY` | Page loaded but only abstract / metadata visible |
| 📦 | `OVERFLOW` | Page loaded but response exceeded model context window (content IS there) |
| 🚫 | `BLOCKED` | Domain blocked, access denied, or login required |
| ❌ | `ERROR` | Network failure, timeout, or unexpected failure |

## Summary counts

- ✅ **FULL_TEXT**: 10 / 41
- ⚠️ **ABSTRACT_ONLY**: 6 / 41
- 🚫 **BLOCKED**: 4 / 41
- ❌ **ERROR**: 21 / 41

## Per-provider details

### arXiv
- **abstract page**  
  `https://arxiv.org/abs/1706.03762`  
  ✅ `FULL_TEXT` — I'll fetch that URL for you. This page loads the abstract and metadata only - I can see the abstract section and bibliographic information, but not the full paper body text. Let me try to access the PDF version to check 
- **HTML full text**  
  `https://arxiv.org/html/1706.03762`  
  ✅ `FULL_TEXT` — I'll fetch that URL and check what content is accessible. The full body text of the academic paper is accessible. I can now locate and return the first sentence of the conclusion verbatim.  From Section 7 (Conclusion), t
- **PDF**  
  `https://arxiv.org/pdf/1706.03762`  
  ✅ `FULL_TEXT` — I'll fetch that URL for you. The full body text of the academic paper is accessible. This is the famous "Attention Is All You Need" paper on the Transformer architecture.  The first sentence of the conclusion is:  "In th

### ar5iv
- **HTML**  
  `https://ar5iv.labs.arxiv.org/html/1706.03762`  
  ✅ `FULL_TEXT` — I'll fetch that URL for you. The full body text of the academic paper is accessible. I can see the complete paper including all sections (Introduction, Background, Model Architecture, Results, Conclusion, etc.).  Here is

### bioRxiv
- **HTML full text**  
  `https://www.biorxiv.org/content/10.1101/2020.02.07.937862v1.full`  
  ❌ `ERROR` — I'll fetch that URL and check if the full paper body is accessible. ERROR
- **PDF**  
  `https://www.biorxiv.org/content/10.1101/2020.02.07.937862v1.full.pdf`  
  ❌ `ERROR` — I'll fetch that URL for you and check the accessibility of the paper's content. ERROR

### medRxiv
- **HTML full text**  
  `https://www.medrxiv.org/content/10.1101/2020.04.09.20059360v1.full`  
  ❌ `ERROR` — I'll fetch that URL for you and check what content is accessible. ERROR

### SSRN
- **abstract page**  
  `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4582612`  
  ❌ `ERROR` — I'll fetch that URL and check what content is accessible. ERROR

### TechRxiv
- **abstract page**  
  `https://www.techrxiv.org/users/684782/articles/686506`  
  ❌ `ERROR` — I'll fetch that URL to check the accessibility of the full paper body. ERROR

### ChemRxiv
- **abstract page**  
  `https://chemrxiv.org/engage/chemrxiv/article-details/6444d9c8aad2a62ca1e87a7a`  
  ❌ `ERROR` — I'll fetch that URL for you and check what content is accessible. ERROR

### PsyArXiv
- **abstract page**  
  `https://psyarxiv.com/9yf3a/`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL and check what content is accessible. The page loads but only minimal metadata is accessible. I cannot see the abstract or full paper body—just basic OSF framework elements. This indicates the full pa

### EarthArXiv
- **abstract page**  
  `https://eartharxiv.org/repository/view/4518/`  
  ❌ `ERROR` — I'll fetch the URL to check if the full paper is accessible. ERROR

### OSF Preprints
- **abstract page**  
  `https://osf.io/preprints/socarxiv/s7gyu`  
  🚫 `BLOCKED` — I'll fetch that URL and check what content is accessible. The page appears to load but only returns minimal metadata without the actual paper content visible. Let me try fetching the actual preprint document, which may b

### PhilArchive
- **abstract page**  
  `https://philarchive.org/rec/ANDTPO`  
  ❌ `ERROR` — I'll fetch that URL for you to check if the full paper body is accessible. ERROR

### PREPRINTS.org
- **abstract page**  
  `https://www.preprints.org/manuscript/202001.0009/v1`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL for you to check the accessibility of the full paper. Based on the fetch results, the page loads and displays the abstract and metadata, but I do not see the full body text of the paper (introduction,

### Internet Archive
- **item page**  
  `https://archive.org/details/cesarano2026-ai-agents-decline-free-beer-sigbovik`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL for you to check the accessibility of the full paper. The page loads and shows the metadata and abstract for the paper, but the actual full body text of the paper is not visible in this fetched conten
- **PDF direct**  
  `https://archive.org/download/cesarano2026-ai-agents-decline-free-beer-sigbovik/FULLTEXT01.pdf`  
  ✅ `FULL_TEXT` — I'll fetch that PDF for you and check if the full body text is accessible. The full body text of the academic paper is accessible. Here is the first sentence of the conclusion verbatim:  "We offered eleven AI agents five

### Zenodo
- **record page**  
  `https://zenodo.org/records/8355191`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL for you. The page loads but provides only the abstract and metadata. The full paper body text is not directly accessible from this record view—only the PDF file link is shown. To access the complete p

### figshare
- **direct download**  
  `https://figshare.com/ndownloader/articles/25674000/versions/1`  
  ❌ `ERROR` — I'll fetch that URL to check what content is accessible. ERROR

### HAL
- **record page**  
  `https://hal.science/hal-04582397`  
  🚫 `BLOCKED` — I'll fetch that URL for you and check what content is accessible. The page is displaying an access denied error with the message "Access Denied: error code 9e4edb5b6b850c41." This indicates the content is blocked or not 
- **PDF direct**  
  `https://hal.science/hal-04582397/document`  
  🚫 `BLOCKED` — I'll fetch the URL for you to determine what content is accessible. BLOCKED

### DIVA Portal
- **PDF direct**  
  `https://kth.diva-portal.org/smash/get/diva2:1953484/FULLTEXT01.pdf`  
  🚫 `BLOCKED` — I'll fetch that PDF URL for you. BLOCKED

### CORE
- **reader page**  
  `https://core.ac.uk/reader/96721350`  
  ❌ `ERROR` — I'll fetch the URL to check the accessibility of the full paper. ERROR

### Europe PMC
- **article page**  
  `https://europepmc.org/article/PPR/PPR155699`  
  ❌ `ERROR` — ERROR  The page requires JavaScript to function and the fetched content shows only the navigation structure without the actual article content. The page cannot be properly parsed to determine if the full body text or onl

### PubMed Central
- **article page**  
  `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7386622/`  
  ✅ `FULL_TEXT` — I'll fetch that URL and check what content is accessible. The full body text of the academic paper is accessible. Here is the first sentence of the conclusion verbatim:  "This review systematically collated pertinent lit

### PLOS ONE
- **article page**  
  `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230068`  
  ✅ `FULL_TEXT` — I'll fetch that URL and check what content is accessible. Based on the fetched content, I can see that the full body text of the academic paper is accessible. The page contains the complete paper including the Introducti

### eLife
- **article page**  
  `https://elifesciences.org/articles/84478`  
  ❌ `ERROR` — I'll fetch that URL for you to check what content is accessible. ERROR

### F1000Research
- **article page**  
  `https://f1000research.com/articles/9-58`  
  ❌ `ERROR` — I'll fetch that URL for you and check what content is accessible. ERROR

### PeerJ
- **article page**  
  `https://peerj.com/articles/13500/`  
  ❌ `ERROR` — I'll fetch that URL for you to check if the full body text is accessible. ERROR

### OpenReview
- **forum page**  
  `https://openreview.net/forum?id=rJ4km2R5t7`  
  ❌ `ERROR` — I'll fetch that URL and check what content is accessible. ERROR
- **PDF**  
  `https://openreview.net/pdf?id=rJ4km2R5t7`  
  ❌ `ERROR` — I'll fetch that URL for you. ERROR

### IEEE Xplore
- **abstract page**  
  `https://ieeexplore.ieee.org/document/10845793/`  
  ❌ `ERROR` — IEEE Access 2025 open-access paper (DOI 10.1109/ACCESS.2025.3531662). ieeexplore.ieee.org blocks all automated fetches (HTTP 418) regardless of open-access status.
- **PDF (stamp)**  
  `https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10845793`  
  ❌ `ERROR`

### ACM DL
- **abstract page**  
  `https://dl.acm.org/doi/10.1145/1294261.1294281`  
  ❌ `ERROR` — Dynamo: Amazon's Highly Available Key-value Store (SOSP 2007).
- **PDF**  
  `https://dl.acm.org/doi/pdf/10.1145/1294261.1294281`  
  ❌ `ERROR`

### ACL Anthology
- **abstract page**  
  `https://aclanthology.org/2023.acl-long.1/`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL and check what content is accessible. The page loaded with abstract and metadata, but the full paper body text is not accessible from the HTML landing page. The fetched content shows only the abstract
- **PDF**  
  `https://aclanthology.org/2023.acl-long.1.pdf`  
  ✅ `FULL_TEXT` — I'll fetch that URL for you to check the accessibility of the full paper. Perfect! The full paper body text is accessible. The paper is a complete academic paper with introduction, background, methodology, experiments, r

### NeurIPS
- **Paper PDF**  
  `https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf`  
  ✅ `FULL_TEXT` — I'll fetch that URL to check the accessibility of the academic paper. The full body text of the academic paper is accessible. This is "Attention Is All You Need," the famous Transformer paper. Here is the first sentence 

### Semantic Scholar
- **paper page**  
  `https://www.semanticscholar.org/paper/Attention-is-All-you-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776`  
  ⚠️ `ABSTRACT_ONLY` — I'll fetch that URL for you and check what content is accessible. Based on the fetched content, this page shows the Semantic Scholar landing page for the "Attention is All you Need" paper. It displays metadata, abstract 

### GitHub Pages
- **github.io page**  
  `https://jalammar.github.io/illustrated-transformer/`  
  ✅ `FULL_TEXT` — The full body text of the article is accessible. First sentence of the final section ("Go Forth And Transform"): "I hope you've found this a useful place to start to break the ice with the major concepts of the Transformer."

### ResearchGate
- **paper page**  
  `https://www.researchgate.net/publication/220365399`  
  ❌ `ERROR` — I'll fetch that URL for you to determine what content is accessible. ERROR

## Reproducing this experiment

The test script is `test_webfetch_providers.py`. It uses the Anthropic API via a claude.ai OAuth token (read from `~/.claude/.credentials.json`).

**What it does:** for each URL in the `TESTS` list, it calls the `web_fetch_20260209` tool and asks the model to return the first sentence of the conclusion, or self-classify the failure as `BLOCKED`, `ABSTRACT_ONLY`, or `ERROR`. Results are written to `webfetch_preprint_status.json`.

**Requirements:**

```
pip install anthropic
```

A valid claude.ai session token must be present in `~/.claude/.credentials.json` (populated automatically by Claude Code).

**Run:**

```bash
python3 test_webfetch_providers.py
```

**To add a provider**, append a tuple to the `TESTS` list:

```python
("Provider Name", "url label", "https://example.com/paper", "description")
```
