# Task Modes for Deep Dive

How the generic recursive algorithm adapts its decomposition, processing, and quality metrics for different task types. Each mode can optionally be backed by a sub-skill that provides templates and domain-specific configuration.

---

## PRD/Spec Writing

- **Decomposition:** By PRD section (Problem, Solution, Implementation, etc.)
- **Source mapping:** Each source feeds specific sections based on content type
- **Quality metric:** Concept coverage >= 85%, source fidelity >= 4/5
- **Sub-skill:** `deep-dive-prd` (provides section templates and quality rubric)

## Research Synthesis

- **Decomposition:** By source document first, then by theme
- **Processing:** Extract findings per source, then cluster by theme across sources
- **Quality metric:** All sources represented, contradictions surfaced

## Document Analysis

- **Decomposition:** By document section/chapter
- **Processing:** Analyze each section independently with full attention
- **Quality metric:** Every section covered, cross-references identified

## Code Review

- **Decomposition:** By file or module
- **Processing:** Review each file with relevant context (deps, tests, docs)
- **Quality metric:** All files reviewed, inter-module issues caught

## Email Processing

- **Decomposition:** By email or thread
- **Processing:** Each email gets CRM lookup + thread context
- **Quality metric:** Every email classified, no skipped items

## Sales Research

- **Decomposition:** By data source (CRM, web, email, social)
- **Processing:** Each source analyzed independently, then cross-referenced
- **Quality metric:** All sources cited, contradictions flagged
