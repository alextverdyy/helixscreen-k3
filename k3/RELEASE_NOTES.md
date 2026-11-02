Native HelixScreen C++/LVGL implementation restored as the active base.
The React/Chromium prototype is superseded and is not part of this installer.

Portrait Home (`400x1280` `small@10x28`) and portrait Control now match the
supplied K3 reference layouts directly in native LVGL:
- **Home (`k3_dashboard`)**: `K3` printer card with fixed `Emergency` button,
  `State` and `Network` status cards, Annex K3 printer render with overlaid
  `Nozzle`/`Bed`/`Chamber` temperature chips, three-column `Statistics` (`Total Time`,
  `Print Count`, and Moonraker `Filament Usage` in meters), 90px `Print` button,
  and `Move`, `Preheat`, and `Extrude` action rows.
- **Control (`ui_xml/portrait/controls_panel.xml`)**: fixed `Control` header and
  `Emergency` button above scrollable `Position` (`X`, `Y`, `Z`), `Homing` (`All`,
  `XY`, `Z`), `Axis Controls` (`5mm`/`10mm`/`25mm`/`50mm` step selector, inline
  224px circular XY jog wheel with center Home button, `Z+`/`Z-` column, and
  `Disable Motors`), `Cooling` (`Part Fan` and `Aux Fan` `-10%`/`Off`/`+10%`),
  and `One-Tap Macros`.
- **Navigation & Reachability**: inset 94%-width rounded bottom dock (`Home`,
  `Print`, `Control`, `Settings`) with dedicated 44px safety slots; portrait
  `Settings` exposes `Move axes`, `Filament & Extrusion`, and `Printer tools`
  so every upstream panel remains reachable.

The archive contains the upstream installer plus `k3/configure.py`. After
installation, stop the screen service, run the helper as the application user
with the actual config directory, then start the screen and complete its wizard.
See K3_README.md and k3/README.md in the archive/source for exact instructions.

Compiled application and runtime-source revisions are recorded separately in
k3-build-provenance.json. Runtime refresh refuses application-source changes.

This is a development snapshot. Native UI/configuration checks pass, but six
Wi-Fi/screensaver assertions reproduce as failures in the untouched upstream
baseline. Physical Waveshare touch, real printer operation and installation on
the user's host remain unverified. See k3/VALIDATION.md for the full scope.
