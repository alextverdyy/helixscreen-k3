# K3 validation

Source base: upstream `f7f68cca25649b731d47b3d2a81b51197d699ed1`
(`1.2.0-beta.1`, development). Validation ran on Linux x86_64 on 2026-11-01/02.

## Passing checks

| Check | Result |
|---|---|
| K3 configuration integration tests | 19 passed |
| Installer refresh, binary preservation, provenance and archive safety | 3 passed |
| Native theme, portrait, default-layout and template tests | 262 cases, 40,578 assertions passed |
| Native machine-guard XML census | 5 cases, 1,857 assertions passed |
| Upstream XML linter | 475 files, zero errors/warnings |
| Required widget names across layout variants | Passed |
| Responsive token scope | Passed |
| Generated theme artifacts | Passed |
| Independent UI review | Three required fixes scored resolved; ship at that review scope |

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

## Pi build and physical hardware

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
