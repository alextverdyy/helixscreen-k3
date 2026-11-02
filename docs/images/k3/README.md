# Native K3 screenshots

These are direct LVGL screenshots, not generated mockups or edits of the user's
reference images. All printer temperatures, history and hardware are synthetic.
The Annex K3 raster comes from the supplied reference project (provenance below).

Captured with `k3/demo.py` using upstream native CI artifact 13104455260,
application commit `c9ac63354225bb67c1642b75629d6df27cc357fb`. GitHub's comparison
with the fork's base `f7f68cca25649b731d47b3d2a81b51197d699ed1` lists changes only
to shell tooling and its tests, so the application sources match. The K3 XML,
theme and temporary user configuration are loaded at runtime from this fork.

Home, controls, motion, settings, print-select, appearance, home-edit and safety-nav
are 400x1280. Compact controls and compact-home are 480x800. Safety-nav forces
visibility subjects in mock mode to check fit; it is not a live printing test.
The native emergency confirmation was opened and cancelled. No real printer was
connected. Earlier landscape/tall-profile captures belong to the previous layout.


The Annex K3 printer raster is inherited unchanged from
https://github.com/tdunl410/printer-ui-klipper/blob/846fc62a2c1756bdbc3a3e79c8d5c47c94d7bf80/assets/printer-render.png
and shipped as assets/images/printers/annex-k3.png. It is a user-supplied visual
reference asset, not a generated mockup. The application and captures are native LVGL.
