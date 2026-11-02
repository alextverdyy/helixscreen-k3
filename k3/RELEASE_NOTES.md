Native HelixScreen C++/LVGL implementation restored as the active base.
The React/Chromium prototype is superseded and is not part of this installer.

New portrait changes include labeled native navigation with Print, a K3 printer
card using the full-resolution reference image, native temperature graph chips,
a clear Print action, readable Control headings and compact macro/tool sections.
Filament, Advanced, calibration, and all native command guards remain available.
Existing printer configuration and custom printer-image selections are preserved.

Native HelixScreen K3 development preview with reviewed portrait controls,
violet theme, Waveshare display profiles and backup/restore customization tools.

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

Reference sizing pass: larger readable action labels, compact print entry,
three-column position readouts, restrained Preheat row, and fixed safety
navigation slots. 400px Home follows the supplied image hierarchy; the native
Motion page remains separate. Physical display and printer tests are pending.
