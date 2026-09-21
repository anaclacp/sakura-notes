# AI Glossary

Glossary built while studying Responsible AI, OWASP GenAI and AI Engineering.

## Index

**A** — [Adapter](#adapter) · [Adversarial Perturbation](#adversarial-perturbation) · [AIBOM — AI Bill of Materials](#aibom--ai-bill-of-materials) · [Artifact](#artifact) · [Assumption](#assumption) · [Attestation](#attestation) · [Authorization](#authorization)

**B** — [Backdoor](#backdoor) · [Baseline](#baseline) · [Biased Output](#biased-output) · [Blast Radius](#blast-radius)

**C** — [Chat Template](#chat-template) · [Circuit Breaker](#circuit-breaker) · [Claim-Check-Act](#claim-check-act) · [Concurrency](#concurrency) · [Content Security Policy — CSP](#content-security-policy--csp) · [Context Window](#context-window) · [Context-Aware Output Encoding](#context-aware-output-encoding) · [Continuous Learning](#continuous-learning) · [Control Character](#control-character) · [Corpus / Corpora](#corpus--corpora) · [Cosine Similarity](#cosine-similarity) · [Cost Asymmetry](#cost-asymmetry) · [Cross-Tenant Leakage](#cross-tenant-leakage) · [Curated Dataset](#curated-dataset)

**D** — [Data Exfiltration](#data-exfiltration) · [Data Poisoning](#data-poisoning) · [Deduplication](#deduplication) · [Denial of Wallet — DoW](#denial-of-wallet--dow) · [Deprecated](#deprecated) · [Developer Instructions](#developer-instructions) · [Digest](#digest) · [Distillation](#distillation) · [Downstream](#downstream) · [Downstream Operation](#downstream-operation) · [Drift](#drift) · [Durable Corruption](#durable-corruption) · [DVC — Data Version Control](#dvc--data-version-control)

**E** — [Embedding](#embedding) · [Embedding Inversion](#embedding-inversion) · [EOS — End-of-Sequence Token](#eos--end-of-sequence-token) · [Escaping](#escaping)

**F** — [Fan-Out](#fan-out) · [Feedback Loop](#feedback-loop) · [Fine-Tuning](#fine-tuning) · [Forged Evidence](#forged-evidence) · [Function Schema](#function-schema)

**G** — [Graceful Degradation](#graceful-degradation) · [Groundedness](#groundedness) · [Grounding](#grounding)

**H** — [Hard Spending Cap](#hard-spending-cap) · [Hardening](#hardening) · [Hash](#hash) · [Hash Pinning](#hash-pinning) · [Hidden Context](#hidden-context)

**I** — [Immutable Reference](#immutable-reference) · [Improper Output Handling](#improper-output-handling) · [Incorrect State Inference](#incorrect-state-inference) · [Inference](#inference) · [Inference Endpoint](#inference-endpoint) · [Integrity](#integrity)

**L** — [Label Poisoning](#label-poisoning) · [Lineage](#lineage) · [Log-Probabilities](#log-probabilities) · [Logits](#logits) · [LoRA — Low-Rank Adaptation](#lora--low-rank-adaptation)

**M** — [Membership Inference](#membership-inference) · [Misattributed Evidence](#misattributed-evidence) · [Misinformation](#misinformation) · [Model Card](#model-card) · [Model Extraction](#model-extraction) · [Model Poisoning](#model-poisoning) · [Model Provenance](#model-provenance) · [Multimodal](#multimodal) · [Mutable Reference](#mutable-reference)

**O** — [Omission Failure](#omission-failure) · [Output Budget](#output-budget) · [Output Encoding](#output-encoding) · [Overreliance](#overreliance)

**P** — [Parameterized Query](#parameterized-query) · [Path Traversal](#path-traversal) · [PEFT — Parameter-Efficient Fine-Tuning](#peft--parameter-efficient-fine-tuning) · [Poisoning](#poisoning) · [Pre-Flight Token Estimation](#pre-flight-token-estimation) · [Prepared Statement](#prepared-statement) · [Privilege Separation](#privilege-separation) · [Probing](#probing) · [Provenance](#provenance)

**Q** — [Quantization](#quantization) · [Queue](#queue) · [Quota](#quota)

**R** — [RAG — Retrieval-Augmented Generation](#rag--retrieval-augmented-generation) · [RAG Poisoning](#rag-poisoning) · [Rate Limiting](#rate-limiting) · [RCE — Remote Code Execution](#rce--remote-code-execution) · [Reasoning Loop](#reasoning-loop) · [Recursion Depth](#recursion-depth) · [Red Teaming](#red-teaming) · [Resource Allocation](#resource-allocation) · [Resource Exhaustion](#resource-exhaustion) · [Retrieval Jamming](#retrieval-jamming) · [Reverse Engineering](#reverse-engineering) · [RLHF — Reinforcement Learning from Human Feedback](#rlhf--reinforcement-learning-from-human-feedback) · [Runtime Verification](#runtime-verification)

**S** — [Sandbox / Sandboxing](#sandbox--sandboxing) · [Sanitization](#sanitization) · [SBOM — Software Bill of Materials](#sbom--software-bill-of-materials) · [Security Boundary](#security-boundary) · [Semantic Cache](#semantic-cache) · [Serialization](#serialization) · [Similarity Score](#similarity-score) · [Sleeper Agent](#sleeper-agent) · [Slopsquatting](#slopsquatting) · [Special Token](#special-token) · [Sponge Example](#sponge-example) · [State Hashing](#state-hashing) · [State Inference](#state-inference) · [Supply Chain](#supply-chain) · [System Prompt](#system-prompt)

**T** — [Tampering](#tampering) · [T&Cs — Terms and Conditions](#tcs--terms-and-conditions) · [Tenant](#tenant) · [Thinking Tokens](#thinking-tokens) · [Third Party](#third-party) · [Threshold](#threshold) · [Token Budget](#token-budget) · [Tool Schema](#tool-schema) · [Tool-Calling Loop](#tool-calling-loop) · [Trigger](#trigger) · [Trust Boundary](#trust-boundary) · [Trust Tier](#trust-tier)

**V** — [Validation](#validation) · [Vector Database](#vector-database) · [Vet / Vet a Supplier](#vet--vet-a-supplier)

**X** — [XSS — Cross-Site Scripting](#xss--cross-site-scripting)

**Z** — [Zero Trust](#zero-trust)

**[Key Distinctions](#key-distinctions)** — [Signed ≠ Safe](#signed--safe) · [Safe Format ≠ Safe Model](#safe-format--safe-model) · [Provenance vs Integrity](#provenance-vs-integrity) · [Supply Chain vs Poisoning](#supply-chain-vs-poisoning)

---

## A

### Adapter

A small set of additional parameters used to modify or specialize the behavior of a base model without retraining the whole model.

Common example: **LoRA adapter**.

```text
Base Model + Adapter → Specialized Model
```

---

### Adversarial Perturbation

A carefully crafted small modification to an input designed to cause unexpected or harmful model behavior.

---

### AIBOM — AI Bill of Materials

An inventory of the AI-related components used in a system.

It may include:

- models
- datasets
- adapters
- tokenizers
- frameworks
- inference runtimes
- external AI services

Useful for provenance, security, governance and compliance.

**Think:** AI ingredients list.

---

### Artifact

A file or output produced or consumed during the development and deployment process.

Examples:

- model weights
- checkpoints
- LoRA adapters
- `.safetensors`
- GGUF files
- ONNX models
- containers

---

### Assumption

An idea or condition treated as true without having been directly verified.

In AI systems, assumptions should be clearly distinguished from verified facts.

**PT:** suposição.

---

### Attestation

A mechanism used to verify that a device, environment or software instance is running in an expected and trusted state.

Often used in device and infrastructure security.

---

### Authorization

The process of determining whether an authenticated user, agent, or service is allowed to perform a specific action or access a resource.

Authentication answers **who are you?**

Authorization answers **what are you allowed to do?**

---

## B

### Backdoor

Hidden malicious behavior intentionally inserted into a model or system.

It may remain inactive until a specific trigger is provided.

```text
Normal input → Normal behavior
Trigger → Malicious behavior
```

---

### Baseline

A reference representing normal system behavior or resource usage, used to identify unusual deviations.

---

### Biased Output

An output influenced by distorted, unfair or systematically skewed patterns in the model, training data or other system components.

**PT:** saída enviesada / tendenciosa.

---

### Blast Radius

The maximum scope of damage or impact that a compromised component, account or system can cause.

---

## C

### Chat Template

A formatting template that converts structured chat messages and roles into the token sequence expected by a specific model.

---

### Circuit Breaker

A control that automatically stops execution when predefined limits such as cost, time, steps or recursion depth are reached.

---

### Claim-Check-Act

A safety pattern that separates model generation from execution.

```text
Claim
  ↓
Check
  ↓
Act
```

The model may propose or infer something, but the claim must be independently verified before an action is executed.

---

### Concurrency

The number of operations or tasks that are running at the same time.

---

### Content Security Policy — CSP

A browser security mechanism that restricts which resources, scripts, frames, and other content a web page is allowed to load or execute.

Useful as defense in depth against attacks such as XSS.

---

### Context Window

The maximum amount of information or tokens a model can process within one inference context.

---

### Context-Aware Output Encoding

Encoding model output according to the environment where it will be used.

Examples:

- HTML → HTML encoding
- JavaScript → JavaScript encoding
- URL → URL encoding
- database values → parameterized queries

There is no universal escaping strategy for every output context.

---

### Continuous Learning

A process where a model or system keeps learning from newly collected data after its initial deployment.

---

### Control Character

A non-printable character that controls how a terminal, log viewer, protocol, or other system behaves rather than representing visible text.

Examples include:

- ANSI escape sequences
- BEL
- carriage return
- backspace
- OSC sequences

---

### Corpus / Corpora

A collection of text or data used for training, evaluation or analysis. **Corpora** is the plural of corpus.

---

### Cosine Similarity

A metric commonly used to measure how similar two embedding vectors are based on the angle between them.

Higher similarity generally means that two vectors are considered more semantically related.

Commonly used in vector search and RAG.

---

### Cost Asymmetry

A situation where a small or inexpensive attacker action causes a disproportionately large computational or financial cost for the target system.

---

### Cross-Tenant Leakage

Exposure or inference of information belonging to one tenant by another tenant in a multi-tenant system.

In vector systems, this may happen when similarity search runs across a shared index before tenant-level filtering is applied.

---

### Curated Dataset

A dataset that has been intentionally selected, reviewed, cleaned and organized for a specific purpose or domain.

---

## D

### Data Exfiltration

Unauthorized transfer of sensitive or protected data from an internal system to an external destination.

---

### Data Poisoning

Manipulation or contamination of data so that a model learns incorrect, biased or malicious behavior. It can be intentional or accidental.

---

### Deduplication

The process of detecting and removing duplicate or near-duplicate data.

Semantic deduplication may use embedding similarity rather than exact text matching.

---

### Denial of Wallet — DoW

An attack that deliberately causes excessive paid resource usage until operating the service becomes financially unsustainable.

---

### Deprecated

A component that is still available but is no longer recommended or actively maintained.

Deprecated components may stop receiving security fixes.

---

### Developer Instructions

Internal instructions provided by the application developer to guide model behavior.

They are normally not intended to be visible to the end user, but should still be treated as potentially discoverable.

---

### Digest

A cryptographic identifier derived from the exact content of an artifact.

Frequently used to reference immutable versions of artifacts.

Example:

```text
sha256:...
```

---

### Distillation

A technique where one model is trained using outputs from another model as supervision. It can also be abused to create an unauthorized functional approximation of a proprietary model.

---

### Downstream

Refers to models, systems or processes that depend on the output of an earlier component in a pipeline.

---

### Downstream Operation

An action triggered later in a workflow as a consequence of an earlier request or tool call.

---

### Drift

A gradual change in data distribution or model behavior over time. Drift may indicate degradation, environmental changes or unexpected system behavior.

---

### Durable Corruption

A persistent change to data, memory or model behavior that continues affecting the system beyond a single inference or session.

---

### DVC — Data Version Control

A version-control system for datasets, models and ML artifacts. It helps track changes, reproduce previous versions and roll back when necessary.

---

## E

### Embedding

A numerical vector representation of data such as text, images or audio, designed to capture semantic relationships.

---

### Embedding Inversion

An attack that attempts to reconstruct original or approximate source content from its embedding vectors.

```text
Embedding
   ↓
Inversion
   ↓
Approximate Source Data
```

**Important:** Embedding ≠ anonymous data.

---

### EOS — End-of-Sequence Token

A special token used to indicate that model generation should stop.

---

### Escaping

Transforming special characters so they are interpreted as data rather than executable syntax or control instructions.

The correct escaping method depends on the destination context.

---

## F

### Fan-Out

A pattern where one action triggers multiple additional actions, which may themselves trigger more actions.

---

### Feedback Loop

A process where system outputs or user feedback are fed back into future decisions, training or model updates. Poorly controlled feedback loops can amplify errors or poisoning.

---

### Fine-Tuning

Additional training performed on an existing model to adapt it to a specific task, domain or behavior.

---

### Forged Evidence

Fabricated or manipulated information presented as if it were legitimate evidence.

Examples:

- nonexistent reports
- fabricated citations
- fake tool results
- invented records

---

### Function Schema

A structured description of a function available to an LLM or agent.

It may define:

- function name
- parameters
- parameter types
- descriptions
- required fields

Function schemas can reveal application capabilities and should not be treated as secrets or authorization mechanisms.

---

## G

### Graceful Degradation

A design strategy where the system reduces functionality under stress instead of completely failing.

---

### Groundedness

The degree to which a model's claims are supported by the provided or authoritative evidence.

A response can be fluent and confident while having poor groundedness.

---

### Grounding

Connecting model outputs to external or verifiable information instead of relying only on the model's internal knowledge.

---

## H

### Hard Spending Cap

A strict budget limit that stops further execution or API usage when the configured financial threshold is reached.

---

### Hardening

The process of reducing a system's attack surface and strengthening its security configuration.

---

### Hash

A fixed-length value generated from data.

It can be used to detect whether an artifact has changed.

```text
Expected hash == Actual hash
→ artifact unchanged
```

A different file produces a different hash.

---

### Hash Pinning

Referencing or validating an artifact using its expected cryptographic hash.

This helps prevent silently replacing one artifact with another.

---

### Hidden Context

Information available to the model but not normally displayed to the end user.

It may include:

- system prompts
- developer instructions
- RAG policies
- tool schemas
- workflow rules
- profile context

**Hidden ≠ secret.**

---

## I

### Immutable Reference

A reference that always identifies the exact same artifact.

Example:

```text
sha256:abc123...
```

Unlike mutable references such as:

```text
latest
```

---

### Improper Output Handling

Unsafe use of LLM-generated output before it is passed to another component or system.

```text
LLM → shell
LLM → SQL
LLM → browser
LLM → filesystem
LLM → tool
```

Model output should be treated as untrusted input.

---

### Incorrect State Inference

A failure where a model assumes that a system condition is true without verifying the real state.

Example:

```text
LLM: payment = confirmed

Actual system:
payment = pending
```

Inferred state ≠ verified state.

---

### Inference

The stage where a trained model receives an input and generates a prediction or output.

```text
Input → Model → Output
```

---

### Inference Endpoint

A network endpoint or API through which applications send inputs to a deployed model and receive inference results.

---

### Integrity

The assurance that data or an artifact has not been changed or tampered with unexpectedly.

In supply-chain security:

> Is this still the exact artifact I expected?

---

## L

### Label Poisoning

A type of data poisoning where examples are intentionally or accidentally assigned incorrect labels so the model learns wrong patterns.

---

### Lineage

The history of how data or an artifact moved and changed through a pipeline, including transformations, versions and dependencies.

---

### Log-Probabilities

The logarithms of token probabilities produced by a model. They provide more detailed information about how likely different outputs are.

---

### Logits

Raw numerical scores produced by a model before they are converted into probabilities.

---

### LoRA — Low-Rank Adaptation

A PEFT technique that adds small trainable matrices to a frozen base model.

Instead of retraining all model parameters, LoRA trains a much smaller number of parameters.

```text
Base Model
   +
LoRA
   ↓
Adapted Model
```

---

## M

### Membership Inference

An attack that tries to determine whether a specific piece of data exists in a dataset or index without necessarily retrieving its contents.

In vector systems, similarity scores, timing, or response patterns may reveal membership.

---

### Misattributed Evidence

Real or fabricated information incorrectly attributed to the wrong source, document, person, or authority.

---

### Misinformation

Incorrect, incomplete, unsupported, or misleading information produced by an AI system that may influence a human decision or automated action.

The primary risk is not only generating incorrect information, but having that information trusted and acted upon.

---

### Model Card

Documentation describing a model.

It may contain:

- intended use
- limitations
- training information
- evaluation results
- licensing information

However:

> **Model Card ≠ proof of origin**

---

### Model Extraction

Repeatedly querying a model to collect enough information to approximate, reproduce or imitate its behavior.

---

### Model Poisoning

Manipulation of a model or its learning process to introduce harmful, biased or attacker-controlled behavior.

---

### Model Provenance

The traceable history and origin of a model.

It may describe:

- who created it
- the base model
- datasets used
- fine-tuning
- transformations
- versions
- ownership

---

### Multimodal

A system capable of processing more than one type of data, such as text, images, audio or video.

---

### Mutable Reference

A reference whose target may change over time.

Example:

```text
model:latest
```

Today it may point to one artifact and later point to another.

---

## O

### Omission Failure

A failure caused by leaving out information that is necessary for a correct decision.

Examples:

- missing exceptions
- missing risks
- missing deadlines
- missing conditions
- missing timestamps

The remaining information may appear correct while still being misleading.

---

### Output Budget

The maximum amount of output a model is allowed to generate for a request.

---

### Output Encoding

Transforming output so special characters are interpreted safely as data instead of executable code or markup.

Example:

```text
<script>
```

may be encoded for HTML so the browser displays it as text rather than executing it.

---

### Overreliance

Excessive trust in AI-generated output.

It often occurs because fluent, confident, or well-structured responses appear authoritative.

**Fluency ≠ correctness. Confidence ≠ evidence.**

---

## P

### Parameterized Query

A database query where data values are supplied separately from the SQL command structure.

Instead of constructing SQL using model-generated strings:

```text
SQL + arbitrary value
```

the SQL structure remains fixed and values are treated as data. This reduces SQL injection risk.

---

### Path Traversal

A vulnerability where an attacker manipulates a file path to access files outside the intended directory.

Common pattern:

```text
../../
```

LLM-generated file paths must be validated before filesystem access.

---

### PEFT — Parameter-Efficient Fine-Tuning

Fine-tuning techniques that update only a small portion of model parameters instead of retraining the entire model.

Benefits include:

- less memory
- lower compute cost
- faster training
- smaller artifacts

LoRA is one example of PEFT.

---

### Poisoning

The intentional manipulation of training data, models or other AI components to influence future model behavior.

Examples:

- training data poisoning
- model poisoning
- embedding poisoning

---

### Pre-Flight Token Estimation

Estimating token usage and expected cost before sending a request to the model, allowing overly expensive requests to be rejected early.

---

### Prepared Statement

A predefined database query structure where parameters are supplied separately from SQL syntax.

Prepared statements help prevent untrusted data from becoming executable SQL.

---

### Privilege Separation

A security principle that separates tasks and components according to the privileges they require.

A component should not automatically inherit access to capabilities that are unnecessary for its task.

---

### Probing

Repeatedly interacting with a system to discover:

- hidden behavior
- internal rules
- limits
- permissions
- available tools
- potential weaknesses

---

### Provenance

The origin and history of an artifact.

It answers questions such as:

- Where did it come from?
- Who created it?
- What transformations were applied?
- Was it modified?
- Which version is this?

**PT:** proveniência / rastreabilidade de origem.

---

## Q

### Quantization

A technique that reduces the numerical precision of model weights to reduce memory usage and computational cost.

Example:

```text
FP16 → INT8 → INT4
```

The quantized model is a new artifact and should be evaluated independently.

---

### Queue

A collection of actions or tasks waiting to be executed.

---

### Quota

A predefined limit on resource consumption, such as requests, tokens, compute, storage or cost.

---

## R

### RAG — Retrieval-Augmented Generation

An architecture where external information is retrieved and provided to the model as context before it generates an answer.

---

### RAG Poisoning

Manipulation of a RAG knowledge base so malicious or misleading content is retrieved and influences model outputs.

---

### Rate Limiting

Restricting how frequently a user, application or source can perform actions or send requests within a defined period.

---

### RCE — Remote Code Execution

A vulnerability that allows an attacker to cause arbitrary code or commands to execute on another system.

In LLM applications this may happen when model output is passed directly to:

- shell commands
- `exec`
- `eval`
- unsafe interpreters

---

### Reasoning Loop

A situation where a reasoning model repeatedly processes the same or related steps without reaching a useful termination state.

---

### Recursion Depth

The number of nested recursive calls or agent/sub-agent levels currently active.

---

### Red Teaming

Adversarial testing of a system to identify vulnerabilities, unsafe behaviors and possible attack paths before real attackers exploit them.

---

### Resource Allocation

The process of assigning and limiting compute, memory, tokens or other resources among users, requests or workloads.

---

### Resource Exhaustion

A condition where resources such as GPU, CPU, memory, tokens, connections or API quota are consumed until service performance degrades or fails.

---

### Retrieval Jamming

An availability attack against a retrieval system where specially crafted content interferes with useful retrieval.

```text
Query
  ↓
Blocker Document
  ↓
Bad Retrieval
  ↓
Refusal / Missing Answer
```

Unlike prompt injection, the retrieved content does not necessarily contain malicious instructions.

---

### Reverse Engineering

The process of studying a system's behavior, structure, or outputs to infer how its internal mechanisms work.

In AI security, this may be used to infer:

- refusal rules
- hidden instructions
- thresholds
- tools
- workflows

---

### RLHF — Reinforcement Learning from Human Feedback

A training technique that uses human preferences or feedback as a signal to shape model behavior.

---

### Runtime Verification

Checking conditions and system state at the moment an action is about to execute.

Used especially for high-impact actions.

```text
LLM proposes action
        ↓
Runtime Check
        ↓
Allow / Reject
```

---

## S

### Sandbox / Sandboxing

An isolated environment that restricts what a model, agent or untrusted component can access or execute.

---

### Sanitization

Removing, modifying, or neutralizing potentially dangerous content before it reaches another component.

Examples include removing:

- dangerous HTML
- control characters
- unsafe URLs
- unexpected markup

Validation asks whether something is allowed. Sanitization makes dangerous content safer.

---

### SBOM — Software Bill of Materials

An inventory of software components and dependencies used by an application.

It may contain:

- package names
- versions
- dependencies
- licenses
- vulnerability information

**Think:** software ingredients list.

---

### Security Boundary

A boundary where security controls determine whether access or an action is allowed.

System prompts and hidden instructions should not be treated as security boundaries.

---

### Semantic Cache

A cache that uses semantic similarity rather than exact matching to reuse previous results.

```text
New Query
   ↓
Embedding Similarity
   ↓
Similar Cached Query?
   ↓
Reuse Response
```

Its similarity threshold can become an attack surface.

---

### Serialization

The process of converting an object or model into a format that can be stored or transferred.

Some serialization formats may execute code while loading.

Example:

```text
Python pickle
```

---

### Similarity Score

A numerical measurement representing how similar two vectors are.

Similarity scores are commonly used to rank retrieval results.

Exposing raw scores may enable information leakage or membership inference.

---

### Sleeper Agent

A model containing hidden behavior that stays dormant until a specific trigger or condition activates it.

---

### Slopsquatting

A supply-chain attack where an AI coding assistant suggests a plausible but nonexistent package name and an attacker registers that package with malicious code.

```text
LLM invents package
        ↓
Attacker registers it
        ↓
Developer installs it
```

---

### Special Token

A token with structural or control meaning to a model, such as tokens representing system, user, assistant or end-of-sequence boundaries.

---

### Sponge Example

An adversarial input intentionally optimized to cause unusually high computational resource consumption.

---

### State Hashing

Generating hashes from agent states so repeated states can be detected, helping identify loops or repeated execution patterns.

---

### State Inference

The process of estimating or reasoning about the current state of a system from available information instead of reading that state directly from an authoritative source.

---

### Supply Chain

All components, suppliers and transformations a system depends on during development, training, deployment and execution.

For AI systems this can include:

- code
- models
- datasets
- packages
- adapters
- pipelines
- infrastructure
- devices

**Simple definition:**

> If the system depends on it, it is part of the supply chain.

---

### System Prompt

High-level instructions supplied to a model by the application to define its role, behavior, constraints, or context.

A system prompt can influence behavior but should not be treated as:

- secure storage
- authentication
- authorization
- deterministic policy enforcement

---

## T

### Tampering

Unauthorized or malicious modification of a component, file, model or artifact.

**PT:** adulteração.

---

### T&Cs — Terms and Conditions

The contractual terms that define how a product or service can be used.

For AI providers, they may define:

- data retention
- training usage
- privacy
- ownership
- commercial use

---

### Tenant

A customer, organization, workspace, or isolated group sharing the same underlying application infrastructure.

A multi-tenant system serves multiple tenants while attempting to keep their data and permissions isolated.

---

### Thinking Tokens

Tokens or computational budget used internally by reasoning models while working through a problem before producing the visible response.

---

### Third Party

A person, organization, service or component external to the team or company building the system.

Examples:

- external model
- external API
- open-source package
- external dataset

**Simple definition:**

> Something external that your system depends on.

---

### Threshold

A predefined boundary used to make a decision.

Example:

```text
similarity >= 0.85 → match
similarity < 0.85  → no match
```

Thresholds are common in retrieval, semantic caches, classifiers, and security controls.

---

### Token Budget

The maximum number of tokens allowed or allocated for input, output, reasoning or an entire execution.

---

### Tool Schema

A structured description of a tool exposed to an LLM or agent.

It may reveal:

- tool capabilities
- accepted arguments
- required parameters
- internal functionality

Tool schemas describe capability; they should not determine authorization.

---

### Tool-Calling Loop

A condition where an agent repeatedly invokes tools without reaching a valid end state.

---

### Trigger

A specific input, phrase, token pattern or condition that activates hidden or backdoored behavior.

---

### Trust Boundary

A boundary between components, users or data sources with different levels of trust. Crossing it should normally require validation or additional controls.

---

### Trust Tier

A classification representing how much a data source or component is trusted.

Example:

```text
Tier 1 → internal verified data
Tier 2 → trusted partner data
Tier 3 → external / untrusted web data
```

Different trust tiers may require separate indexes or security controls.

---

## V

### Validation

Checking whether input or output conforms to expected rules before it is accepted or used.

Examples:

- correct type
- allowed values
- expected schema
- valid range
- permitted action

Validation does not necessarily remove dangerous content; that is the role of sanitization.

---

### Vector Database

A database designed to store and search vector representations such as embeddings.

It commonly supports nearest-neighbor or similarity search and is frequently used in:

- RAG
- semantic search
- agent memory
- recommendation systems

---

### Vet / Vet a Supplier

To carefully evaluate a supplier before trusting or using its products or services.

This may include checking:

- reputation
- security practices
- privacy policy
- T&Cs
- data handling
- artifact provenance

**PT:** avaliar / verificar cuidadosamente um fornecedor.

---

## X

### XSS — Cross-Site Scripting

A web vulnerability where attacker-controlled content causes JavaScript or other active content to execute in another user's browser.

In LLM applications, XSS may occur when generated HTML, Markdown, or JavaScript is rendered without proper sanitization and output encoding.

---

## Z

### Zero Trust

A security principle based on not automatically trusting a user, component, network, or model output.

Every access or action should be explicitly verified based on identity, permissions, context, and policy.

For LLM applications: treat model output as untrusted input.

---

## Key Distinctions

### Signed ≠ Safe

A valid digital signature can prove:

- origin
- integrity

It does **not** prove that the model behaves safely.

---

### Safe Format ≠ Safe Model

A secure serialization format reduces some technical risks but does not guarantee that the model itself has no:

- backdoors
- bias
- poisoned behavior

---

### Provenance vs Integrity

**Provenance**

> Where did this artifact come from?

**Integrity**

> Has this artifact changed since it was created or approved?

---

### Supply Chain vs Poisoning

**Poisoning** focuses on malicious manipulation of the model or data.

**Supply Chain** focuses on how a compromised component entered or propagated through the system.

The same incident may involve both.
