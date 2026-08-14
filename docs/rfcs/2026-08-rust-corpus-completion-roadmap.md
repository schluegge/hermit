# RFC: Rust Corpus Completion Roadmap

Status: Draft roadmap  
Date: 2026-08-14  
Branch: `roadmap/rust-corpus-completion`

## 1. Goal

Build a continuously reproducible, provenance-preserving corpus and knowledge system for Rust that aims to capture every publicly discoverable Rust source artifact that we are legally and technically allowed to ingest, classify it, deduplicate it, and make it queryable at progressively deeper semantic levels.

This is intentionally larger than an "awesome list" or crate catalog. The target is a measured corpus with explicit source coverage, immutable provenance, reproducible ingestion, exact and semantic deduplication, and machine-verifiable completion criteria for every finite source universe.

The phrase "all Rust on the Internet" must not be treated as a claim that can be proven globally. The Internet is open-ended, mutable, partially inaccessible, and contains sources that cannot be enumerated. Therefore Hermit must distinguish:

1. **Finite/enumerable source universes** — completion can be proven at a point in time.
2. **Known but partially enumerable source universes** — coverage can be measured with explicit gaps.
3. **Open-web discovery** — completion cannot be proven; only search saturation and repeated no-new-class discovery can be measured.

The project is complete only when this distinction is visible in the data model and UI/API. We must never silently turn partial retrieval into "complete" coverage.

## 2. Non-goals

- Do not replace original upstream repositories or erase attribution.
- Do not make popularity, stars, downloads, or recency equivalent to quality.
- Do not flatten distinct revisions, forks, licenses, build targets, feature sets, or historical compiler contexts into one record.
- Do not redistribute source code whose license or source terms do not permit redistribution.
- Do not discard duplicate provenance just because bytes are deduplicated.
- Do not use one search engine, one archive, one package registry, or one code forge as a proxy for the Internet.

## 3. Core design principle: content-addressed evidence, not "rows of lines"

The raw canonical storage unit is an immutable source **blob**, not an individual line.

Every unique raw blob receives at least:

- SHA-256
- BLAKE3
- byte length
- MIME/content classification
- source-language evidence
- first/last-seen timestamps
- ingest receipt

Separate provenance records then connect the same blob to every known occurrence:

`source -> origin -> repository/artifact -> revision/version -> path/block -> blob`

A source blob may therefore occur in hundreds of forks, crate releases, documentation mirrors, snippets, vendor trees, or copied projects while being stored physically once.

Derived representations are separate objects and never replace the raw source:

- normalized text fingerprint
- token stream
- syntax tree
- item/symbol graph
- AST structural fingerprints
- rust-analyzer semantic model where available
- rustc HIR/MIR-derived fingerprints where available
- build/test/benchmark evidence
- vector representation where useful

## 4. Provenance is mandatory

No blob is useful without evidence of where it came from.

Minimum provenance fields:

- source adapter and adapter version
- source universe identifier
- canonical origin URL/identifier
- retrieval URL/identifier
- upstream object/revision/version identifiers
- repository identity if applicable
- branch/tag/commit/version if applicable
- original path or snippet/block identifier
- retrieval timestamp
- HTTP/API response metadata sufficient for audit when applicable
- upstream checksum when provided
- Hermit checksums
- license evidence and confidence
- robots/terms/access classification where relevant
- deletion/takedown/tombstone state
- exact ingest receipt ID

For Git-backed material, preserve commit and blob identities independently from Hermit's own hashes.

## 5. Source universe registry

Every source adapter must be registered before bulk ingestion. A registry entry must contain:

- `source_universe_id`
- human-readable name
- source class
- authoritative documentation URL
- discovery mechanism
- enumeration mechanism
- pagination/cursor semantics
- whether enumeration is finite at snapshot time
- whether raw content is available
- rate limits
- authentication requirements
- robots/terms notes
- license/redistribution policy
- update mechanism
- cursor/checkpoint schema
- expected object count if independently knowable
- observed object count
- last full reconciliation timestamp
- error and exclusion counts
- known blind spots

No source may be labeled `complete` without a documented enumeration mechanism and reconciliation evidence.

## 6. Initial source classes

This is the starting taxonomy. Discovery must continue until repeated independent searches stop producing materially new source classes.

### 6.1 Rust first-party and official ecosystem

Highest-priority canonical baseline:

- `rust-lang/rust`: compiler, standard libraries, rustdoc, tests, bootstrap, bundled tools
- Cargo
- rust-analyzer
- Clippy
- rustfmt
- Miri
- portable-simd
- rustc_codegen_cranelift and other Rust compiler-team repositories
- official Rust project repositories and working-group repositories containing Rust
- historical releases/tags/branches where retrievable

Why first: this gives Hermit language-definition-adjacent code, compiler tests, standard-library implementations, diagnostics, unsafe patterns, target-specific code, and historical language evolution.

### 6.2 crates.io

Treat crates.io as an enumerable package universe, not merely a website search target.

Ingest:

- complete Cargo registry index metadata
- every crate name
- every published version
- yanked state
- index checksum
- downloadable `.crate` artifact for each version where available
- Cargo.toml metadata
- lockfiles included in artifacts
- README/license files
- all `.rs` and generated Rust sources contained in published archives
- repository/homepage/documentation links
- owner/category/keyword/download metadata where useful but never as quality truth
- crates.io database dump metadata where officially available

The Cargo registry index specifies both index representation and crate download endpoints. Hermit should use the registry protocol directly and reconcile index versions against downloaded artifacts.

### 6.3 Alternate Cargo registries

Discover and register public alternate Cargo registries from:

- Cargo configuration found in public repositories
- public Forgejo/GitLab/GitHub package registries exposing Cargo protocol
- public organizational documentation
- web discovery

Each registry becomes its own finite source universe only if it exposes a complete enumerable index.

### 6.4 Software Heritage

Software Heritage is a strategic bootstrap and reconciliation source because its explicit mission is to archive publicly available source code at world scale.

Use it for:

- source-origin discovery
- content-addressed cross-checking
- historical revisions no longer available at their original origin
- cross-forge reconciliation
- provenance enrichment
- discovery of repositories missed by forge-specific adapters
- archive-gap analysis

Hermit should use Software Heritage identifiers where possible as external stable identifiers, but must retain its own ingest receipts and source-specific provenance.

Software Heritage must not be treated as the only source because archive lag, takedowns, missing origins, and source-specific metadata can differ.

### 6.5 GitHub

Do not use GitHub code search as the completeness mechanism. Search APIs are intentionally bounded and can return incomplete results.

Primary enumeration strategy:

- enumerate public repositories through GitHub's public-repository listing mechanism and incremental repository IDs
- maintain a monotonic checkpoint
- obtain repository language/path evidence
- retrieve candidate repositories/files using documented Git/object/archive mechanisms
- separately ingest Gists containing Rust
- keep fork relationships and commit/blob identities
- use code search only as a discovery/reconciliation channel, never as proof of completeness

Additional discovery channels:

- repository topics
- Cargo manifests referencing Git dependencies
- release assets containing source archives
- submodules
- vendored trees

### 6.6 GitLab.com and public GitLab instances

For GitLab.com:

- enumerate public projects using keyset pagination where supported
- retrieve repository trees, blobs, and archives through the repository APIs
- retain project IDs, commit IDs, blob IDs, paths, forks, mirrors, and namespaces

For self-hosted GitLab:

- maintain an instance registry
- discover instances independently via web, Software Heritage origins, package metadata, and repository links
- only claim per-instance completeness where public project enumeration is possible

### 6.7 Forgejo/Gitea/Codeberg instances

Forgejo exposes paginated repository search and repository APIs. Treat each discovered public instance as a separate source universe.

Important targets include Codeberg plus independently hosted Forgejo/Gitea instances.

Instance discovery is itself open-ended; therefore track:

- discovered instances
- verified active instances
- instances with public enumeration enabled
- instances inaccessible to automated retrieval
- completed snapshots per instance

### 6.8 Bitbucket Cloud

Use the official Bitbucket Cloud REST API to enumerate repositories where possible and retrieve source trees/content and file history. Preserve workspace, repository, commit, and path identifiers.

### 6.9 SourceHut

Ingest public Rust repositories from `git.sr.ht` and Rust fragments from relevant SourceHut services, including `paste.sr.ht` where publicly enumerable/discoverable.

Use SourceHut's GraphQL APIs and preserve repository and object identities.

### 6.10 Other Git/Mercurial hosting

Continuously discover:

- independent bare Git servers
- cgit
- Gitweb
- Pagure
- Savannah
- Launchpad
- Heptapod
- Mercurial hosting
- Fossil repositories where Rust appears
- project-specific source browsers

Each platform gets an adapter only after a documented discovery/enumeration analysis.

### 6.11 Operating-system and distribution source archives

Rust code can appear outside Rust-specific package registries.

Candidate source universes include:

- Debian source packages / Debian Sources
- Ubuntu source archives
- Fedora source packages
- Arch package sources
- Alpine aports/source packages
- Gentoo ebuild source references
- Nix/Nixpkgs source references
- Homebrew formulas/casks that point to Rust projects
- BSD ports/pkgsrc systems
- Android/AOSP trees
- Chromium and other large monorepos containing Rust
- Linux/kernel-adjacent Rust trees and mirrors

Prefer original upstream content for canonical provenance, but retain distro patches as distinct derived revisions because they contain unique Rust code.

### 6.12 Documentation and generated source views

Discover Rust embedded in:

- docs.rs source views
- rustdoc source pages
- mdBook documentation
- API documentation examples
- README files
- tutorials
- RFCs
- issue/PR discussions when they contain fenced Rust blocks

Do not duplicate a source blob if the documentation merely mirrors an already-known crate/repository file; record the additional occurrence/provenance edge instead.

### 6.13 Q&A, forums, and discussion archives

Ingest Rust code blocks and snippets from sources such as:

- Stack Overflow / Stack Exchange data access mechanisms
- users.rust-lang.org
- internals.rust-lang.org
- Rust project Zulip exports where public and ingestible
- public mailing-list archives
- public issue trackers and discussions across forges

Every snippet must retain post/comment/message identity, author attribution where terms allow, timestamp, and surrounding-context pointer.

Snippet licensing and redistribution must be handled separately from repository licenses.

### 6.14 Snippet and paste services

Discover Rust fragments from:

- GitHub Gists
- SourceHut pastes
- Rust Playground share links/artifacts where recoverable
- public paste services
- code-sharing platforms

This class is usually not globally enumerable; track discovery saturation rather than false completeness.

### 6.15 Blogs, books, courses, and arbitrary web pages

Rust examples occur in ordinary HTML, Markdown, notebooks, PDFs, static sites, books, and course material.

Use multiple independent discovery paths:

- general web search
- Common Crawl-derived discovery where legally and operationally appropriate
- link extraction from already-known Rust pages
- sitemap/RSS discovery
- `text/rust`, `.rs`, fenced `rust`, `cargo`, `rustc`, and Rust-specific syntax heuristics
- reverse links from package/repository metadata

This remains an open universe. The system must report saturation metrics, not "complete".

### 6.16 Academic and benchmark datasets

Discover public datasets that contain source code or Rust subsets, including:

- code-clone research corpora
- software-engineering mining datasets
- code-search datasets
- vulnerability datasets
- benchmark suites
- code-generation training/evaluation corpora where licensing permits use

These are valuable as independent reconciliation channels because they can preserve code from sources no longer online.

### 6.17 Dependency caches, vendored code, generated code, and mirrors

Do not discard these as "duplicates" before provenance analysis.

Classify separately:

- `cargo vendor` trees
- repository mirrors
- forks
- generated bindings
- generated protobuf/FFI code
- patched downstream copies
- copied examples
- template-generated projects

They are major evidence for code diffusion and provenance, even when their bytes deduplicate to an existing blob.

## 7. Acquisition architecture

Every adapter implements the same conceptual pipeline:

1. `discover`
2. `enumerate`
3. `checkpoint`
4. `fetch_metadata`
5. `fetch_content`
6. `verify`
7. `emit_receipt`
8. `normalize_derived_views`
9. `classify`
10. `deduplicate`
11. `index`
12. `reconcile`

Adapters must be resumable and idempotent.

Required operational properties:

- deterministic cursors where the source allows them
- append-only ingest receipts
- retry classes for transient failures
- explicit permanent-failure reasons
- rate-limit awareness
- conditional requests/ETags where available
- immutable raw-object storage
- reproducible derived-index rebuilds
- source adapter versioning
- per-source dashboards

## 8. Storage layers

Do not force all workloads into one database.

### Layer A: raw object store

Content-addressed immutable blobs and source archives.

### Layer B: provenance/relational metadata

Origins, repositories, versions, revisions, paths, snippets, licenses, receipts, cursors, source-universe status, exclusions.

### Layer C: analytical lake

Columnar snapshots for large-scale analysis, likely Arrow/Parquet-compatible, partitioned by source/snapshot/language/object type.

### Layer D: graph

Edges including:

- repository -> revision
- revision -> path
- path occurrence -> blob
- crate -> version
- version -> dependency
- symbol -> references/calls/implements
- blob -> clone cluster
- snippet -> probable origin
- fork/mirror/derived-from relations

### Layer E: search indexes

Separate indexes for:

- exact identifiers
- lexical code search
- regex/path search
- symbol/API search
- structural search
- semantic/vector search

Choose concrete engines only after a corpus-size and access-pattern benchmark. The architecture must permit replacement.

## 9. Rust detection

File extension alone is insufficient.

Evidence can include:

- `.rs` path
- Cargo manifest membership
- GitHub Linguist / forge language classification
- tree-sitter-rust parse success
- rustc/rust-analyzer parse evidence
- fenced-code language tag
- Rust lexical/syntactic classifier
- neighboring Cargo.toml or Rust documentation context

Store detection evidence and confidence instead of a single opaque boolean.

## 10. Exact deduplication

Exact dedup must happen before expensive semantic work.

Levels:

### D0: byte identity

Same bytes -> one raw blob, unlimited provenance occurrences.

### D1: transport normalization fingerprint

Derived fingerprint after safe transport normalization such as newline representation. Never replace the raw blob.

### D2: lexical normalization

Token-level fingerprints that can ignore formatting and optionally comments.

### D3: renamed-token clone fingerprints

Detect copied code with renamed identifiers/literals while preserving the original representations.

### D4: AST structural fingerprints

Hash normalized Rust syntax subtrees at item/block/expression levels.

### D5: semantic structure

Use rust-analyzer and/or compiler-derived information to group implementations that are structurally different but represent the same API/behavioral pattern.

### D6: behavioral equivalence candidates

Where code can be safely built and tested, use tests/property tests/fuzzing/generated cases to gather evidence that implementations are behaviorally equivalent. Never label semantic equivalence as proven solely from embeddings.

## 11. Parsing and semantic enrichment

Progressive enrichment pipeline:

1. tree-sitter-rust parse
2. edition inference
3. Cargo workspace/crate/module graph
4. item extraction
5. symbol definitions/references
6. type information where recoverable
7. macro/proc-macro boundaries
8. cfg/features/targets
9. unsafe blocks and unsafe APIs
10. FFI surfaces
11. async/concurrency primitives
12. `no_std`/embedded/WASM/kernel/platform classifications
13. rust-analyzer semantic graph
14. optional rustc HIR/MIR extraction for compilable snapshots

Every derived record must reference the parser/compiler/tool version used.

## 12. Historical compiler compatibility

Do not judge historical Rust only with the newest compiler.

For compilable projects/artifacts, record:

- declared MSRV when available
- inferred minimum successful toolchain where practical
- Rust edition
- stable/beta/nightly requirements
- removed/renamed features
- target triples
- required native/system dependencies
- feature combinations

Maintain a toolchain matrix for representative and high-value artifacts. Historical builds are evidence, not merely CI noise.

## 13. Build, test, lint, and dynamic evidence

For material that can be executed safely in an isolated environment, collect:

- `cargo metadata`
- `cargo check`
- `cargo test` / nextest-compatible results
- doctests
- Clippy diagnostics
- rustdoc status
- Miri where applicable
- fuzz targets
- benchmarks
- sanitizer support where applicable
- coverage where practical
- compile-time and artifact-size metrics where useful

Never execute arbitrary Internet code directly on the host. All builds/tests require isolated sandboxes with denied-by-default network and constrained resources.

## 14. License and policy layer

A perfect corpus without provenance/license handling is unusable.

Per repository/artifact/file/snippet, retain:

- declared SPDX identifier/expression when present
- detected license texts
- package registry license metadata
- file-level exceptions/headers
- source terms
- attribution requirements
- redistribution status
- modification/derivative restrictions
- uncertainty/conflict state

Recommended states:

- `redistributable`
- `metadata_only`
- `internal_analysis_only`
- `unknown_review_required`
- `takedown`

Never infer that public accessibility equals permission to republish.

## 15. Quality and canonicalization

Deduplication alone does not answer "what implementation should Hermit prefer?"

Build a separate evidence-based ranking model using factors such as:

- source authority
- maintenance state
- compiler compatibility
- test evidence
- property/fuzz evidence
- Miri/sanitizer evidence
- dependency risk
- known vulnerabilities
- unsafe surface
- API stability/semver history
- benchmark evidence
- documentation/examples
- platform coverage
- reproducibility

Stars/downloads may be features but must never dominate correctness evidence.

Preserve competing implementations when tradeoffs differ.

## 16. Knowledge extraction beyond a corpus

The long-term target is not just "find code". It is to construct a Rust implementation graph.

Extract reusable concepts such as:

- task/problem solved
- API surface
- trait relationships
- algorithms/data structures
- error-handling pattern
- ownership/lifetime strategy
- concurrency model
- unsafe invariant
- allocation behavior
- platform assumptions
- security properties
- performance envelope
- dependencies
- examples/tests proving behavior

This allows queries such as:

- "show every materially distinct implementation of an LRU cache in Rust"
- "which implementations are `no_std`, safe-only, and allocation-free?"
- "show implementations of this API pattern that survived Miri and fuzzing"
- "trace where this code fragment first appeared and how it propagated"
- "show the smallest dependency closure implementing capability X"

## 17. Completeness ledger

This is the mechanism that prevents premature completion claims.

For every source universe and snapshot record:

- enumerator version
- snapshot start/end
- first cursor
- final cursor
- pages/partitions expected
- pages/partitions inspected
- objects enumerated
- objects fetched
- objects excluded
- objects inaccessible
- transient failures remaining
- permanent failures
- content bytes
- unique raw blobs
- Rust-positive blobs
- Rust-uncertain blobs
- parse success/failure counts
- license-known/unknown counts
- reconciliation count against independent sources

A finite source snapshot is `complete` only if:

1. enumeration reached its documented terminal condition;
2. all pages/partitions are reconciled;
3. every discovered object has a terminal state: fetched, intentionally excluded, inaccessible with reason, or tombstoned;
4. no transient failures remain unresolved;
5. counts and checkpoints are persisted;
6. an independent reconciliation pass finds no unexplained gap above the defined threshold.

## 18. Open-web saturation protocol

Because the open web is not finite, use explicit research stopping criteria:

- maintain a cumulative source-class/candidate set
- use multiple independent search engines/datasets/discovery paths
- search terminology variants and non-English terms
- inspect one abstraction layer above and below each major source class
- actively search for counterexamples to the current source taxonomy
- rerank the entire source universe registry periodically
- stop only when repeated discovery passes produce no materially new source classes and remaining discoveries are instances of already-covered classes

The result is `saturated_as_of`, never `complete`.

## 19. Reconciliation strategy

Use independent sources to detect blind spots.

Examples:

- crates.io repository URLs vs forge enumeration
- Software Heritage origins vs forge adapters
- Git dependencies in Cargo manifests vs known repositories
- docs.rs source links vs crate archive contents
- distro source-package upstream URLs vs known origins
- search-engine `.rs` results vs known origins
- Stack Overflow links to GitHub vs known origins
- dependency graphs vs registered Cargo registries

Every unexplained mismatch becomes a discovery task, not an ignored anomaly.

## 20. Roadmap

### Phase 0 — Contract and evidence model

Deliverables:

- source-universe schema
- provenance schema
- ingest receipt schema
- blob identity scheme
- snapshot/completeness ledger
- exclusion/failure taxonomy
- license-policy states
- adapter interface contract

Acceptance:

- a synthetic source can be enumerated twice with identical terminal counts and no duplicate raw storage
- every raw blob can be traced back to at least one immutable ingest receipt

### Phase 1 — Official Rust baseline

Ingest Rust first-party repositories and release history.

Acceptance:

- documented repository set reconciled against Rust project/compiler-team repository lists
- every `.rs` occurrence represented with revision/path provenance
- standard library/compiler/tooling code queryable separately

### Phase 2 — crates.io closure

Ingest the complete crates.io index and all retrievable crate versions.

Acceptance:

- index terminal state captured
- every version has terminal artifact state
- downloaded artifact checksum reconciled with index checksum
- all Rust files extracted and content-addressed
- yanked versions retained, not silently omitted

### Phase 3 — Software Heritage bootstrap/reconciliation

Build Software Heritage adapter and ingest Rust-relevant origins/content references at scale.

Acceptance:

- SWH identifiers retained
- known crates.io/GitHub origins reconciled
- archive-only historical content can be distinguished from live-origin content

### Phase 4 — Major forge enumeration

Implement GitHub, GitLab.com, Bitbucket Cloud, Codeberg/Forgejo, and SourceHut adapters.

Acceptance per finite forge/instance snapshot:

- cursor terminal condition reached
- object counts persisted
- `.rs`/Rust detection pipeline applied
- failures terminally classified
- independent reconciliation performed

### Phase 5 — Forge discovery expansion

Create instance discovery and adapters for self-hosted GitLab, Forgejo/Gitea, cgit/Gitweb, Pagure, Savannah, Launchpad, and other identified hosts.

Acceptance:

- source-class registry updated by repeated discovery passes
- every discovered instance has explicit coverage/access state

### Phase 6 — Fragment sources

Add Gists, SourceHut paste, Rust Playground artifacts where possible, Stack Exchange, Rust forums, documentation code blocks, public issue/PR discussion snippets, blogs/books/tutorial discovery.

Acceptance:

- snippets preserve exact surrounding source identity and licensing state
- copied repository code links to existing blobs/clone groups where detected

### Phase 7 — Distribution and monorepo sources

Add distro source archives and large non-Rust-specific monorepos containing Rust.

Acceptance:

- downstream patches represented as distinct provenance/revision objects
- upstream-vs-downstream relationships captured when inferable

### Phase 8 — Exact and clone dedup

Implement D0-D4 systematically before expensive semantic analysis.

Acceptance:

- physical raw storage deduplicated by byte identity
- provenance occurrence count unaffected by dedup
- benchmark corpus measures precision/recall for clone stages

### Phase 9 — Rust semantic graph

Implement tree-sitter, Cargo graph, rust-analyzer, and selective rustc enrichment.

Acceptance:

- parser/tool version recorded for every derived object
- symbol/item/API queries reproducible from a clean index build

### Phase 10 — Build/test/toolchain matrix

Create sandboxed compilation and evidence runners.

Acceptance:

- no arbitrary Internet artifact executes on host
- network denied by default
- resource/time limits recorded
- results keyed by source revision, toolchain, target, feature set, and runner version

### Phase 11 — Licensing and redistribution gate

Integrate license detection, SPDX normalization, conflicting-evidence handling, and takedown/tombstone workflow.

Acceptance:

- every stored occurrence has an explicit distribution-policy state
- public export cannot emit `metadata_only`, `internal_analysis_only`, `unknown_review_required`, or `takedown` content

### Phase 12 — Canonical implementation mining

Create capability/task clusters and rank materially distinct implementations by evidence.

Acceptance:

- ranking explanations expose evidence and uncertainty
- popularity never substitutes for build/test/security evidence
- materially different tradeoffs remain discoverable

### Phase 13 — Continuous ingestion

Turn one-shot crawls into incremental adapters with checkpoints and scheduled reconciliation.

Acceptance:

- snapshots can be reproduced
- adapters resume after interruption
- source updates do not destroy historical snapshots
- per-source lag and error budgets visible

### Phase 14 — Saturation campaign

Run repeated independent discovery passes across the open web and research datasets until no new major source classes appear.

Acceptance:

- discovery logs preserved
- new source classes per pass trend to zero
- unresolved blind spots explicitly listed
- final status is `saturated_as_of=<date>`, not universal completeness

## 21. First implementation slice

Do not start by crawling GitHub blindly.

The first end-to-end vertical slice should be:

1. source-universe registry
2. immutable blob store
3. provenance/receipt schema
4. completeness ledger
5. crates.io index enumerator
6. one crate-version downloader
7. extraction of `.rs` files
8. exact byte dedup
9. tree-sitter parse
10. query proving multiple occurrences can point to one blob
11. reconciliation report

Once this is correct, scale to all crates.io versions. Only then add another large source.

## 22. Metrics that matter

Track at least:

- source universes registered
- finite universes complete
- finite universes incomplete
- discovered origins
- artifacts/revisions
- source occurrences
- raw bytes fetched
- unique raw bytes after exact dedup
- dedup ratio
- Rust-positive blobs
- Rust-uncertain blobs
- parse success rate
- buildable artifact rate by toolchain
- license-known rate
- inaccessible/excluded count by reason
- unresolved transient errors
- clone clusters by level
- provenance edges
- independent reconciliation gaps
- new source classes discovered per saturation pass

## 23. Hard invariants

1. **No provenance, no canonical corpus record.**
2. **Raw bytes are immutable.**
3. **Derived normalization never overwrites source.**
4. **Deduplication removes storage duplication, not historical/provenance occurrences.**
5. **Search results are discovery evidence, not enumeration evidence.**
6. **A finite source is not complete until counts/cursors/failures reconcile.**
7. **The open web is never labeled universally complete.**
8. **Publicly accessible is not synonymous with redistributable.**
9. **Historical Rust is analyzed with historical context/toolchains where material.**
10. **Popularity is not correctness.**
11. **Arbitrary Internet code never executes unsandboxed.**
12. **Every derived semantic claim records the tool/model/version that produced it.**

## 24. Additional high-value ideas

### 24.1 Code genealogy graph

Use clone fingerprints plus commit dates and provenance to estimate code lineage: where an implementation likely originated, how it spread through forks/snippets/vendors, and where mutations occurred.

### 24.2 "Implementation periodic table"

Cluster Rust implementations by capability rather than crate name. A capability can have multiple implementations with explicit tradeoffs: `std`/`no_std`, safe/unsafe, alloc/no-alloc, sync/async, target support, dependency count, license, benchmark envelope, and evidence quality.

### 24.3 Negative knowledge

Store failed approaches, compiler errors, unsound patterns, CVEs, removed APIs, failed fuzz cases, and Miri findings. A perfect Rust knowledge base must know what *not* to reproduce.

### 24.4 Temporal Rust

Treat Rust as a time-varying language/ecosystem. Preserve when APIs, compiler behavior, editions, lints, crates, and implementation patterns changed.

### 24.5 Differential implementation testing

When multiple implementations claim the same capability, generate shared property tests and fuzz corpora and execute them across implementations. This can discover semantic differences that code similarity misses.

### 24.6 Minimal implementation synthesis

Once capability clusters are mature, derive evidence-backed minimal dependency closures for a requested capability. This is more useful than selecting the most popular crate.

### 24.7 Source-confidence graph

Keep "official", "upstream", "mirror", "fork", "vendored", "generated", "snippet", "unknown origin", and "probable derivative" as explicit evidence states. Do not collapse them into a single quality score.

### 24.8 Counterexample-first ranking

Before labeling an implementation canonical, actively search the corpus for implementations that beat it on safety, portability, dependency surface, performance, maintenance, or correctness evidence.

## 25. Current authoritative anchors

The roadmap should be updated when these contracts change:

- Cargo registry index and registry protocols: https://doc.rust-lang.org/cargo/reference/registry-index.html
- Cargo source replacement/vendor model: https://doc.rust-lang.org/cargo/reference/source-replacement.html
- Rust compiler source layout: https://rustc-dev-guide.rust-lang.org/compiler-src.html
- Rust external compiler-team repositories: https://rustc-dev-guide.rust-lang.org/external-repos.html
- Software Heritage data access: https://docs.softwareheritage.org/user/using_data/index.html
- Software Heritage API overview: https://docs.softwareheritage.org/devel/getting-started/api.html
- GitHub repository API: https://docs.github.com/rest/repos/repos
- GitHub search API limitations: https://docs.github.com/rest/search/search
- GitLab projects API: https://docs.gitlab.com/api/projects/
- GitLab repositories API: https://docs.gitlab.com/api/repositories/
- Bitbucket Cloud source API: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-source/
- Forgejo API usage: https://forgejo.org/docs/latest/user/api-usage/
- SourceHut APIs: https://docs.sourcehut.org/

## 26. Definition of success

Hermit's Rust corpus is successful when a user can ask for a Rust capability, implementation, API, pattern, historical variant, unsafe invariant, or source fragment and receive:

- the materially distinct implementations known to the corpus;
- exact provenance for each;
- license/distribution state;
- dedup/clone relationships;
- build/compiler/target context;
- quality/security/test evidence;
- known counterexamples and tradeoffs;
- explicit corpus coverage and blind spots for the relevant source universes.

The objective is not a bigger list. The objective is a reproducible, evidence-carrying map of Rust source code and its evolution.