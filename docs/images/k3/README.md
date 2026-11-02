# Native K3 screenshots

These are direct LVGL screenshots, not generated mockups or edits of the user's
reference images. All printer temperatures, history and hardware are synthetic.
The Annex K3 raster comes from the supplied reference project (provenance below).

Captured with `k3/demo.py` using the native `build/bin/helix-screen` binary
compiled from the fork's `feature/k3` C++ and XML sources (`K3DashboardWidget`,
three-column `PrintStatsWidget` subjects, `MotionPanel::jog_axis_distance`, and
`k3_jog` / `k3_fan_adjust` / `k3_step` callbacks).

Home, controls, controls-scrolled, motion, settings, print-select, appearance,
home-edit, temperature-graph,emergency-confirmation, and safety-nav are 400x1280.
Compact-home, compact-controls-scrolled, compact-home-edit, and compact-safety-nav
are 480x800. During capture, `k3/demo.py` also exercises interactive step selection,
inline XY jogging (`Position X` -> `10.00`), and `Part Fan` `+10%` adjustment
(`10%`). Safety-nav forces visibility subjects in mock mode to check fit; it is not
a live printing test. The native emergency confirmation was opened and cancelled.
No real printer was connected. Earlier landscape/tall-profile captures belong to
the previous layout.


The Annex K3 printer raster is inherited unchanged from
https://github.com/tdunl410/printer-ui-klipper/blob/846fc62a2c1756bdbc3a3e79c8d5c47c94d7bf80/assets/printer-render.png
and shipped as assets/images/printers/annex-k3.png. It is a user-supplied visual
reference asset, not a generated mockup. The application and captures are native LVGL.
