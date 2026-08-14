# helper-fn-not-deployed

## Description
Build agent adds a new helper function (or constant, or utility) and verifies it works locally. The deployed bundle does not include the new symbol because the build, deploy, or sync step missed it. Local works, deployed fails silently.

## Symptoms
- Local dev server: feature works
- Deployed target: feature broken or "feature missing"
- `curl <deployed-bundle>.js | grep '<symbol>'` returns nothing
- Console shows `ReferenceError: <symbol> is not defined` on production but not local
- Theme / plugin code on the server is older than the local source

## Root cause
Build / deploy / sync pipeline has a step the agent did not invoke or did not verify. Common causes: forgot to run build, build cache served stale output, file copied to wrong directory, file missing from manifest, file blocked by `.gitignore` / deploy-ignore.

## Independent verification
Fetch the deployed bundle / theme file via a transport tier different from the one used to deploy (SFTP if deploy was REST, REST if deploy was wp-cli). Grep the deployed file for the symbol. If absent, finding confirmed.

For interpreted languages: fetch the deployed source file, diff against local source. Even one byte of difference is the finding.

## Common fix attempts that DON'T work
- Re-running the same deploy command (often produces the same incomplete deploy)
- Clearing browser cache (does not address server-side absence)
- Adding `console.log` on local (works on local; deployed still missing)

The fix that works: run the full build pipeline, verify the symbol is in the build output before deploying, then verify again after deploying.

## Likely lenses
developer, code-architect
