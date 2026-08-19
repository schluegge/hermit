# AI Trend Research — GitHub repositories created since 2025

Snapshot date: **2026-08-19 (Europe/Berlin)**

## Scope

This inventory researches public GitHub repositories that satisfy both hard filters:

- repository creation date: `2025-01-01..2026-08-19`
- current GitHub stars: `>1000` (strictly more than 1000)

The phrase **"has a relation to AI"** is not a canonical GitHub field. To avoid subjective guessing, inclusion is evidence-based: a repository must be returned by at least one explicitly AI-related GitHub topic query listed below. GitHub topics are repository-maintainer metadata, so they provide a reproducible inclusion rule.

This is therefore an **exhaustive snapshot of the queried explicit-AI-topic universe**, not a claim that GitHub provides an exhaustive semantic definition of every repository that could conceivably be AI-related.

## Discovery / classification topics

Primary AI categories:

- `ai`
- `artificial-intelligence`
- `machine-learning`
- `deep-learning`
- `generative-ai`
- `llm`
- `ai-agents`
- `rag`
- `mcp`
- `model-context-protocol`
- `natural-language-processing`
- `computer-vision`

Every category uses the same hard qualifiers:

```text
created:2025-01-01..2026-08-19 stars:>1000
```

## Exhaustion gates verified

A category is marked exhausted only after requesting the first page that returns zero repositories.

| Topic | Result pages | First empty page | Gate |
|---|---:|---:|---|
| `ai` | 1–7 | 8 | PASS |
| `llm` | 1–6 | 7 | PASS |
| `artificial-intelligence` | 1 | 2 | PASS |
| `generative-ai` | 1 | 2 | PASS |
| `machine-learning` | 1 | 2 | PASS |
| `deep-learning` | 1 | 2 | PASS |
| `ai-agents` | 1–4 | 5 | PASS |
| `rag` | 1–2 | 3 | PASS |
| `mcp` | 1–5 | 6 | PASS |
| `model-context-protocol` | 1 | 2 | PASS |
| `natural-language-processing` | 1 | 2 | PASS |
| `computer-vision` | 1 | 2 | PASS |

## Evidence format

Repository links are stored under `trend-research/categories/`. Large categories are split into page files mirroring GitHub Search pagination. A repository may legitimately appear in more than one category because GitHub repositories may have several relevant topics.

Every stored repository link uses the canonical form:

```text
https://github.com/OWNER/REPOSITORY
```

The hard star/date filters are enforced by the GitHub repository-search query, not inferred from names.

## Branch-name note

The requested literal branch name `Trend Research` was rejected by GitHub with HTTP 422 because a Git ref cannot contain a space. The research is therefore stored on the syntactically normalized branch **`Trend-Research`**.

## Known boundary

No repository is included solely because its owner/name contains strings such as `AI`, `GPT`, or `agent`; an initial broad keyword test produced false positives. Explicit topic evidence is required. This deliberately trades speculative recall for reproducibility and no-guessing classification.
