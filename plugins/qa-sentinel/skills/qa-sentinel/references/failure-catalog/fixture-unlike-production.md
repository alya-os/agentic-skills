# fixture-unlike-production

## Description
A test passes because its fixture is a degenerate form of the real input: plain strings where production supplies objects or closures, a hand-built binary payload with an invented length field, one flat record where the real shape is nested, an empty database where production has a million rows. The suite is green and demonstrates nothing about the code under test.

Matters most when a build agent offers "all tests pass" as evidence of done.

## Symptoms
- Fixtures literal-typed by hand where the system builds them through a loader, factory or config parser
- A test that would still pass if the function under test returned early
- Assertions on shape ("the key exists") rather than on behaviour
- Green tests beside a defect that any real input would have exposed
- Fixtures with no counterpart in the trace, database or logs

## Root cause
The fixture is written from a mental model of the input rather than from the input. It is easier to type a string than to construct the real object, and nothing forces the two to agree.

## Independent verification
Build one fixture from the real source: the config loader, the factory, or a payload captured from a live run. Assert the fixture is not the degenerate type. Then mutate the code under test to be obviously wrong and confirm the test fails — a test that passes both ways is measuring nothing.

## Common fix attempts that DON'T work
- Adding more assertions to the same synthetic fixture
- Widening the code to accept the fixture's shape as well as the real one
- Mocking the loader, which reintroduces the invented shape one layer up

The fix that works: derive fixtures from production shapes, and keep one end-to-end case that uses no fixture at all.

## Likely lenses
developer, code-architect

