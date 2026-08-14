# PRD Quality Rubric

Scoring criteria for the concept audit phase. Use this rubric to evaluate PRD drafts and determine whether a section needs another recursion pass or is ready for finalization.

---

## Dimension 1: Concept Coverage

**Definition:** The percentage of distinct concepts, facts, and requirements present in the source materials that appear (explicitly or by clear implication) in the PRD output.

**How to measure:** Extract a concept inventory from source materials during Phase 1. After drafting, check each concept against the PRD. Coverage = (concepts present / total concepts) x 100.

| Score | Description |
|-------|-------------|
| 0-20% | Most source material is missing. The PRD reads like it was written without the sources. |
| 21-40% | Major themes are present but significant details, constraints, and supporting data are absent. |
| 41-60% | Core concepts are covered. Secondary details and edge cases have gaps. A reader familiar with the sources would notice omissions. |
| 61-80% | Strong coverage. Most concepts are represented. Only minor details or low-priority items are missing. |
| 81-100% | Near-complete coverage. All significant concepts, data points, and requirements from sources appear in the PRD. Omissions are intentional and noted. |

**Minimum acceptable score:** 80%

If coverage falls below 80%, trigger a targeted recursion pass on the missing concepts before finalizing.

---

## Dimension 2: Depth Score

**Definition:** The average number of supporting details (evidence, examples, specifications, rationale) provided per key concept in the PRD.

**How to measure:** For each key concept, count the supporting elements: data points, examples, technical specs, citations, rationale statements, or constraints. Average across all key concepts.

| Score | Description |
|-------|-------------|
| 1 | **Surface-level.** Concepts are named but not explained. No supporting evidence or specifications. Reads like a bullet-point brainstorm. |
| 2 | **Thin.** Brief explanations exist but lack specifics. A reader would need to consult original sources to understand the details. |
| 3 | **Adequate.** Each concept has 1-2 supporting details. An informed reader can follow the logic, but an uninformed reader may have questions. |
| 4 | **Solid.** Each concept has 2-3 supporting details including rationale, specs, or data. An engineer could begin planning from this section. |
| 5 | **Comprehensive.** Each concept is fully elaborated with evidence, specifications, edge cases, and rationale. The section stands alone without needing to consult sources. |

**Minimum acceptable score:** 3

Sections scoring below 3 should be flagged for a depth-expansion recursion pass.

---

## Dimension 3: Cross-Reference Density

**Definition:** The count of meaningful inter-section references within the PRD - places where one section explicitly calls out a relationship to another section's content.

**How to measure:** Count each instance where a section references content in another section (e.g., "as described in the Data Model section," "this connects to the risk identified in Section 11," "per the success criteria defined above"). Only count references that add clarity - not filler cross-links.

| Score | Description |
|-------|-------------|
| 0-2 | **Isolated.** Sections read as independent documents. Contradictions or redundancies may exist undetected. |
| 3-5 | **Lightly connected.** A few obvious connections are noted but many implicit relationships are left for the reader to infer. |
| 6-10 | **Well-connected.** Most important relationships between sections are made explicit. The PRD reads as a coherent whole. |
| 11+ | **Densely linked.** Sections form a tight web of references. Dependencies, tradeoffs, and relationships are fully surfaced. |

**Minimum acceptable count:** 5

For PRDs with 8+ sections, fewer than 5 cross-references usually means sections were written in isolation. Run a coherence pass to surface implicit connections.

---

## Dimension 4: Source Fidelity

**Definition:** How accurately the PRD's claims, data points, and technical details match the original source materials. Measures whether the PRD faithfully represents the sources without distortion, fabrication, or unsupported extrapolation.

**How to measure:** Sample 10+ claims from the PRD and trace each back to its source. Score based on accuracy of representation.

| Score | Description |
|-------|-------------|
| 1 | **Unreliable.** Multiple claims cannot be traced to sources. Fabricated details or significant misrepresentations are present. |
| 2 | **Loose.** General themes match sources, but specific numbers, timelines, or technical details are inaccurate or invented. |
| 3 | **Mostly accurate.** Core claims match sources. Minor inaccuracies exist in secondary details. Extrapolations are not clearly marked. |
| 4 | **Faithful.** Claims accurately reflect sources. Extrapolations and assumptions are labeled as such. Data points are correct. |
| 5 | **Rigorous.** Every claim traces to a source or is explicitly marked as an assumption/recommendation. Nuances from sources are preserved. No distortion. |

**Minimum acceptable score:** 4

Source fidelity below 4 is a blocking issue. Any fabricated or distorted claims must be corrected before the PRD can be finalized.

---

## Dimension 5: Actionability

**Definition:** Whether an engineer (or cross-functional team) could pick up this PRD and begin implementation without needing to seek additional clarification on what to build.

**How to measure:** Have someone unfamiliar with the project read the PRD and list every question they would need answered before starting work. Fewer questions = higher actionability.

| Score | Description |
|-------|-------------|
| 1 | **Vague.** The PRD describes a vision but provides no concrete specifications. An engineer would not know where to start. |
| 2 | **Directional.** High-level approach is clear, but technical details, acceptance criteria, and scope boundaries are missing. Significant back-and-forth would be needed. |
| 3 | **Workable.** An experienced engineer could begin work but would need to make assumptions about edge cases, error handling, and integration details. |
| 4 | **Clear.** Specifications are detailed enough to estimate and plan sprints. Most edge cases are addressed. Open items are explicitly called out. |
| 5 | **Implementation-ready.** An engineer could write code directly from this PRD. Acceptance criteria, error states, data formats, and integration contracts are all specified. |

**Minimum acceptable score:** 3

For Technical PRDs and Research-to-Engineering PRDs, the target should be 4+. For Product PRDs (which will go through design iteration), 3 is acceptable.

---

## Composite Scoring

### Overall PRD Quality Score

Calculate the composite score as a weighted average:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Concept Coverage | 30% | A PRD that misses source concepts fails its primary purpose |
| Depth Score | 20% | Depth separates useful PRDs from shallow summaries |
| Cross-Reference Density | 10% | Coherence matters but is fixable in a quick pass |
| Source Fidelity | 25% | Incorrect information is worse than missing information |
| Actionability | 15% | The PRD must ultimately drive implementation |

### Quality Gates

| Gate | Criteria | Action |
|------|----------|--------|
| **Pass** | All dimensions meet minimums AND composite >= 75% | PRD is ready for review |
| **Conditional Pass** | One dimension below minimum by 1 point, composite >= 65% | Flag the weak dimension, note it in Open Questions, proceed to review |
| **Fail - Targeted Fix** | One dimension significantly below minimum | Run a focused recursion pass on the failing dimension only |
| **Fail - Major Rework** | Two or more dimensions below minimum | Re-enter the recursive pipeline from Phase 2 (section drafting) |

### Audit Output Format

After scoring, produce an audit summary in this format:

```
## Concept Audit Results

| Dimension              | Score   | Minimum | Status |
|------------------------|---------|---------|--------|
| Concept Coverage       | ___%    | 80%     | PASS/FAIL |
| Depth Score            | __/5    | 3       | PASS/FAIL |
| Cross-Reference Density| __ refs | 5       | PASS/FAIL |
| Source Fidelity        | __/5    | 4       | PASS/FAIL |
| Actionability          | __/5    | 3       | PASS/FAIL |

**Composite Score:** ___%
**Gate Decision:** PASS / CONDITIONAL PASS / FAIL

### Action Items (if any)
- [ ] ...
```
