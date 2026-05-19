#!/usr/bin/env python3
"""
Test web_fetch support across major open-science / preprint providers.

Status codes:
  FULL_TEXT      – paper body retrieved; first conclusion sentence returned
  ABSTRACT_ONLY  – page loaded, only abstract / metadata visible
  OVERFLOW       – page loaded but response exceeded model context window
  BLOCKED        – access denied / login required / domain blocked
  ERROR          – network failure, timeout, or unexpected failure
"""

import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import anthropic

CREDENTIALS_FILE = Path.home() / ".claude" / ".credentials.json"
MODEL = "claude-haiku-4-5-20251001"
OUT_DIR = Path(__file__).parent

FETCH_TOOL = {"type": "web_fetch_20260209", "name": "web_fetch", "allowed_callers": ["direct"]}

# ── Test matrix ───────────────────────────────────────────────────────────────
# (provider, url_label, url, description)
TESTS = [
    # ── arXiv ────────────────────────────────────────────────────────────────
    ("arXiv",         "abstract page",  "https://arxiv.org/abs/1706.03762",
     "Attention Is All You Need — control: abstract only"),
    ("arXiv",         "HTML full text", "https://arxiv.org/html/1706.03762",
     "Attention Is All You Need — HTML"),
    ("arXiv",         "PDF",            "https://arxiv.org/pdf/1706.03762",
     "Attention Is All You Need — PDF"),

    # ── ar5iv (arXiv HTML mirror via LaTeXML, different CDN) ─────────────────
    ("ar5iv",         "HTML",           "https://ar5iv.labs.arxiv.org/html/1706.03762",
     "arXiv HTML mirror — same paper"),

    # ── bioRxiv — correct full-text URL uses .full suffix ────────────────────
    ("bioRxiv",       "HTML full text", "https://www.biorxiv.org/content/10.1101/2020.02.07.937862v1.full",
     "A COVID-19 preprint (SARS-CoV-2 genome)"),
    ("bioRxiv",       "PDF",            "https://www.biorxiv.org/content/10.1101/2020.02.07.937862v1.full.pdf",
     "Same preprint — PDF"),

    # ── medRxiv — same .full suffix pattern ──────────────────────────────────
    ("medRxiv",       "HTML full text", "https://www.medrxiv.org/content/10.1101/2020.04.09.20059360v1.full",
     "A COVID-19 clinical preprint"),

    # ── Other preprint servers ───────────────────────────────────────────────
    ("SSRN",          "abstract page",  "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4582612",
     "Social-science preprint"),
    ("TechRxiv",      "abstract page",  "https://www.techrxiv.org/users/684782/articles/686506",
     "IEEE preprint"),
    ("ChemRxiv",      "abstract page",  "https://chemrxiv.org/engage/chemrxiv/article-details/6444d9c8aad2a62ca1e87a7a",
     "Chemistry preprint"),
    ("PsyArXiv",      "abstract page",  "https://psyarxiv.com/9yf3a/",
     "Psychology preprint (OSF-backed)"),
    ("EarthArXiv",    "abstract page",  "https://eartharxiv.org/repository/view/4518/",
     "Earth-science preprint"),
    ("OSF Preprints", "abstract page",  "https://osf.io/preprints/socarxiv/s7gyu",
     "Social-science preprint"),
    ("PhilArchive",   "abstract page",  "https://philarchive.org/rec/ANDTPO",
     "Philosophy preprint"),
    ("PREPRINTS.org", "abstract page",  "https://www.preprints.org/manuscript/202001.0009/v1",
     "Multi-disciplinary preprint"),

    # ── Open repositories ────────────────────────────────────────────────────
    ("Internet Archive", "item page",   "https://archive.org/details/cesarano2026-ai-agents-decline-free-beer-sigbovik",
     "SIGBOVIK 2026 — item page"),
    ("Internet Archive", "PDF direct",  "https://archive.org/download/cesarano2026-ai-agents-decline-free-beer-sigbovik/FULLTEXT01.pdf",
     "SIGBOVIK 2026 — direct PDF download"),
    ("Zenodo",        "record page",    "https://zenodo.org/records/8355191",
     "A Zenodo record — note: may overflow context"),
    ("figshare",      "direct download","https://figshare.com/ndownloader/articles/25674000/versions/1",
     "figshare ndownloader direct link"),
    ("HAL",           "record page",    "https://hal.science/hal-04582397",
     "HAL Science record"),
    ("HAL",           "PDF direct",     "https://hal.science/hal-04582397/document",
     "HAL PDF direct link"),
    ("DIVA Portal",   "PDF direct",     "https://kth.diva-portal.org/smash/get/diva2:1953484/FULLTEXT01.pdf",
     "KTH DIVA — PDF direct"),
    ("CORE",          "reader page",    "https://core.ac.uk/reader/96721350",
     "CORE aggregated paper"),
    ("Europe PMC",    "article page",   "https://europepmc.org/article/PPR/PPR155699",
     "Europe PMC article"),
    ("PubMed Central","article page",   "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7386622/",
     "NIH PMC — static HTML"),

    # ── Publisher open-access ────────────────────────────────────────────────
    ("PLOS ONE",      "article page",   "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230068",
     "PLOS ONE article"),
    ("eLife",         "article page",   "https://elifesciences.org/articles/84478",
     "eLife article"),
    ("F1000Research", "article page",   "https://f1000research.com/articles/9-58",
     "F1000Research article"),
    ("PeerJ",         "article page",   "https://peerj.com/articles/13500/",
     "PeerJ article"),
    ("OpenReview",    "forum page",     "https://openreview.net/forum?id=rJ4km2R5t7",
     "ICLR submission (OpenReview)"),
    ("OpenReview",    "PDF",            "https://openreview.net/pdf?id=rJ4km2R5t7",
     "OpenReview PDF"),

    # ── IEEE Xplore ──────────────────────────────────────────────────────────
    ("IEEE Xplore",   "abstract page",  "https://ieeexplore.ieee.org/document/10845793/",
     "IEEE Access 2025 open-access paper (DOI 10.1109/ACCESS.2025.3531662)"),
    ("IEEE Xplore",   "PDF (stamp)",    "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10845793",
     "Same IEEE Access 2025 paper — stamp PDF link"),

    # ── ACM Digital Library ──────────────────────────────────────────────────
    ("ACM DL",        "abstract page",  "https://dl.acm.org/doi/10.1145/1294261.1294281",
     "Dynamo: Amazon's Highly Available Key-value Store (SOSP 2007)"),
    ("ACM DL",        "PDF",            "https://dl.acm.org/doi/pdf/10.1145/1294261.1294281",
     "Dynamo paper — ACM DL PDF link"),

    # ── Conference proceedings ───────────────────────────────────────────────
    ("ACL Anthology", "abstract page",  "https://aclanthology.org/2023.acl-long.1/",
     "ACL 2023 paper"),
    ("ACL Anthology", "PDF",            "https://aclanthology.org/2023.acl-long.1.pdf",
     "ACL 2023 PDF"),
    ("NeurIPS",       "Paper PDF",      "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
     "NeurIPS 2017 — Attention paper (full paper PDF)"),

    # ── Aggregators / discovery ──────────────────────────────────────────────
    ("Semantic Scholar", "paper page",  "https://www.semanticscholar.org/paper/Attention-is-All-you-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776",
     "Attention paper — JS-rendered"),

    # ── Author-controlled hosting ────────────────────────────────────────────
    ("GitHub Pages",  "github.io page", "https://jalammar.github.io/illustrated-transformer/",
     "Long-form technical article on GitHub Pages (github.io)"),
    ("ResearchGate",  "paper page",     "https://www.researchgate.net/publication/220365399",
     "Control: known login wall"),
]

# ── Classification ────────────────────────────────────────────────────────────

BLOCKED_RE = re.compile(
    r"blocked|access denied|access restriction|unable to access|cannot access"
    r"|not able to access|permission denied|login required|sign.?in required"
    r"|authentication required|403 forbidden|page.*unavailable|website.*unavailable"
    r"|couldn'?t access|could not access|not accessible",
    re.I,
)

def classify(raw_text: str, api_error: str | None) -> tuple[str, str]:
    """Return (status, snippet)."""
    if api_error:
        if "prompt is too long" in api_error or "tokens >" in api_error:
            return "OVERFLOW", api_error[:200]
        return "ERROR", api_error[:200]

    text = raw_text.strip()
    low  = text.lower()

    # Model self-classified
    for code in ("BLOCKED", "ABSTRACT_ONLY", "ERROR"):
        if re.search(rf"\b{code}\b", text):
            return code, text[:250]

    if BLOCKED_RE.search(low):
        return "BLOCKED", text[:250]

    if not text or len(text.split()) < 10:
        return "ERROR", text[:100] or "(empty response)"

    # Heuristic: does the response contain a substantial sentence?
    if re.search(r"[A-Z][^.!?]{40,}[.!?]", text):
        return "FULL_TEXT", text[:350]

    return "ABSTRACT_ONLY", text[:250]


def fetch_one(client: anthropic.Anthropic, url: str) -> tuple[str, str]:
    messages = [{"role": "user", "content": (
        f"Fetch this URL: {url}\n\n"
        "Determine if the full body text of an academic paper is accessible.\n"
        "• Full paper body readable → return the first sentence of the conclusion verbatim.\n"
        "• Page loads but only abstract/metadata → reply exactly: ABSTRACT_ONLY\n"
        "• Access denied / login wall / domain blocked → reply exactly: BLOCKED\n"
        "• Network or parsing error → reply exactly: ERROR"
    )}]
    for _ in range(4):
        try:
            r = client.messages.create(
                model=MODEL, max_tokens=300,
                tools=[FETCH_TOOL], messages=messages,
            )
        except anthropic.BadRequestError as e:
            msg = str(e)
            if "prompt is too long" in msg or "tokens >" in msg:
                return classify("", msg)
            return "ERROR", msg[:200]
        except Exception as e:
            return "ERROR", str(e)[:200]

        text = " ".join(b.text for b in r.content if b.type == "text").strip()
        if r.stop_reason == "end_turn":
            return classify(text, None)
        if r.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": r.content})
        else:
            return classify(text, None)
    return "ERROR", "max continuations"


ICON = {
    "FULL_TEXT":     "✅",
    "ABSTRACT_ONLY": "⚠️",
    "OVERFLOW":      "📦",
    "BLOCKED":       "🚫",
    "ERROR":         "❌",
}

STATUS_ORDER = ["FULL_TEXT", "ABSTRACT_ONLY", "OVERFLOW", "BLOCKED", "ERROR"]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    creds = json.loads(CREDENTIALS_FILE.read_text())
    token = creds.get("claudeAiOauth", {}).get("accessToken")
    if not token:
        raise SystemExit(f"No claudeAiOauth.accessToken in {CREDENTIALS_FILE}")
    client = anthropic.Anthropic(auth_token=token)

    print(f"Testing {len(TESTS)} URLs across {len({t[0] for t in TESTS})} providers\n")
    results = []

    for provider, url_label, url, description in TESTS:
        print(f"  {provider:20} {url_label:20} ", end="", flush=True)
        status, snippet = fetch_one(client, url)
        print(f"{ICON.get(status,'?')} {status}")
        results.append({
            "provider": provider, "url_label": url_label,
            "url": url, "description": description,
            "status": status, "snippet": snippet,
        })
        time.sleep(1)

    # Write outputs
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL, "tool": "web_fetch_20260209", "results": results,
    }
    (OUT_DIR / "webfetch_preprint_status.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False))

    print(f"\nWrote webfetch_preprint_status.json")
    counts = Counter(r["status"] for r in results)
    print("\nSummary:")
    for s in STATUS_ORDER:
        if s in counts:
            print(f"  {ICON[s]} {s:<15} {counts[s]:2} / {len(results)}")


if __name__ == "__main__":
    main()
