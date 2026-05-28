# studfinderapp.com HUMAN-action backlog (handoff doc)

> Active blockers requiring an out-of-band human action — anything the autonomous dev cycle cannot perform from inside its own iteration. **NOT** for deferred work (use `docs/FUTURE-WORK.md`), and **NOT** for acceptance tests the dev cycle can't self-verify (also `FUTURE-WORK.md > ## Manual / human verification`). HUMAN.md is the "the cycle is stuck right now, waiting on you" list.
>
> Every skill reads this on start. Top of file is highest urgency; within each section, newest-first.

## Blocking

- [ ] H1.1 [easy] **Sign up for Amazon Associates (US account + Earn Globally + OneLink)**
  Sign up once at affiliate-program.amazon.com for the **US** Associates program (one W-8BEN as a Canadian individual covers the whole bundle). Then in Associates Central enable two free add-ons: (a) **Earn Globally** — auto-extends commission earning to 12 additional storefronts (UK, CA, DE, FR, IT, ES, NL, PL, SE, AU, SG, JP) with no separate signups or tax forms; (b) **OneLink** — JS snippet (or pre-built link wrapper) that geo-redirects visitors to their local Amazon. Without OneLink a UK visitor clicking an `amazon.com` link won't trigger the UK commission even with Earn Globally on. Amazon storefronts outside Earn Globally (MX, BR, IN, AE, TR, EG) require separate per-country accounts — skip them; not worth the maintenance for a stud-finder app. Once approved, paste the associate tag (format: `toadlybroodle-20` or similar) into a new file `docs/amazon-tag.txt` in this repo (gitignored — add `docs/amazon-tag.txt` to `.gitignore`). The dev cycle will then pick up SPEC 1.3 (product cards) on the next run.

  **3-sales-in-180-days rule (timing matters):** After signup, the account is provisionally approved. Within 180 days you must generate at least 3 qualifying sales (any product, any of the 13 storefronts — Earn Globally rolls all storefronts into the same counter) or Amazon closes the account. If you hit 3, Amazon does a manual policy review (FTC disclosure present, real content, no incentivized clicks) and converts to full approval. **Implication:** don't sign up until the F-Droid release + website CTAs are live and shipping traffic, otherwise the clock starts before you have an audience.

  **Search-fallback caveat:** when OneLink can't ASIN-match an item across stores it lands on a search page paying 1-1.5% instead of the 3-12% category rate. Mitigate by linking products that exist on all target storefronts (confirm Franklin ProSensor 710, Zircon HD55 SKUs in UK/DE/CA before linking).

  This cannot be automated: Amazon requires a human to accept terms, provide tax information, and create an account.
  Blocks: 1.2, 1.3, 1.4, 1.5
  Verify: test -f docs/amazon-tag.txt && grep -qE '^[a-z0-9]+-[0-9]+$' docs/amazon-tag.txt
  Filed by: sst-dev-cycle at 2026-05-27T12:00:00Z; updated with Earn-Globally/OneLink/3-sales research at 2026-05-28T20:00:00Z.
  Source: TODO.md Next-up entry "Sign up for Amazon Associates" annotated human-only.

## High

## Medium

## Low

## Done

- [x] H7.1 [easy] **Replaced placeholder Lightning address `toadlybroodle@stacker.news` → `rob@botlab.dev`** — edited `public_html/index.html` (both `href` and visible text); scp'd to VPS (`/var/www/studfinderapp.com/index.html`, backup at `index.html.bak.20260528`); curl confirms the served page now displays `lightning:rob@botlab.dev`; 4 donate tests still pass. (verified 2026-05-28T21:30:00Z)

---

## How this file evolves

- **Who writes:** `sst-supervisor` (primary, post-chain), `sst-dev-review` (when a review finding's fix is human-only), `sst-dev-cycle` (when a Next-up item is human-only).
- **Who closes:** the human user (manual `[ ]` -> `[x]`). The supervisor/manager auto-verifies on the next tick via the optional `Verify:` shell line.
- **Who reads:** every skill on cycle start. `sst-dev-cycle` especially uses `Blocks:` lines to decide whether to emit `[blocked-on-human]` and bail.
- **Ordering:** newest-first within each section; sections themselves are ordered top-to-bottom from most-urgent to least.
