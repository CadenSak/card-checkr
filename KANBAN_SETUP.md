# GitHub Projects — Board Setup

A copy-paste guide to stand up the Kanban board for this project. Mirrors the columns and
cards in the plan. Two paths: **click-through** (no tooling) or **`gh` CLI** (scriptable, and
itself a nice thing to show an employer).

---

## 1. Columns (the `Status` field)

GitHub Projects calls columns the options of a single-select **Status** field. Use these six,
in this order:

| Column | Meaning |
|--------|---------|
| **Backlog** | Real work, not scheduled this week |
| **This Week** | Committed for the current sprint |
| **In Progress** | Actively being worked (keep this short — WIP limit ~2) |
| **Blocked** | Can't proceed; note what it's waiting on |
| **Demo-Ready** | Done and verified, queued to show at the next demo |
| **Done** | Shipped and demoed |

> The **Blocked** and **Demo-Ready** columns are the two that make this board worth having —
> Blocked keeps the EX/XY-scans dependency visible; Demo-Ready separates "code works" from
> "shown and signed off," which matches the Wed/Fri cadence.

## 2. Two extra fields (optional but recommended)

- **Milestone** — single-select: `Wed`, `Fri`, `—`. Lets you filter the board per demo.
- **Type** — single-select: `diagnosis`, `M1`, `M2`, `eval`, `data`, `stretch`.

Add fields from the board's **⋯ → Settings → + New field**.

## 3. A saved view for demo day

After adding cards, create a **Board** layout view grouped by `Status`, plus a second view
**"This Week"** filtered to `Milestone = Wed`. Switching to that view during Wednesday's demo
shows exactly the sprint scope with no noise.

---

## 4. Starter cards

Column = where it starts. Copy each title as an issue/draft item; paste the note into the body.

### Done
- [ ] **Measure baseline accuracy (~50%)** — _Type: diagnosis._ Established the number the project improves on.
- [ ] **Diagnose 3 root causes with evidence** — _diagnosis._ Duplicate gallery classes; weak descriptor separability; fixed-pixel crop. Numbers recorded in `PROJECT_PLAN.md`.
- [ ] **Validate isolation approach (12/12 on Box 14)** — _M1._ Card-anchor → blob-snap prototype isolates the symbol on all sampled cards.

### This Week  _(Milestone: Wed)_
- [ ] **Card detection → bounding box** — _M1._ Saturation + brightness threshold to find the card inside the scan margin. _Done when:_ returns a stable card bbox across varied scan sizes.
- [ ] **Card-anchored symbol band** — _M1._ Locate the symbol region relative to the card's bottom edge, not scan height. _Done when:_ band contains the symbol on ≥95% of 200 scans.
- [ ] **Blob-snap refinement** — _M1._ Dark connected component, filtered by aspect ratio + fill, rejecting text and the regulation mark. _Done when:_ contact sheet shows tight symbol crops.
- [ ] **Unify color mode (gallery + query)** — _M1._ Build gallery and process queries in the same mode. _Done when:_ choice is made and justified in one sentence in the decision log.
- [ ] **Label ≥10 cards for evaluation** — _M1 · eval._ Hand-label known sets to measure top-k. _Done when:_ a small labeled CSV/list exists.

### In Progress  _(keep to ~2)_
- [ ] **Matching demo: top-k distances view** — _M1 · demo._ For a labeled card, print the ranked gallery matches with distances. _Done when:_ demo flows card → isolated symbol → ranked distances → interpretation.

### Blocked
- [ ] **Acquire EX / XY test scans** — _blocks M2._ No EX/XY card scans exist on disk yet. _Unblocks:_ EX/XY isolation. **Do by Wed, Jul 29.**
- [ ] **EX / XY symbol isolation** — _M2._ Waiting on scans above. Derive a new anchor for that era's symbol location.

### Backlog
- [ ] **Report top-1 / top-3 vs. 50% baseline** — _stretch._ Quantify the lift from better isolation.
- [ ] **Merge duplicate gallery classes** — _data._ Collapse byte-identical symbols (e.g. `swsh12`/`swsh12tg`, promos) into one label.
- [ ] **OCR the set total ("x/195") as a stronger signal** — _future._ The printed set total is more unique per set than the tiny symbol.
- [ ] **Era classifier vs. symbol detector** — _architecture._ Decide how isolation generalizes across eras; record the tradeoff.

---

## 5. `gh` CLI path (optional)

Requires the GitHub CLI (`brew install gh`) and `gh auth login`. Create the project, then add
items. Adjust `--owner` to your GitHub username.

```bash
# Create the project (v2) and capture its number from the output
gh project create --owner "@me" --title "Card Set-Symbol Matching"

# If the repo isn't on GitHub yet, create it first, then link issues to the project.
# Add draft items straight to the board (no repo needed):
gh project item-create <PROJECT_NUMBER> --owner "@me" --title "Card detection → bounding box"
gh project item-create <PROJECT_NUMBER> --owner "@me" --title "Card-anchored symbol band"
gh project item-create <PROJECT_NUMBER> --owner "@me" --title "Blob-snap refinement"
# ...repeat for each starter card above
```

> Note: the `Status` column and custom fields are set in the web UI (or via
> `gh project field-list` / `field-create`); the CLI adds items but the board layout is
> easiest to configure by clicking. Setting up the columns once by hand is faster than
> scripting the field options.

---

## 6. Using it on demo day

1. Move Wednesday's finished cards **This Week → Demo-Ready** before the demo.
2. Walk the board top-down: what shipped, what's in flight, what's blocked and why.
3. After the demo, drag the shown cards to **Done** live — it's a small, honest ritual that
   reads as "I run this like real engineering work."
