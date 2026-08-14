# fix-not-on-the-path

## Description
The change exists in source and does not execute where it matters. A once-only initialiser, an unreached branch, a long-lived process holding the old code in memory, an unbuilt bundle, a config the running instance never re-read. Source review confirms the fix; the system behaves exactly as before.

Generalises `helper-fn-not-deployed`, which is the deploy-step case of the same failure.

## Symptoms
- A fix verified by reading the diff rather than by observing a changed behaviour
- A daemon, worker or server process older than the commit under test
- Code placed in a function that runs at startup only, or in a branch the path under test never takes
- Behaviour that changes after a restart but not before, with nobody having restarted
- A test asserting the code is present rather than that it ran

## Root cause
"Present" is confused with "executing". The verifier reads the artifact rather than the behaviour, and long-lived processes, build steps and caches all sit between the two.

## Independent verification
Assert the change RAN: a changed value, a log line, an observable difference in output. Confirm the process under test started after the change (compare process start time with commit or file mtime). Where a build step exists, verify the deployed artifact contains the symbol, not just the repository.

## Common fix attempts that DON'T work
- Re-reading the diff and confirming it is correct
- Restarting one process while another still serves the old code
- Asserting the string is in the file, which passes whether or not the line executes

The fix that works: exercise the path, observe the difference, and record which process produced it.

## Likely lenses
developer, code-architect
