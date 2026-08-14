# unknown-collapsed-to-default

## Description
A missing, null or empty value is rendered or branched on as a confident one. Absent config reads as `false`, no data as `0`, an empty allow-list as "everything permitted", a null cost as `$0.00`. Binary assertions pass because the value is present and well-typed; it is simply not the answer.

Three states get collapsed into two: "we cannot tell", "no", and "none" are different facts.

## Symptoms
- A total, count or currency showing `0` where nothing has been measured yet
- An empty collection described as unrestricted, complete, clean or passing
- A default applied when a field is absent, indistinguishable from the same value chosen deliberately
- A newer client reading an older server: a field the payload does not carry treated as `false`
- Explanatory copy that asserts a cause nobody checked ("none found", "not applicable")

## Root cause
Falsy-coalescing at the boundary — `value || default`, `int(x or 0)`, `dict.get(k, False)` — applied where absence is meaningful. The default is chosen for rendering convenience, not because it is true.

## Independent verification
For each displayed or branched-on value, remove its source and check the system says it does not know, rather than printing a default. Test the three states separately: unset, empty, and zero. Where a client reads a server field, drop the field and confirm the client degrades to "unknown", not to "no".

## Common fix attempts that DON'T work
- Changing the default (still a default where the answer is unknown)
- Adding the caveat only to the tooltip while the number still reads as fact
- Fixing the one surface that was reported, leaving siblings that coalesce identically

The fix that works: carry the unknown through to the render and say so, and keep null distinct from zero at every layer.

## Likely lenses
developer, code-architect, product-manager
