# AI Trend Research — GitHub repositories created since 2025

Snapshot date: **2026-08-19 (Europe/Berlin)**

## Scope

This inventory researches public GitHub repositories that satisfy both hard filters:

- repository creation date: `2025-01-01..2026-08-19`
- current GitHub stars: `>1000` (strictly more than 1000)

The phrase **"has a relation to AI"** is not a canonical GitHub field. To avoid subjective guessing, inclusion is evidence-based: a repository must be returned by at least one explicitly AI-related GitHub topic query listed below. GitHub topics are repository-maintainer metadata, so this provides a reproducible inclusion rule.

This is therefore an **exhaustive snapshot of the documented explicit-AI-topic union**, not a claim that GitHub exposes an exhaustive semantic predicate for every repository that a human might consider AI-related.

## Frozen discovery vocabulary

Every topic below was queried with the same hard qualifiers:

```text
created:2025-01-01..2026-08-19 stars:>1000
```

### General AI / ML

- `ai`
- `artificial-intelligence`
- `machine-learning`
- `deep-learning`
- `reinforcement-learning`

### Language models / reasoning

- `llm`
- `large-language-models`
- `transformers`
- `natural-language-processing`

### Agents / interoperability

- `ai-agents`
- `agentic-ai`
- `mcp`
- `model-context-protocol`

### Retrieval / knowledge

- `rag`
- `retrieval-augmented-generation`

### Vision / multimodal / generative media

- `computer-vision`
- `vision-language-model`
- `multimodal`
- `generative-ai`
- `diffusion`
- `diffusion-models`

### Speech / audio

- `text-to-speech`
- `speech-recognition`

## Exhaustion gates verified

A topic is marked exhausted only after requesting the first GitHub Search page that returns zero repositories.

| Topic | Result pages | First empty page | Gate |
|---|---:|---:|---|
| `ai` | 1–7 | 8 | PASS |
| `artificial-intelligence` | 1 | 2 | PASS |
| `machine-learning` | 1 | 2 | PASS |
| `deep-learning` | 1 | 2 | PASS |
| `reinforcement-learning` | 1 | 2 | PASS |
| `llm` | 1–6 | 7 | PASS |
| `large-language-models` | 1 | 2 | PASS |
| `transformers` | 1 | 2 | PASS |
| `natural-language-processing` | 1 | 2 | PASS |
| `ai-agents` | 1–4 | 5 | PASS |
| `agentic-ai` | 1–2 | 3 | PASS |
| `mcp` | 1–5 | 6 | PASS |
| `model-context-protocol` | 1 | 2 | PASS |
| `rag` | 1–2 | 3 | PASS |
| `retrieval-augmented-generation` | 1 | 2 | PASS |
| `computer-vision` | 1 | 2 | PASS |
| `vision-language-model` | 1 | 2 | PASS |
| `multimodal` | 1 | 2 | PASS |
| `generative-ai` | 1 | 2 | PASS |
| `diffusion` | 1 | 2 | PASS |
| `diffusion-models` | 1 | 2 | PASS |
| `text-to-speech` | 1 | 2 | PASS |
| `speech-recognition` | 1 | 2 | PASS |

## Evidence format

Repository links are stored under `trend-research/categories/`. Large categories are split into page files mirroring GitHub Search pagination. Smaller categories are one Markdown file each. A repository may legitimately appear in more than one category because GitHub repositories may have several relevant topics.

Every stored repository link uses the canonical owner/repository value returned by GitHub at snapshot time:

```text
https://github.com/OWNER/REPOSITORY
```

The hard star/date filters are enforced by the GitHub repository-search query, not inferred from repository names or descriptions.

## QA / reproducibility rules

1. No link is admitted solely because its name contains `AI`, `GPT`, `LLM`, `agent`, or similar text.
2. Every included repository is backed by at least one explicit topic query with the hard date/star filters.
3. Every documented topic query was paginated until the first empty page.
4. Canonical link casing comes from GitHub's current `repository_full_name` / returned owner and repository names.
5. Search vocabulary is frozen above for this snapshot, so the result can be reproduced rather than silently changing the meaning of "AI-related".

## Branch-name note

The requested literal branch name `Trend Research` was rejected by GitHub with HTTP 422 because a Git ref cannot contain a space. The research is therefore stored on the syntactically normalized branch **`Trend-Research`**.

## Known boundary

GitHub has no global, canonical `AI-related=true` field. Topic metadata is user-maintained and can be missing even for genuinely AI-related software. Accordingly, **global semantic completeness across all of GitHub cannot be proven from GitHub metadata alone**. What is proven here is exhaustion of the explicitly documented topic universe above under the requested date/star constraints.
