# Behavioral UX Psychology

Persuasion and conversion are not "copy problems" bolted on at the end. They are **structural** — they live in defaults, step order, progress state, framing, and adjacency. This reference makes behavioral design a first-class mechanic, alongside the design dials.

> **Ethics guardrail (non-negotiable).** These principles reduce friction and reveal value. They must NOT be used to deceive, trap, or manufacture false urgency. No fake scarcity, no fabricated deadlines, no losses the user won't actually incur, no pre-checked consent/marketing opt-ins, no roach-motel cancellation. If a technique only works because the user is misled, it is a dark pattern — do not build it. Every "loss" you show must be real; every default you set must be genuinely the best choice for most users.

---

## The Six Core Principles

Each lists **the mechanism**, **how it shows up in code**, and **the trap** (the dark-pattern version to avoid).

### 1. Smart Defaults — beats decision fatigue
Blank forms force a decision on every field and drive abandonment. A pre-selected option reads as a trusted recommendation.

- **In code:** never ship a fully blank form. Set `defaultValue` / `selected` / `checked` on the most common choice; auto-fill today's date, detected locale/currency/timezone, the modal plan most users pick. Pre-fill what you can infer (email from SSO, name from account).
- **Trap:** pre-selecting the *expensive* option or a pre-checked marketing/consent box. Default to what serves the user, not what serves the invoice.

### 2. Goal Gradient Effect — momentum toward a finish line
The closer a finish line feels, the faster people move. Starting at 0% is deflating.

- **In code:** progress bars / steppers / onboarding checklists **never start empty**. Credit steps already done ("Account created ✓") so the user opens at 20–30%. Show `n of N`, not just a percentage. Order steps easy→hard so early wins accumulate.
- **Trap:** faking progress the user didn't make, or a bar that jumps backward. Momentum must be earned and monotonic.

### 3. Reciprocity — value before the ask
Give something useful for free and people feel a pull to reciprocate (an email, a signup).

- **In code:** let the user reach the core value **before** any wall. They run the tool, get a partial result (an SEO score, a generated draft, a preview), *then* the signup/paywall appears to **save / download / unlock the full** result. The gate guards persistence, not access.
- **Trap:** a `<SignUpModal>` that blocks the first interaction. Gate before value = friction, not reciprocity.

### 4. Endowment / IKEA Effect — ownership through investment
People overvalue what they helped build and resist abandoning it.

- **In code:** **reverse the onboarding.** Customization wizard first (avatar, theme, username, workspace name), held in `localStorage`/state. The final button says **"Continue"**, not "Sign Up" — email/password come *after* they've built something they don't want to lose. Persist the work-in-progress so a refresh never wipes it.
- **Trap:** collecting the investment then destroying it if they don't convert. Their work survives whether or not they sign up today.

### 5. Loss Aversion — protecting what you have
The pain of losing outweighs the pleasure of an equivalent gain (~2×). People protect the status quo.

- **In code:** frame around what's **at risk**, not just what's gained. "Storage full — 12 files will be archived in 3 days. Upgrade to keep them" reads stronger than "Upgrade for more storage." Use a warning state (amber, not alarmist red-for-red's-sake) and show the concrete thing at stake.
- **Trap:** manufacturing losses that won't happen (files that were never going to be deleted, countdown timers that reset). The loss must be **real and reversible by the user's action** — otherwise it's a threat.

### 6. Contrast / Anchoring — numbers judged by their neighbors
The brain evaluates a price against the numbers next to it, not in isolation.

- **In code:** never show a cost alone. In pricing tables, place the target plan beside a higher anchor (annual vs monthly, or a struck-through "was"). For upsells, express the add-on relative to the cart ("$50 — just 2.6% of your order"). Order tiers so the intended pick sits next to a pricier one (decoy/asymmetric-dominance layout).
- **Trap:** fake "was" prices that were never charged, or phantom decoys that don't exist. Anchors must be genuine comparisons.

---

## Two more worth knowing

- **Social Proof** — "2,847 gyms onboarded this month", real logos, recent-activity toasts. Only ever with true numbers. Placed near the decision point (next to the CTA, not buried in a footer).
- **Hick's Law** — every added choice slows the decision. Collapse long option lists behind progressive disclosure; surface 3–5 primary choices, advanced behind "More options." Pairs with Smart Defaults: fewer visible choices *and* a good default.

---

## How to apply during a build

1. **Name the primary conversion action** for the surface (sign up, upgrade, complete onboarding, add to cart). One per surface.
2. **Pick the 1–3 principles that fit** — don't stack all six on one screen; that reads as manipulation and creates noise.
   | Surface | Highest-leverage principles |
   |---------|------------------------------|
   | Onboarding flow | Goal Gradient + Endowment + Smart Defaults |
   | Forms / setup | Smart Defaults + Hick's Law |
   | Landing / signup | Reciprocity + Social Proof |
   | Pricing / checkout / upsell | Contrast/Anchoring + Loss Aversion |
   | Retention / upgrade prompts | Loss Aversion + Social Proof |
3. **Make it structural, not cosmetic** — the win is in step order, default state, and what's gated, not in a banner color. Bake it into the component logic and state.
4. **Run the ethics guardrail** on each one before shipping (see top). If it only works by misleading, cut it.

## Prompt-role primer (for briefing a build)

> *"Act as an expert frontend developer and behavioral UX designer. Apply the **Endowment Effect** — let the user customize their dashboard before any email ask — and the **Goal Gradient Effect** — start the progress bar at 25%. Keep every 'loss' and every social-proof number real."*
