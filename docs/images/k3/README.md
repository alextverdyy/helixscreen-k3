# Native K3 screenshots

These are direct LVGL screenshots, not generated mockups or edits of the user's
reference images. All printer temperatures, history and hardware are synthetic.
The Voron image is an existing upstream demo asset, not a claim about the user's K3.

Captured with `k3/demo.py` using upstream native CI artifact 13104455260,
application commit `c9ac63354225bb67c1642b75629d6df27cc357fb`. GitHub's comparison
with the fork's base `f7f68cca25649b731d47b3d2a81b51197d699ed1` lists changes only
to shell tooling and its tests, so the application sources match. The K3 XML,
theme and temporary user configuration are loaded at runtime from this fork.

Home, controls, motion and settings are 400x1280. The scrolled controls and
Emergency confirmation images are 480x800. The confirmation was cancelled;
no real printer was connected. Other validation captures cover 480x800,
800x480 and 320x1480.
