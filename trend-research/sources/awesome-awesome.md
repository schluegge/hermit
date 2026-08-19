# Discovery source — sindresorhus/awesome

Snapshot date: **2026-08-19 (Europe/Berlin)**

Canonical source: https://github.com/sindresorhus/awesome

## Purpose

This source is used as a second, independent discovery lane after the initial explicit-AI-topic sweep.

The central Awesome index was inspected for categories whose own title/description establishes an explicit AI or machine-learning relationship. Those categories are then translated into reproducible GitHub topic queries using the same hard filters as the main research:

```text
created:2025-01-01..2026-08-19 stars:>1000
```

## AI/ML-related Awesome taxonomy observed

Direct AI/ML categories and subcategories in the central index include:

- Artificial Intelligence → `owainlewis/awesome-artificial-intelligence`
- Machine Learning → `josephmisiti/awesome-machine-learning`
- Software Engineering for Machine Learning → `SE-ML/awesome-seml`
- Core ML Models → `likedan/Awesome-CoreML-Models`
- H2O → `h2oai/awesome-h2o`
- AI in Finance → `georgezouq/awesome-ai-in-finance`
- JAX → `n2cholas/awesome-jax`
- XAI → `altamiracorp/awesome-xai`
- Speech and Natural Language Processing → `edobashira/speech-language-processing`
- Question Answering → `seriousran/awesome-qa`
- Natural Language Generation → `accelerated-text/awesome-nlg`
- Computer Vision → `jbhuang0604/awesome-computer-vision`
- Deep Learning → `ChristosChristofidis/awesome-deep-learning`
- TensorFlow → `jtoy/awesome-tensorflow`
- TensorFlow.js → `aaronhma/awesome-tensorflow-js`
- TensorFlow Lite → `margaretmz/awesome-tensorflow-lite`

## New topic queries admitted from this source

The following additional GitHub topics are accepted because Awesome explicitly places their corresponding technologies/concepts inside AI/ML categories:

- `jax`
- `explainable-ai`
- `xai`
- `question-answering`
- `mlops`
- `coreml`
- `neural-networks`

## Zero-result gates from this source

These explicit AI/ML-derived queries returned zero repositories under the hard filters and are recorded as closed zero-result gates:

- `tensorflow`
- `tensorflow-lite`
- `tensorflowjs`
- `natural-language-generation`
- `machine-learning-engineering`
- `ai-in-finance`

## Rejected broad adjacency

`data-science` and `robotics` are present in Awesome and can overlap AI, but the topic labels alone do **not** prove an AI relationship for every repository. They are therefore not admitted as standalone inclusion predicates.

A `topic:data-science` probe did return repositories under the date/star filters, but those results are deliberately excluded from the AI inventory unless independently captured by an accepted AI/ML topic.

## QA rule

Awesome is used here as a taxonomy/evidence source, not as a claim that every project in every adjacent Awesome list is AI-related. Broad categories are rejected unless the category itself provides an explicit AI/ML relationship.
