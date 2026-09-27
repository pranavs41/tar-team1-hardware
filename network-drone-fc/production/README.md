# Production files

One folder per board revision, e.g. `rev-A/`. Each holds exactly what was sent to the fab, so we can always tell which files made which boards.

```
rev-A/
  gerbers.zip        # KiCad: File → Fabrication Outputs → Gerbers + Drill, zipped
  bom.csv            # parts list with LCSC numbers
  cpl.csv            # component positions (only if JLCPCB assembles)
  schematic.pdf      # PDF of the schematic at the time of ordering
  order-notes.md     # date, fab, quantity, stackup, stencil, cost
  bringup-log.md     # per-board results from ../../electrical/docs/bring-up.md
```

Never edit a revision folder after the order is placed. Changes go into the next revision.
