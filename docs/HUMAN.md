# studfinderapp.com HUMAN-action backlog (handoff doc)

> Active blockers requiring an out-of-band human action — anything the autonomous dev cycle cannot perform from inside its own iteration. **NOT** for deferred work (use `docs/FUTURE-WORK.md`), and **NOT** for acceptance tests the dev cycle can't self-verify (also `FUTURE-WORK.md > ## Manual / human verification`). HUMAN.md is the "the cycle is stuck right now, waiting on you" list.
>
> Every skill reads this on start. Top of file is highest urgency; within each section, newest-first.

## Blocking

- [ ] H1.1 [easy] **Sign up for Amazon Associates (US + OneLink for UK/CA/AU)**
  Go to associate-central.amazon.com, sign up for the US Amazon Associates program, then enroll in OneLink so UK/CA/AU traffic auto-routes to local storefronts with commission credited correctly. Once approved, paste the associate tag (format: `toadlybroodle-20` or similar) into a new file `docs/amazon-tag.txt` in this repo (gitignored — add `docs/amazon-tag.txt` to `.gitignore`). The dev cycle will then pick up SPEC 1.3 (product cards) on the next run. This cannot be automated: Amazon requires a human to accept terms, provide tax information, and create an account.
  Blocks: 1.2, 1.3, 1.4, 1.5
  Verify: test -f docs/amazon-tag.txt && grep -qE '^[a-z0-9]+-[0-9]+$' docs/amazon-tag.txt
  Filed by: sst-dev-cycle at 2026-05-27T12:00:00Z.
  Source: TODO.md Next-up entry "Sign up for Amazon Associates" annotated human-only.

## High

## Medium

## Low

## Done

---

## How this file evolves

- **Who writes:** `sst-supervisor` (primary, post-chain), `sst-dev-review` (when a review finding's fix is human-only), `sst-dev-cycle` (when a Next-up item is human-only).
- **Who closes:** the human user (manual `[ ]` -> `[x]`). The supervisor/manager auto-verifies on the next tick via the optional `Verify:` shell line.
- **Who reads:** every skill on cycle start. `sst-dev-cycle` especially uses `Blocks:` lines to decide whether to emit `[blocked-on-human]` and bail.
- **Ordering:** newest-first within each section; sections themselves are ordered top-to-bottom from most-urgent to least.
