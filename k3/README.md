# K3 setup and customization

## Hardware requirements

You need a Linux host, a working Waveshare display and touch input, and network
access to your printer's Moonraker. HDMI with USB touch and DSI touch panels use
different wiring and drivers. A serial HMI, SPI microcontroller panel or bare
LCD is not automatically compatible with this Linux application.

Use the **exact panel SKU's** Waveshare instructions first. Confirm Linux shows
the correct display mode and touch device before installing the UI. Do not add
a guessed `dtoverlay` to boot configuration. Useful local checks:

```bash
python3 k3/configure.py doctor
cat /sys/class/drm/card*-*/modes
ls -l /dev/input/by-id/
```

`doctor` prints no API keys and sends no commands to the printer. It cannot
identify a Waveshare SKU from the label “K3”, or test physical touch alignment.

The app uses DRM or framebuffer output. A Pi display already owned by a desktop
compositor or another touchscreen UI needs the upstream display/service setup.
See [installation](../docs/user/INSTALL.md). Display rotation and touch rotation
must both be checked on the real device, including all four corners.

## Install this fork

Build the correct target using [K3_README.md](../K3_README.md), then follow
the upstream deployment instructions for your host. The 64-bit Pi outputs are
under `build/pi/bin/`, with framebuffer output under `build/pi-fbdev/bin/`.
Keep `ui_xml/`, `assets/` and the binary from the same source revision together.
Use the upstream service/launcher; it reads `config/helixscreen.env`.

The manual **K3 Pi build** workflow supplies a complete installer archive in its
artifact, including assets and the upstream installer. Download the artifact,
unzip it, and copy its `.tar.gz` to the display host. Then extract it and run the
included installer from the extracted directory:

```bash
tar xzf helixscreen-pi-*.tar.gz
cd helixscreen
sh install.sh
```

Return to your source clone to run the K3 configuration commands below. The
installer can also be given its local archive with `--local`. Runtime OS
libraries are still required; follow the installer's platform diagnostics.
See [BUILD_SYSTEM.md](../docs/devel/BUILD_SYSTEM.md) for the full packaging path.

Once your installation is at `~/helixscreen`, stop **only the screen service**,
apply the appearance, and start it again:

```bash
sudo systemctl stop helixscreen
python3 k3/configure.py --config-dir ~/helixscreen/config apply
sudo systemctl start helixscreen
```

If installed elsewhere, substitute its actual config directory. Do not run the
configuration tool with `sudo`: keep files owned by the application user.
Installations using another service manager should stop/start that UI service.
The tool checks HelixScreen's lock and refuses to edit a running configuration.
Ordinary user-owned installer symlinks are preserved.

The default is dark K3 Violet, 80% brightness, rotation 0, automatic display
mode/backend and unchanged touch-device assignment. Upstream in-screen updates
are disabled to keep the fork's XML paired with its binary. Update from this
fork's builds; restoring the backup restores the previous update setting.
The tool changes no
Moonraker address, API key, macro, heater limit, machine config or wizard state.
Finish HelixScreen's setup wizard to connect Moonraker (usually port 7125),
discover your actual printer and choose its sensors/fans. No machine operations
are issued by applying the profile.

## Customize from the screen

Use the upstream Appearance/Theme settings to select **K3 Violet**, edit colors,
or save another theme. Use home edit mode to rearrange/add widgets and choose
your printer image. Configure macros and the four Controls quick-action slots
in their upstream settings. Calibration and hardware-specific controls appear
according to detected printer capabilities.

The custom Controls page scrolls in portrait mode. Motion opens the existing jog
pad; cooling opens the full fan controls; every printer command still passes
through the upstream command handling and guards. The bottom navigation remains
available outside that scrolling content.

## Display profiles and colors

Stop the screen before running these commands and restart it afterwards:

```bash
python3 k3/configure.py profiles
python3 k3/configure.py apply --profile portrait-480x800
python3 k3/configure.py apply --profile portrait-480x1280
python3 k3/configure.py apply --size 480x1920 --rotation 90
python3 k3/configure.py apply --accent '#7946E8' --brightness 70
python3 k3/configure.py apply --mode light
python3 k3/configure.py apply --touch-device /dev/input/event1
python3 k3/configure.py apply --profile auto --backend auto --rotation 0
```

These profile names describe resolutions, not verified Waveshare models.
Use your panel's **actual kernel mode**. Rotation can swap the logical width and
height; start with `auto` and set rotation before considering a forced size.
`HELIX_SCREEN_SIZE` does not install a driver or create an unsupported DRM mode.
Existing service environment overrides take precedence over the env file.

Arguments update the last K3 profile. Choosing a named profile clears a previous
custom `--size`. Setting `auto` removes K3-owned size/backend overrides and
leaves unrelated environment entries intact. Applying a profile regenerates
`themes/k3-violet.json`; save Theme Editor changes under another theme name
before applying again. Pick an accent with readable button contrast.

## Share appearance options

```bash
python3 k3/configure.py export my-k3-appearance.json
python3 k3/configure.py apply --from-file my-k3-appearance.json
```

Exports include K3 profile options only, with no printer connection details,
credentials or macros. They do not capture later in-screen Theme Editor edits.
Existing export files are never overwritten. Share your separately saved theme
JSON too if you customized it on the screen.

## Backups and rollback

Every changed apply saves the original files under
`config/k3-backups/<timestamp>/`. An identical apply creates no new backup.
Backups can contain your existing connection credentials, so keep them local.
The backup directory is private to your user. File writes are atomic, and an
apply write failure attempts to roll back all touched files. A power loss
between files is recoverable from the backup, rather than a multi-file atomic
transaction.

```bash
sudo systemctl stop helixscreen
python3 k3/configure.py restore 20261101T220000.000000Z
sudo systemctl start helixscreen
```

Replace the sample timestamp with the actual backup folder name printed by
`apply`. Restore recovers the original settings/theme/env files; it does not
restore firmware, layout XML or a binary. Back up your full install before
upgrading the application itself.

## Verification boundaries

The native demo uses synthetic printer data. It verifies rendering and UI
navigation, not real heating, motion, display-driver behavior, power control or
touch alignment. Those require the actual host, exact Waveshare panel model,
and a connected printer. See [VALIDATION.md](VALIDATION.md) for recorded results.
