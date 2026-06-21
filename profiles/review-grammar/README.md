# gc.profile.review-grammar

**Governance Commons Review Grammar Profile**  
**Profile ID:** gc.profile.review-grammar  
**Version:** 0.1.0  
**Status:** Draft

## What is gc.profile.review-grammar?

`gc.profile.review-grammar` is a portable Governance Commons profile for making
AI-assisted review commands unambiguous in a development repository.

It defines what commands such as "normalize", "validate", "verify", "trace",
"adversarial audit", "meta-audit", "authority audit", "registry audit", and
"close the loop" mean when a human gives them to an agent.

## What problem does it solve?

AI-assisted repositories drift when common review words are interpreted differently
from session to session. A maintainer may ask for normalization and receive a
rewrite, ask for validation and receive a summary, or ask for an adversarial audit
and receive reassurance.

This profile gives those commands stable meanings and minimum output expectations.

## What it is for

- Multi-repo development portfolios
- AI-assisted software teams
- Repositories using AGENTS.md, CLAUDE.md, Copilot instructions, or `.governance/`
  agent briefings
- Planning, registry, and authority review workflows
- Lightweight gap analysis and gap-closure discipline

## What it is not

- It is not runtime enforcement by itself.
- It is not a legal audit opinion or certification product.
- It does not replace security review, compliance review, or project management.
- It does not make a repo "governed" unless agents actually read and follow it.

## Required adoption files

An adopter repo should include:

```text
docs/REVIEW-GRAMMAR.md
```

At least one active agent instruction file should reference that grammar, such as:

```text
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
.governance/agents.md
```

## Minimum conformance

A conforming repo has:

- a review grammar file
- stable definitions for the required command verbs
- review-order terms that distinguish first-order review, meta-audit, and process audit
- closure states: `open`, `spec-complete`, `release-complete`, `runtime-complete`
- an output contract requiring scope, findings, evidence, validation, and next action
- at least one agent instruction file that points agents to the grammar

## DCP validation

DCP/Governance Kit validates this profile with:

```powershell
./validate-review-grammar.ps1
```

The validator is intentionally lightweight. It checks file presence and required
terms. It does not prove agent behavior.

## eco runtime mapping

eco may later map review sessions to PASS/RunRecord evidence after this profile is
accepted or release-pinned by Governance Commons. Until then, this profile is a
draft portable vocabulary and adoption contract.
