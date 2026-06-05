#!/usr/bin/env python3
"""Authoring-ONLY tool: probe the Echo Brain corpus (DCPS + DCPDS + DoD FMR Vol 8)
and draft a citation-grounded civpay_qa.csv.

This runs on the Tower lab (needs Ollama nomic-embed-text @ :11434 and Qdrant @ :6333).
Its OUTPUT — data/civpay_qa.csv — is what ships to SharePoint. NOTHING at runtime in
the O365 environment depends on this script.

Usage:
    generate_qa_from_probe.py [seed-questions.yaml] [out.csv]
"""
import csv
import re
import sys

EMBED_URL = "http://localhost:11434/api/embed"
QDRANT_URL = "http://localhost:6333/collections/echo_memory/points/search"
SYSTEM_BY_TAG = {"dcps": "DCPS", "dcpds": "DCPDS", "fmr_vol8": "FMR Vol 8"}


def fmt_citation(filename: str) -> str:
    """Turn a corpus filename into a human-readable official citation."""
    fn = filename.replace(".pdf", "")
    fn = re.sub(r"^FMR_Vol08_08_(\w+)", r"DoD FMR Vol 8 Ch \1", fn)
    fn = re.sub(r"^DCPS_(DBSpec|IFSpec|UM)_(?:26_1_)?(?:DCPS_[A-Za-z_]*?)?", r"DCPS \1: ", fn)
    fn = re.sub(r"_+", " ", fn)
    fn = re.sub(r"\bp(\d+)-(\d+)\b", r"p\1-\2", fn)
    return fn.strip()[:200]


def to_row(q, hit, system, roles):
    """Pure: build a draft CSV row from one probe hit. Testable without network."""
    p = hit.get("payload", {})
    passage = re.sub(r"\s+", " ", (p.get("text") or "")).strip()
    # Draft answer = first 2 sentences of the cited passage; a human distills it in
    # the authoring pass. The Citation is the binding artifact.
    answer = " ".join(re.split(r"(?<=[.!?]) ", passage)[:2])[:600]
    return {
        "Question": q,
        "Answer": answer,
        "Citation": fmt_citation(p.get("filename", "?")),
        "System": system,
        "Role": ";".join(roles),
        "Keywords": "",
        "LastReviewed": "2026-06-05",
        "_score": round(hit.get("score", 0), 3),
    }


def _embed(text):
    import httpx
    r = httpx.post(EMBED_URL, json={"model": "nomic-embed-text", "input": text}, timeout=20.0)
    r.raise_for_status()
    d = r.json()
    return d.get("embeddings", [d.get("embedding")])[0]


def _probe(q, tag, top_n=1):
    import httpx
    body = {
        "vector": _embed(q),
        "limit": top_n,
        "with_payload": True,
        "filter": {"must": [{"key": "source_tag", "match": {"value": tag}}]},
    }
    r = httpx.post(QDRANT_URL, json=body, timeout=15.0)
    r.raise_for_status()
    return r.json().get("result", [])


def main(seed_path, out_csv):
    import yaml
    seeds = yaml.safe_load(open(seed_path))
    rows = []
    for area in seeds:
        for item in area["questions"]:
            best = None
            for tag in item["tags"]:
                hits = _probe(item["q"], tag)
                if hits and (best is None or hits[0]["score"] > best[0]["score"]):
                    best = (hits[0], tag)
            if best:
                rows.append(to_row(item["q"], best[0], SYSTEM_BY_TAG.get(best[1], best[1]), item["roles"]))
    cols = ["Question", "Answer", "Citation", "System", "Role", "Keywords", "LastReviewed", "_score"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} draft rows -> {out_csv}")


if __name__ == "__main__":
    main(
        sys.argv[1] if len(sys.argv) > 1 else "../data/seed-questions.yaml",
        sys.argv[2] if len(sys.argv) > 2 else "../data/civpay_qa.csv",
    )
