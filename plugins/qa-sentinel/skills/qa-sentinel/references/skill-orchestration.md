# Skill Orchestration Map

Declarative mapping of each perspective to its preferred skill chain, with explicit fallbacks for when a skill is not available in the calling session.

## Availability rule

1. Check the session's actual available-skills list (the harness lists invocable skills in context; a skill present in a repo checkout is NOT necessarily invocable — repo presence never drives availability decisions).
2. Use the first available skill from the perspective's `preferred_chain` below.
3. None available → use the fallback primitive and mark the verifier's output `using_fallback: true` so the verdict flags the lower-fidelity evaluation.

## Mapping

### Designer

```yaml
preferred_chain:
  - premium-web-design       # invoke audit mode for technical + design rubric
  - premium-web-design     # AI-slop checklist + 3-second comprehension test
fallback:
  - tool: agent-browser    # screenshot desktop + mobile, then apply rubric
  - rubric_file: references/lenses/designer.md  # inline checklist
require_artifacts:
  - desktop_screenshot.png
  - mobile_screenshot.png
```

### SEO

```yaml
preferred_chain:
  - <a crawler skill>      # crawl, response codes, schema, hreflang
  - agent-browser          # for raw vs rendered HTML diff
fallback:
  - tool: verify_independent.sh    # curl + grep + manual rubric
  - rubric_file: references/lenses/seo.md
require_artifacts:
  - rendered_html_sample.html
  - raw_html_sample.html
  - crawl_summary.json     # if a crawler skill is available
```

### Business / Conversion

```yaml
preferred_chain:
  - premium-web-design     # 3-second comprehension test, value-prop clarity
  - <a copywriting skill>   # CTA and persuasion frameworks
fallback:
  - rubric_file: references/lenses/business-conversion.md
require_artifacts:
  - cta_inventory.md
  - hero_screenshot.png
```

### Product Manager

```yaml
preferred_chain:
  - agent-browser          # workflow replay end-to-end
fallback:
  - tool: verify_independent.sh
  - rubric_file: references/lenses/product-manager.md
ground_truth_inputs:
  - workflow_discovery_output    # from /qa plan
  - prd_or_spec_files
require_artifacts:
  - workflow_replay_log.md
```

### Developer

```yaml
preferred_chain:
  - agent-browser          # console + network panels
fallback:
  - tool: verify_independent.sh    # curl + grep + log triage
  - rubric_file: references/lenses/developer.md
require_artifacts:
  - console_errors.txt
  - network_errors.txt
  - server_log_excerpt.txt    # if applicable
```

### Content / Copy

```yaml
preferred_chain:
  - <a copywriting skill>   # tone, persuasion, microcopy
fallback:
  - rubric_file: references/lenses/content-copy.md
ground_truth_inputs:
  - copy_decks_if_available
  - translation_files_if_available
require_artifacts:
  - copy_extract.md
  - translation_diff.md    # for bilingual targets
```

### Accessibility

```yaml
preferred_chain:
  - premium-web-design       # audit mode, accessibility section
  - agent-browser          # axe-core injection + keyboard simulation
fallback:
  - rubric_file: references/lenses/accessibility.md
require_artifacts:
  - a11y_findings.json
  - keyboard_nav_log.md
```

### Performance

```yaml
preferred_chain:
  - premium-web-design       # audit mode, performance section
  - dev-front-system       # --perf mode (deeper)
  - agent-browser          # timing API + Lighthouse if available
fallback:
  - tool: agent-browser
  - rubric_file: references/lenses/performance.md
require_artifacts:
  - lcp_fid_cls.json
  - bundle_size_report.md
```

### Code Architect (Senior CTO)

```yaml
preferred_chain:
  - simplify                       # reuse + quality + efficiency review
  - improve-codebase-architecture  # architectural friction detection
  - security-review                # security check on pending changes
  - review                         # generic PR review
fallback:
  - tool: git_diff_scan
  - rubric_file: references/lenses/code-architect.md
require_artifacts:
  - diff_summary.md
  - elegance_findings.md
  - security_findings.md
hard_rule: |
  Simple and elegant only, with pattern reuse.
  Over-engineered, premature-abstraction, or pattern-duplicating proposals
  fail the lens regardless of whether they "work".
```

## Fallback semantics

When a lens uses a fallback:

- The lens still produces the same structured-finding schema
- The lens report carries `fallback_used: true`
- `evidence_path` points to artifacts produced by the fallback (e.g., screenshot from `agent-browser`)
- The final aggregated report surfaces a "lower-fidelity evaluation" notice naming which lenses fell back

When ALL preferred skills are missing AND no fallback artifact can be produced (e.g., `agent-browser` itself is unavailable and the target is a live URL), the lens returns:

```json
{
  "lens": "<name>",
  "status": "skipped",
  "reason": "no_executable_chain",
  "fallback_used": true
}
```

The aggregator counts skipped lenses against coverage but does NOT block the run. The final report flags coverage gaps explicitly.

## Hard requirements (won't run without these)

- **agent-browser** must be available to evaluate any rendered output. Without it, only static-file analysis is possible. Run will warn but proceed with reduced coverage.
- **handoff** must be available for terminal-failure escalation. If absent, the report is saved to `tmp/qa-sentinel/<run-id>/report.md` only.

## Updating this map

When new skills are added to your skills repo that fit one of the lenses, append them to the preferred chain (never replace; preserve order). Newer skills go at the head of the chain only if they strictly supersede the older one (e.g., a newer design skill supersedes an older one for technical audit but not for the AI-slop checklist).
