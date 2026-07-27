# Card Set-Symbol Matching — Summer Project Plan

**Owner:** (student)
**Purpose:** Learn applied computer vision / embeddings end-to-end and produce a
demonstrable portfolio artifact. Success is measured as much by *understanding and
documenting the tradeoffs* as by raw accuracy.

**Cadence:** Demo checkpoints this week on **Wednesday, July 29** and **Friday, July 31**
(plan drafted Monday, July 27, 2026). Each demo is accompanied by a short written reflection
(see "Decision Log & Reflection" below).

**Status:** v1 proposal — open to changes. If a milestone, task, or acceptance
criterion should shift, propose the change (and the reasoning) rather than silently
skipping it; that negotiation is part of the work.

---

## 1. Background / where we are

The system identifies which Pokémon set a card belongs to by:
1. Cropping the small **set symbol** from the bottom of the card,
2. Computing an image **embedding** (Apple Vision `VNGenerateImageFeaturePrint`,
   a 768-d L2-normalized vector — the "CNN feature"),
3. Matching it to a gallery of reference set symbols by nearest distance.

**Baseline: ~50% accuracy.** Diagnosis found three stacked causes:

| # | Problem | Evidence |
|---|---------|----------|
| 1 | **Duplicate classes in the gallery** | 35 symbol pairs are near-identical; several are byte-identical (e.g. `swsh12` ≡ `swsh12tg`, all promo sets share one symbol). These are unwinnable by symbol alone. |
| 2 | **Descriptor barely separates tiny symbols** | Median distance to the *nearest different* symbol is 0.57; 44/150 symbols have a neighbor < 0.5 away. Real-card noise (~0.8 to the true symbol) exceeds the gap to many wrong ones. |
| 3 | **Crop is a fixed pixel box** | Scans vary 787–796 × 1050–1096 px; a fixed box drifts off a ~30px symbol. Also grayscales the query while references are color. |

This plan attacks **#3** first (isolation + color mode), because it's the most
fixable, then measures how much of the 50% gap it actually closes. #1 and #2 are
acknowledged ceilings — see Reflection.

---

## 2. Milestones

### Milestone 1 — Wednesday, July 29: Robust isolation + matching demo (Sword & Shield era)

**Objective:** Isolate the set symbol *without a fixed pixel box*, use a consistent
color mode, and demonstrate matching + near-matches by distance on Box 14 cards.

**Tasks**
- [ ] **Card detection:** find the card rectangle inside the scan (background is white:
      low saturation + high brightness; card border is saturated). Take its bounding box.
- [ ] **Card-anchored band:** locate the symbol region relative to the *card's bottom
      edge* (stable to ~4px) instead of the scan height (varies ~46px).
- [ ] **Blob snap:** within that band, threshold dark ink, take the compact, roughly-square
      connected component (reject wide text and the boxed regulation mark by aspect
      ratio + fill ratio). Consider Otsu thresholding for holo/colored backgrounds.
- [ ] **Consistent color mode:** build the gallery and process queries in the *same* mode.
      Document which mode was chosen and why.
- [ ] **Matching demo:** for a labeled sample of cards, print top-k matches with distances.

**Acceptance criteria (what "done" looks like for the demo)**
- Isolation runs over all 200 Box 14 scans with **no hard-coded pixel coordinates**;
  visual spot-check (contact sheet) shows the symbol correctly isolated on ≥ 95%.
- Gallery and query use the same color mode; choice is justified in one sentence.
- For ≥ 10 hand-labeled cards, the demo shows the ranked distance list and the correct
  set appears in the top-k (target: top-3), OR the case is explained as a known
  duplicate/near-match from Problem #1.
- Demo narrative flows: *card → isolated symbol → ranked distances → interpretation.*

**Stretch:** report overall top-1 / top-3 accuracy across a larger labeled sample and
compare to the 50% baseline.

---

### Milestone 2 — Friday, July 31: Generalize to a different era (EX and/or XY)

EX-era (2003–2007) and XY-era (2013–2016) place the set symbol in **different
locations** than Sword & Shield, so the positional anchor from M1 will not transfer
unchanged. This milestone is about *generalization*.

**⚠️ Dependency (do this first, by Wednesday):** obtain a small set of **EX-era and/or
XY-era card scans** to test on. The gallery already contains the reference symbols
(`ex1`–`ex16`, `xy0`–`xy12`), but there are currently **no EX/XY card scans on disk** —
without them, this milestone cannot be demoed.

**Objective (recommended scope):** get **one** additional era working end-to-end, and
*analyze* the second so the generalization strategy is explicit.

**Tasks**
- [ ] Acquire test scans for the target era(s).
- [ ] Determine where the symbol lives in that era's layout; derive a new card-anchored
      region for it.
- [ ] Re-run isolation + matching; report accuracy and near-matches.
- [ ] Decide and document the generalization strategy: **per-era anchors** (an era
      classifier picks the region) vs. a **location-agnostic symbol detector**
      (find the symbol anywhere). State the tradeoff.

**Acceptance criteria**
- Isolation demonstrated on the target era's sample scans (contact sheet).
- Matching results reported with distances.
- One paragraph explaining *why* the M1 anchor didn't transfer and what changed.

**Trimmed-scope fallback (if time is short):** fully demo XY; present EX as a written
analysis + plan rather than working code. This is an acceptable and honest outcome.

---

## 3. Risks & dependencies

| Risk | Impact | Mitigation |
|------|--------|------------|
| No EX/XY test scans | M2 can't be demoed | Acquire scans by Wed (top priority) |
| Duplicate gallery classes (#1) | Caps achievable accuracy | Acknowledge; consider merging identical symbols into one label |
| Descriptor separability ceiling (#2) | Some sets stay confusable | Frame honestly; note stronger signals (e.g. OCR the set total "x/195") as future work |
| Holo/reverse colored backgrounds | Blob threshold may fail | Use Otsu / adaptive threshold |
| Scope creep across two eras | Friday slips | Use the trimmed-scope fallback |

---

## 4. Decision Log & Reflection (fill in as you go)

This is the portfolio centerpiece. Employers care less about the accuracy number and
more about *engineering judgment*: what you chose, what you rejected, and why. Keep it
honest — documented limitations read as maturity, not weakness.

For **each significant decision**, record:

- **What I chose to do** — the approach and why.
- **Alternatives I considered and rejected** — and the reason.
- **What I deliberately chose *not* to build/use** — and why it wasn't worth it *now*.
- **Limitations / where it fails** — be specific.
- **What I'd do next** with more time.

### Seed entries (expand these in your own words)

**Decision: color mode (grayscale vs. color).**
- Considered: grayscaling the query (original code did this) vs. keeping color.
- Chose: _____ because gallery and query must be processed identically; measured effect: _____.

**Decision: how to isolate the symbol.**
- Considered: fixed pixel box (original) → proportional box → card-anchored region → blob detection.
- Chose: _____ Why the fixed box failed: scans vary in size and the card floats in the margin.

**Decision: descriptor / model.**
- Considered: Apple Vision feature print (current) vs. template matching vs. OCR of the
  set-total number vs. training a custom classifier.
- Chose to keep: _____ Chose *not* to train a custom CNN because: _____ (data volume? time? overkill?).
- Known limitation: the feature print barely separates tiny near-identical symbols (Problem #2).

**Decision: gallery data quality.**
- Observation: 35 near-duplicate symbol pairs; some byte-identical.
- Chose to: _____ (merge? label as one class? leave and document?) Why: _____.

**Decision: era generalization (M2).**
- Considered: one anchor per era (needs an era detector) vs. a symbol detector that
  works anywhere on the card.
- Chose: _____ Tradeoff: _____.

### Closing reflection (write after Friday)
- What did I learn about image embeddings and the "domain gap" between clean reference
  art and real photographed crops?
- What surprised me? (e.g. duplicate references, the near-tie distances)
- If I restarted, what would I do differently from day one?
