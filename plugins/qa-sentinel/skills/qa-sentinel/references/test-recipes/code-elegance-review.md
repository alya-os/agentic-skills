# Recipe: code-elegance-review

The senior-CTO simple-and-elegant pass. Drives the Code Architect lens. Hard rule: working code that is over-engineered, prematurely abstracted, or duplicates an existing pattern fails this recipe regardless of correctness.

## Inputs

- `diff`: the code change under review (git diff, or the patch the build agent applied)
- `repo_root`: for grep-based pattern-reuse checks

## Steps

1. **Pattern-reuse grep** - for each new function, class, helper, or utility introduced by the diff, grep `repo_root` for similar names, signatures, or behaviors. If a similar primitive already exists, the new code duplicates it (finding: `multilayer-bug-class` precursor).
2. **Abstraction check** - for any new "framework", "engine", "system", "factory", "builder" pattern: count concrete consumers. If only one consumer, premature abstraction (finding: `regression-silent-failure` for architecture).
3. **Defensive-overuse scan** - count try/catch blocks, null-checks, validation calls. If more than 30% of new lines are defensive code without a documented threat model, finding (`false-positive-generator` precursor: defensive code that flags non-issues).
4. **State leak scan** - search the diff for module-level mutable state, new singletons, new globals. Any without justification is a finding.
5. **Dependency check** - search the diff for new `import` / `require` statements adding new dependencies. For each new dep, ask: could existing code or stdlib have done this in <30 LOC? If yes, finding.
6. **Naming pass** - function names describe results, not methods; variables are nouns; booleans use `is`/`has`/`should`. Flag obscure abbreviations.
7. **Test alignment** - if the change has tests, verify tests use strong assertions (not `expect(thing).toBeDefined()`). Verify no tests were commented out. Verify new behavior has at least one test.
8. **Skill delegation** (when available):
   - Run `simplify` and ingest its findings as primary input
   - Run `improve-codebase-architecture` for friction signals
   - Run `security-review` for security-impacting changes
   - Run `review` as a final pass

## Pass criteria

- Zero pattern-reuse misses (every new primitive justified vs existing)
- Zero premature abstractions
- Defensive code under 30% of new lines OR documented threat model
- Zero unjustified new dependencies
- Naming clarity passes
- Tests aligned

## Lenses this recipe feeds

- code-architect (primary; this recipe IS the lens)
