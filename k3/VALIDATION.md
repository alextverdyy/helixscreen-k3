# K3 validation

Source base: upstream `f7f68cca25649b731d47b3d2a81b51197d699ed1`
(`1.2.0-beta.1`, development). Validation ran on Linux x86_64 on 2026-11-01/02.

## Passing checks

| Check | Result |
|---|---|
| K3 configuration integration tests | 19 passed |
| Installer refresh, binary preservation, provenance and archive safety | 3 passed |
| Native theme, portrait, default-layout and template tests | 262 cases, 40,578 assertions passed (231 cases, 15,422 assertions on `[theme],[portrait]` rerun) |
| Native machine-guard XML census | 5 cases, 1,933 assertions passed |
| Upstream XML linter | 489 files, zero errors/warnings |
| Required widget names across layout variants | Passed |
| Responsive token scope | Passed |
| Generated theme artifacts | Passed |
| Independent UI review | Exact-reference Home and Control rebuild verified across 400×1280 and 480×800 |

Configuration tests cover retaining printer data and credentials, installer
symlinks, locking, backups/restore, idempotence, failure rollback, invalid imports,
appearance-only exports, grid geometry and preserving existing user layout defaults.
A deliberately broken printer-retention implementation was detected by its test,
then restored before the green run.

## Native rendering and interaction

Home, Controls, Motion and Settings were captured and inspected at 400x1280,
480x800, 800x480 and 320x1480. Portrait Controls was additionally captured after
scrolling, and its Emergency action opened the upstream confirmation dialog and
was cancelled. Macro visibility and the fixed Emergency header were confirmed
after review fixes. No STOP confirmation or real printer command was issued.

The screenshots and relevant native tests use upstream CI artifact 13104455260,
compiled from `c9ac63354225bb67c1642b75629d6df27cc357fb`. Comparing that revision
with the fork base lists changes only in shell tooling and its shell tests, so
the application C++ sources match. K3 XML, theme and settings load at runtime.
The local cold desktop build was stopped after matching native artifacts and
the completed ARM build supplied the required evidence; it is not claimed as a
completed local desktop source build.

The new portrait XML initially needed an entry in the upstream guard census.
Its 17 machine guards are now registered in
`tests/unit/test_job_holds_machine.cpp`. The actual current census section was
compiled separately with the repository's Catch2 implementation and all five
cases passed. The downloaded full test binary predates this census entry.

## Broader suite limitations

The full imported C++ test binary was run in eight shards. It reported seven
assertion failures: the now-corrected portrait census registration, four Wi-Fi
persistent-config assertions, and two Aqua screensaver pixel fingerprints.
The six Wi-Fi/screensaver assertions also fail when the same two cases are run
against the untouched upstream checkout. They remain unresolved baseline failures;
the full suite and production land gate are **not** claimed green.

The Wi-Fi test uses a `/tmp` symlink target while the implementation deliberately
rejects volatile targets. Screensaver results are recorded as fingerprint
mismatches, without claiming a proven rendering cause.

The mutation gate was attempted after pushing. Its launcher declined this
four-core host because no configured test host was available; no mutation-pass
claim is made. The separate deliberate printer-retention test break did run.

## Initial Pi build and physical hardware

The [K3 Pi build](https://github.com/alextverdyy/helixscreen-k3/actions/workflows/k3-pi.yml)
workflow cross-compiles DRM/framebuffer binaries and packages an installer.
The [Pi run](https://github.com/alextverdyy/helixscreen-k3/actions/runs/41358544806)
and [reviewed packaging run](https://github.com/alextverdyy/helixscreen-k3/actions/runs/41361637327)
both succeeded. The preview tag is `k3-preview-41358544806-da4bc44` (draft).

The downloaded archive passed its SHA256SUMS check. Its main binary is ELF
AArch64, and its digest matches the embedded build provenance. The package
contains the corrected macro rows/fixed-header XML, installer and K3 tools.
The packaged configuration helper successfully applied the 400x1280 profile
and exported appearance options in an isolated directory while retaining the
first-run wizard. No ARM binary was executed on the x86 host.

The main Pi binary includes both DRM and fbdev backends; a separate
`helix-screen-fbdev` executable is not part of this archive. Native rendering
and successful cross-compilation do not establish that a panel boots.

No physical Waveshare panel or printer was available. The likely Annex K3
7.9-inch Waveshare profile is 400x1280, but the user's exact SKU, host, wiring,
touch alignment and Moonraker endpoint are unverified. No hardware deployment,
real heating, extrusion, motion or print job has been tested.


## Native base restored after user clarification

The active product is HelixScreen C++/LVGL; the React kiosk fork is superseded.
Application C++ sources remain unchanged from the existing ARM64 build. Portrait
XML, default layout, theme, configuration helper and image assets are runtime
files layered onto that verified binary.

Latest local scope: 19 configuration cases, 3 packaging cases, 262 relevant native
cases / 40,578 assertions, and 5 source-current machine-guard census cases /
1,913 assertions. XML lint, required widget names, responsive-token scope and
1239-token theme artifact checks pass. Existing six upstream Wi-Fi/screensaver
baseline failures are unchanged; this is not a claim of a green full suite.

The mock capture helper now visits native Home, Print Select, Control, Motion,
Filament, Advanced and Settings, opens Appearance, opens the Home nozzle graph
on 400×1280 and opens/cancels the native emergency confirmation. It always uses
--test, isolated temporary configuration and a private control socket.

Physical Waveshare touch/rotation, installation on the user's host and live
printer operation remain unverified.

## Reference sizing refinement

Current 400×1280 defaults give the printer card 13 rows, statistics 3, native
print actions 4, Motion 2, Preheat 2, Macros/Console 2, and a 2-row gap.
Statistics show native weekly time and lifetime support text; no fake totals.
The print entry keeps native reprint/queue access. The selected 400px layout
suppresses optional auto-placed widgets; these remain available in the editor.
Existing customized dashboards are preserved.

Normal portrait navigation uses four 80px main tabs and 44px secondary controls.
Independent 44px safety slots retain space and never overlap the main tabs.
Home editing was entered with a real long press and exited with Done. Safety
visibility is a synthetic fixture; actual machine safety behavior was not
exercised on hardware. Native Control retains separate Motion navigation rather
than the reference's inline circular jog wheel.

Final source lint: 486 XML files, zero errors/warnings; required widget names,
responsive token scope and theme artifacts pass.

The final native reference sizing review scored the two outstanding items
resolved: unwanted auto-added Multi-Filament removed and complete calibration
grid visible at both 400×1280 and 480×800. Disposition: ship within the reviewed
native scope. This does not establish pixel parity or physical operation.

## Exact reference portrait layout & native C++ bindings

To match the user's supplied Home (`54967.jpg`) and Control (`54968.jpg`)
portrait reference screenshots directly in native C++/LVGL, the fork's C++
application binary (`build/bin/helix-screen` on x86_64 and `K3 Pi build` on
ARM64) and portrait XML were extended with:
- **`K3DashboardWidget` (`src/ui/panel_widgets/k3_dashboard_widget.cpp`, `ui_xml/components/panel_widget_k3_dashboard.xml`)**:
  registered as `k3_dashboard` across `[0, 0, 10, 28]` on `small@10x28`
  (`400x1280` in `k3/home-layout.json`), composing `PrinterImageWidget`
  (`k3_printer_card`: `K3` header + `Emergency` shell button with red
  `alert_circle` icon and white label, `State` and `Network` status cards with
  Wi-Fi icon, and 20px-radius inner printer container with the Annex K3 render
  and overlaid 40px `Nozzle`/`Bed`/`Chamber` temperature chips),
  `PrintStatsWidget` (`k3_statistics`: three-column `Total Time`, `Print Count`,
  and honest Moonraker `Filament Usage` in meters), the 90px primary violet
  `Print` button (`k3_print_files`, 40px bold), and three 56px action rows
  (`Move`, `Preheat`, `Extrude`).
- **Portrait `Controls` (`ui_xml/portrait/controls_panel.xml`, `src/ui/ui_panel_controls.cpp`, `src/ui/ui_panel_motion.cpp`)**:
  fixed 48px `Control` header + `Emergency` shell button above scrollable
  three-column `POSITION` (`X`, `Y`, `Z`), `HOMING` (`All`, `XY`, `Z`),
  `AXIS CONTROLS` (`5mm`/`10mm`/`25mm`/`50mm` step selector bound to
  `k3_jog_step`, inline 224px circular XY jog wheel `k3_jog_wheel` with center
  Home button `k3_jog_home`, `Z+`/`Z-` column, and `Disable Motors`), `Cooling`
  (`Part Fan` and `Aux Fan` with live percentage subjects and `-10%`/`Off`/`+10%`
  buttons via `k3_fan_adjust`), and content-height `One-Tap Macros`.
- **Floating 4-tab navigation & Settings reachability (`ui_xml/portrait/navigation_bar.xml`, `ui_xml/portrait/app_layout.xml`, `ui_xml/portrait/settings_panel.xml`)**:
  inset 94%-width rounded dock (`24px` radius) with four 96px tabs (`Home`,
  `Print`, `Control`, `Settings`) and independent 44px safety slots; portrait
  `Settings` exposes `Move axes`, `Filament & Extrusion`, and `Printer tools`
  rows at the top so every upstream panel remains reachable.

Latest verification results on the exact-reference build:
- `python3 -m unittest discover -s k3 -p 'test_*.py' -v`: 19 passed.
- `python3 k3/package_checks.py`: 3 passed.
- Upstream XML linter (`helix_xml_linter.cli`): 489 files checked, 0 errors, 0 warnings.
- Native machine-guard XML census (`/tmp/k3-native-census-tests`): 5 test cases, 1,933 assertions passed.
- Native `[theme],[portrait]` unit tests: 231 test cases, 15,422 assertions passed.
- Interactive simulator capture (`k3/demo.py` at `400x1280` and `480x800`): verified `k3_step_25` -> `k3_step_10` subject updates, `k3_jog_xplus` updating `Position X` to `10.00`, `k3_part_+` updating `Part Fan` to `10%`, Home long-press edit mode, temperature graph, and Emergency confirmation dialog with zero XML/component errors in `native.log`.
- ARM64 Pi build ([`K3 Pi build` run `41495912404`](https://github.com/alextverdyy/helixscreen-k3/actions/runs/41495912404) on commit `e68b8cc`) triggered on GitHub Actions to produce the matching ARM64 binary and reviewed installer.
