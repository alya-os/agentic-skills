# ui-language-mismatch

## Description
UI chrome (labels, badges, buttons, headings, footers) appears in a language other than the site's declared primary language. Distinct from `tone-inconsistency` (same language, clashing voice) and `translation-semantic-drift` (a translation that says the wrong thing): here the interface string is simply in the wrong language entirely. Most often a stray word copied verbatim from a reference artifact, a sample, or another locale's deliverable that was used as a visual template.

Critically: this is about the INTERFACE, not the data. Content the product is legitimately about (e.g. French-language prompts a brand tracker analyzes, a quoted foreign review) is data and must be left alone. The finding is foreign-language CHROME on a single-language UI.

## Symptoms
- A stray foreign-language label/badge on an otherwise English UI ("Confidentiel" on a "Confidential" site, "Rapport", "Aperçu", "Enregistrer")
- Strings lifted from a reference report/mockup in another language and pasted into a template
- A single page or component in language B while the rest of the app is language A
- Hardcoded foreign strings in templates (not behind the i18n/translation layer, if one exists)

## Root cause
A reference artifact in another language was used as the design/structure template and its literal strings were carried over instead of being localized to the app's primary language. Or copy authored by someone working in a different default language. No "primary UI language" assertion in the build checklist.

## Independent verification
Establish the site's primary UI language first (declared in config, `<html lang>`, or stated in the brief — e.g. "English-only"). Then grep the rendered templates/output for chrome strings NOT in that language. Exclude data fields (anything bound from user/analysis content: `{{ }}` interpolations, stored records). A fast sweep: search templates for a vocabulary list of the suspected other language's common UI words. Any hardcoded hit in chrome is the finding.

## Common fix attempts that DON'T work
- Translating the one word you noticed while missing its siblings elsewhere (sweep the whole codebase, not just the reported instance)
- "Translating" data that is legitimately foreign-language (breaks the actual feature)
- Assuming one occurrence — strings copied from a reference usually arrive in clusters (header + footer + badge)

The fix that works: assert the primary UI language, sweep all chrome strings against it, convert every foreign chrome string, and explicitly leave data untouched.

## Likely lenses
content-copy, designer
