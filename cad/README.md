# CAD

Mechanical files for the network drone: the flight controller as a 3D part, pictures of it, and the frame.

| File | What it is |
|---|---|
| [`network-drone-fc.step`](network-drone-fc.step) | the assembled flight controller as a STEP solid, with every component modelled. Import it into SolidWorks, Fusion or Onshape to design around the board |
| [`board-top.png`](board-top.png) | top side, rendered from the PCB |
| [`board-bottom.png`](board-bottom.png) | bottom side, rendered from the PCB |

## Frame

The frame is 3D printed. Its files live on the team drive:

- STL, for printing: https://drive.google.com/file/d/1vladkpQCeSWTD4HoTr5YP3W7nkRsmsth/view?usp=sharing
- SLDPRT, SolidWorks source: https://drive.google.com/file/d/1ZKLZhnVlJFwb6PA8m5haO54EwXYErk0C/view?usp=sharing

Copies can be added to this folder so the frame is versioned with the board.

## Board dimensions for mounting

- Outline: 36 mm wide, 39 mm tall, 1.6 mm thick, 2 mm corner radius.
- Holes: four, 3.2 mm for M3, on a 20 × 20 mm square. They sit 8 mm in from the left, right and bottom edges and 11 mm from the top.
- Clear zone: nothing on the top side within 3 mm of a hole centre, and the bottom near the holes is bare, so the ESC's grommets or an M3 nut fit on either side.
- Tallest parts on top: the USB-C socket on the right edge and the radio port J6 in the bottom-right corner and the landing sensor port J8 on the right edge near the top. Both point straight up and need room above them for a plug and cable.
- Bottom side: one capacitor (C35), 3.1 mm tall, at the lower-left corner.
- Cables leave on every edge: USB-C right, ESC bottom centre, obstacle sensor left, charging board top right. The landing sensor's cable leaves upward from J8.

Regenerate the STEP after board changes, from `pcb/network-drone-fc/`:

```
kicad-cli pcb export step --subst-models -f -o ../../cad/network-drone-fc.step network-drone-fc.kicad_pcb
```
