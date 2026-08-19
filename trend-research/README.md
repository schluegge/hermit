# AI Trend Research — GitHub repositories created since 2025

Snapshot date: **2026-08-19 (Europe/Berlin)**

## Scope

This inventory researches public GitHub repositories that satisfy both hard filters:

- repository creation date: `2025-01-01..2026-08-19`
- current GitHub stars: `>1000` (strictly more than 1000)

The phrase **"has a relation to AI"** is not a canonical GitHub field. To avoid subjective guessing, inclusion is evidence-based. A repository must be returned by at least one documented AI/ML-related GitHub topic query below. Topic vocabulary is sourced either directly from explicit AI concepts or from an AI/ML category in the central `sindresorhus/awesome` taxonomy.

This is therefore an **exhaustive snapshot of the documented discovery vocabulary**, not a claim that GitHub exposes a universal semantic predicate for every repository a human might consider AI-related.

## Discovery lanes

### Lane A — explicit AI-topic sweep

The initial sweep uses direct AI/ML topics such as `ai`, `llm`, `machine-learning`, `ai-agents`, `rag`, `mcp`, multimodal/generative-media topics, and speech topics.

### Lane B — `sindresorhus/awesome`

The central Awesome index is used as an independent taxonomy source. Its explicit AI/ML branches include Artificial Intelligence, Machine Learning, Software Engineering for Machine Learning, Core ML, JAX, XAI, Speech/NLP, Question Answering, Computer Vision, Deep Learning, and TensorFlow-family lists.

Detailed source evidence and acceptance/rejection rules are stored at:

```text
trend-research/sources/awesome-awesome.md
```

Broad adjacent Awesome categories such as `data-science` and `robotics` are **not** standalone inclusion predicates because those labels alone do not prove an AI relationship for every repository.

## Hard query qualifiers

Every accepted or zero-result topic probe uses:

```text
created:2025-01-01..2026-08-19 stars:>1000
```

## Frozen accepted discovery vocabulary

### General AI / ML

- `ai`
- `artificial-intelligence`
- `machine-learning`
- `deep-learning`
- `reinforcement-learning`
- `neural-networks`
- `mlops`
- `coreml`
- `jax`
- `explainable-ai`
- `xai`

### Language models / reasoning / NLP

- `llm`
- `large-language-models`
- `transformers`
- `natural-language-processing`
- `question-answering`

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
| `neural-networks` | 1 | 2 | PASS |
| `mlops` | 1 | 2 | PASS |
| `coreml` | 1 | 2 | PASS |
| `jax` | 1 | 2 | PASS |
| `explainable-ai` | 1 | 2 | PASS |
| `xai` | 1 | 2 | PASS |
| `llm` | 1–6 | 7 | PASS |
| `large-language-models` | 1 | 2 | PASS |
| `transformers` | 1 | 2 | PASS |
| `natural-language-processing` | 1 | 2 | PASS |
| `question-answering` | 1 | 2 | PASS |
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

## Closed zero-result Awesome-derived probes

These explicit AI/ML-derived topic queries were tested and returned zero repositories on page 1 under the same hard filters:

| Topic | First empty page | Gate |
|---|---:|---|
| `tensorflow` | 1 | PASS / zero-result |
| `tensorflow-lite` | 1 | PASS / zero-result |
| `tensorflowjs` | 1 | PASS / zero-result |
| `natural-language-generation` | 1 | PASS / zero-result |
| `machine-learning-engineering` | 1 | PASS / zero-result |
| `ai-in-finance` | 1 | PASS / zero-result |

## Evidence format

Repository links are stored under `trend-research/categories/`. Large categories are split into page files mirroring GitHub Search pagination. Smaller categories are one Markdown file each. A repository may legitimately appear in more than one category because GitHub repositories may have several relevant topics.

Every stored repository link uses the canonical owner/repository value returned by GitHub at snapshot time:

```text
https://github.com/OWNER/REPOSITORY
```

The hard star/date filters are enforced by the GitHub repository-search query, not inferred from repository names or descriptions.

## QA / reproducibility rules

1. No link is admitted solely because its name contains `AI`, `GPT`, `LLM`, `agent`, or similar text.
2. Every included repository is backed by at least one documented AI/ML-related topic query with the hard date/star filters.
3. Every documented non-empty topic query is paginated until the first empty page.
4. Zero-result probes are explicitly recorded rather than silently discarded.
5. Canonical link casing comes from GitHub's current returned owner/repository names.
6. Awesome-derived topic vocabulary is accepted only where the Awesome taxonomy itself establishes the AI/ML relationship; broad adjacent categories are rejected.
7. Search vocabulary is frozen in this snapshot so the result can be reproduced rather than silently changing the meaning of "AI-related".

## Branch-name note

The requested literal branch name `Trend Research` was rejected by GitHub with HTTP 422 because a Git ref cannot contain a space. The research is therefore stored on the syntactically normalized branch **`Trend-Research`**.

## Known boundary

GitHub has no global, canonical `AI-related=true` field. Topic metadata is user-maintained and Awesome lists are curated rather than exhaustive. Accordingly, **global semantic completeness across all of GitHub cannot be proven from these metadata sources alone**. What is proven here is exhaustion of the explicitly documented discovery vocabulary under the requested date/star constraints.
