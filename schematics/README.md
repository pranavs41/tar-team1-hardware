# Schematics

[`network-drone-fc-schematic.pdf`](network-drone-fc-schematic.pdf) is the flight controller's full schematic. Open it in any PDF viewer; you do not need KiCad.

The editable source is `network-drone-fc.kicad_sch` in [`../pcb/network-drone-fc/`](../pcb/network-drone-fc/). KiCad keeps a project's schematic and board in the same folder and links them by file name, so the source stays there and this folder holds the readable copy.

Regenerate the PDF after any schematic change, from the project folder:

```
kicad-cli sch export pdf network-drone-fc.kicad_sch -o ../../schematics/network-drone-fc-schematic.pdf
```

For a pin-by-pin table of every connector, see [`../docs/hardware-reference.md`](../docs/hardware-reference.md).
