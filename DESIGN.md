---
name: HelixScreen K3
description: Native LVGL printer controls with charcoal surfaces, violet actions, and exact portrait reference composition.
colors:
  screen-bg: "#101118"
  overlay-bg: "#171921"
  card-bg: "#161920"
  elevated-bg: "#252832"
  border: "#353843"
  text: "#F4F4F7"
  text-muted: "#ADB0BD"
  text-subtle: "#A29CB7"
  primary: "#8047FF"
  secondary: "#C4B5FD"
  tertiary: "#71D4C1"
  info: "#98C8FF"
  success: "#78D6A3"
  warning: "#F5C879"
  danger: "#FF879A"
  focus: "#C4B5FD"
  selected-surface: "#3B2B6D"
  light-screen-bg: "#F2F0F8"
  light-overlay-bg: "#E9E5F2"
  light-card-bg: "#FFFFFF"
  light-elevated-bg: "#DDD7EC"
  light-border: "#898197"
  light-text: "#211A31"
  light-text-muted: "#544964"
  light-text-subtle: "#665C76"
  light-primary: "#6735CB"
  light-secondary: "#633D9C"
  light-tertiary: "#19695C"
  light-info: "#275C9A"
  light-success: "#226B43"
  light-warning: "#825500"
  light-danger: "#B12742"
  light-focus: "#6735CB"
typography:
  heading-small:
    fontFamily: "Noto Sans"
    fontSize: "20px"
    fontWeight: 400
  body-small:
    fontFamily: "Noto Sans"
    fontSize: "14px"
    fontWeight: 400
  label-small:
    fontFamily: "Noto Sans"
    fontSize: "12px"
    fontWeight: 300
  metadata-small:
    fontFamily: "Noto Sans"
    fontSize: "10px"
    fontWeight: 300
  portrait-display:
    fontFamily: "Noto Sans"
    fontSize: "40px"
    fontWeight: 700
  portrait-title:
    fontFamily: "Noto Sans"
    fontSize: "28px"
    fontWeight: 700
  portrait-subsection:
    fontFamily: "Noto Sans"
    fontSize: "20px"
    fontWeight: 700
  portrait-section:
    fontFamily: "Noto Sans"
    fontSize: "18px"
    fontWeight: 700
  portrait-action:
    fontFamily: "Noto Sans"
    fontSize: "16px"
    fontWeight: 700
  portrait-nav-label:
    fontFamily: "Noto Sans"
    fontSize: "14px"
    fontWeight: 700
rounded:
  bold-small: "8px"
  bold-medium: "10px"
  portrait-card: "16px"
  portrait-chip: "20px"
  portrait-selection: "16px"
  portrait-dock: "24px"
  portrait-wheel: "112px"
spacing:
  space-xxs-small: "2px"
  space-xs-small: "4px"
  space-sm-small: "6px"
  space-md-small: "8px"
  space-lg-small: "12px"
  space-xl-small: "16px"
  space-2xl-small: "24px"
  portrait-outer: "12px"
  portrait-card: "14px"
  portrait-action-inset: "18px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.bold-small}"
    height: "48px"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    rounded: "{rounded.bold-small}"
  button-danger:
    backgroundColor: "{colors.danger}"
    rounded: "{rounded.bold-small}"
  card:
    backgroundColor: "{colors.card-bg}"
    rounded: "{rounded.bold-small}"
    padding: "{spacing.space-sm-small}"
  portrait-control-card:
    backgroundColor: "{colors.card-bg}"
    rounded: "{rounded.portrait-card}"
    padding: "{spacing.portrait-card}"
  portrait-action-row:
    backgroundColor: "{colors.card-bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.portrait-card}"
    typography: "{typography.portrait-section}"
    height: "56px"
  portrait-print-button:
    backgroundColor: "{colors.primary}"
    typography: "{typography.portrait-display}"
    rounded: "{rounded.portrait-card}"
    height: "90px"
  portrait-navigation:
    backgroundColor: "{colors.card-bg}"
    rounded: "{rounded.portrait-dock}"
    height: "132px"
  portrait-macro:
    typography: "{typography.portrait-action}"
    height: "48px"
---
# Design System: HelixScreen K3

## Overview

HelixScreen K3 extends the existing native embedded Linux/LVGL interface. Charcoal surfaces, electric violet actions, and pale lavender icons match the user’s supplied portrait Home and Control reference images while retaining the upstream component vocabulary, typography, and broad printer functionality.

The visual character is compact, calm, and operational. Related readings and controls sit inside dark tonal containers with subtle borders, while semantic colors are reserved for the state or command they communicate. This documents the implemented K3 theme and portrait extension, not a replacement identity for upstream HelixScreen.

**Key Characteristics:**
- Charcoal tonal surfaces (`#101118` screen, `#161920` cards, `#252832` elevated controls) with electric violet (`#8047FF`) primary emphasis.
- Native Noto Sans bitmap faces (including Tier 3 `noto_sans_bold_40` and `noto_sans_bold_28`) and Material Design Icons.
- Exact portrait Home dashboard (`k3_dashboard`) and scrollable portrait Control cards with an inline 224px circular XY jog wheel.
- Existing Moonraker command handlers, feature discovery, and machine guards preserved end-to-end.

Provenance: `PRODUCT.md`; `assets/config/themes/defaults/k3-violet.json`; `ui_xml/globals.xml`; `include/border_radius_sizes.h`; `include/ui_breakpoint.h`; `k3/home-layout.json`; `src/ui/panel_widgets/k3_dashboard_widget.cpp`; `src/ui/panel_widgets/print_stats_widget.cpp`; `src/ui/ui_panel_controls.cpp`; `src/ui/ui_panel_motion.cpp`; `ui_xml/components/panel_widget_k3_dashboard.xml`; native XML overrides in `ui_xml/portrait/`; native `ui_button`, `ui_card`, and `ui_text_input` implementations. The `annex-k3.png` printer image has provenance in `docs/images/k3/README.md`. Current simulator capture directories are `.impeccable/review/exact-reference-400/` and `.impeccable/review/exact-reference-480/`. Source extraction and mock captures establish implementation evidence, not physical hardware validation.

## Colors

The frontmatter records the active K3 palette from `assets/config/themes/defaults/k3-violet.json` plus the local `#3B2B6D` selected surface token used in portrait XML. Unprefixed colors are the dark preset; `light-` colors are the supplied light alternative, not colors to mix into the dark preset. Theme JSON remains the runtime authority; explicit user theme overrides remain valid.

### Primary

Electric violet `primary` (`#8047FF`) marks primary actions (`Print`, `All` homing), active accents, and chart emphasis. Deep violet `selected-surface` (`#3B2B6D`) fills active navigation tabs and selected jog step pills (`5mm`/`10mm`/`25mm`/`50mm`). Pale lavender `secondary` (`#C4B5FD`) supports iconography and secondary emphasis; `focus` supplies the existing focus treatment.

### Secondary

Lavender (`#C4B5FD`) provides leading action-row icons, temperature chip accents, and supporting emphasis against dark charcoal cards.

### Tertiary

Mint `tertiary` (`#71D4C1`) supports existing tertiary controls. Semantic `info`, `success`, `warning`, and `danger` retain upstream meanings. The header and navigation Emergency controls use `danger` (`#FF879A`).

### Neutral

`screen-bg` (`#101118`) anchors the screen; `overlay-bg` (`#171921`), `card-bg` (`#161920`), and `elevated-bg` (`#252832`) distinguish native surface levels. `border` (`#353843`) separates edges and divides the circular jog wheel quadrants. `text` (`#F4F4F7`), `text-muted` (`#ADB0BD`), and `text-subtle` (`#A29CB7`) establish reading hierarchy. Button foregrounds are contrast-adjusted by the native component; shell `<ui_button text="">` buttons are used where an explicit child `<icon variant="danger">` must coexist with a `#text` label.

**The Semantic State Rule.** Use danger, warning, success, and info for their existing state meanings; violet identifies ordinary primary actions and active step/tab selection.

## Typography

Use upstream Noto Sans regular, light, and bold bitmap faces with Material Design Icons. No fallback stack or CSS scaling is defined by this native application. Frontmatter typography records the upstream Small tier used at 400×1280 and explicit portrait overrides (`K3DashboardWidget` registers Tier 3 fonts so `noto_sans_bold_40` and `noto_sans_bold_28` are available at Small/Medium breakpoints).

| Runtime role | Small | Medium | Purpose |
| --- | --- | --- | --- |
| font_heading | 20px regular | 26px regular | Screen and section headings |
| font_body | 14px regular | 18px regular | Values, action labels, and primary reading |
| font_small | 12px light | 16px light | Supporting labels and hints |
| font_xs | 10px light | 12px light | Compact metadata |

Portrait overrides use 40px bold (`noto_sans_bold_40`) for the Home `Print` button, 28px bold (`noto_sans_bold_28`) for the `K3` and `Control` screen headers and the three machine statistics values, 20px bold (`noto_sans_bold_20`) for `Cooling` and `One-Tap Macros` titles, 18px bold (`noto_sans_bold_18`) for Home action rows (`Move`, `Preheat`, `Extrude`) and Control `Position` values, 16px bold/regular (`noto_sans_bold_16` / `noto_sans_16`) for Control buttons and macro rows, 14px bold (`noto_sans_bold_14`) for uppercase group labels (`STATISTICS`, `POSITION`, `HOMING`, `AXIS CONTROLS`) and navigation labels, and 12px regular (`noto_sans_12`) for status and axis captions.

**The Native Hierarchy Rule.** Reuse upstream responsive font tokens, registered Noto Sans bitmap sizes, and MDI assets; do not introduce web fonts, a new display face, or an unrelated icon family.

## Layout

Responsive tiers use `min(width,height)`: Micro ≤272, Tiny ≤390, Small ≤460, Medium ≤550, Large ≤700, XLarge ≤1000, and XXLarge above 1000. These are inclusive narrow-axis limits, not browser media queries. Thus 400×1280 is Small and 480×800 is Medium. Runtime spacing/font/radius resolution is authoritative.

The Small spacing ladder is encoded in frontmatter. At Medium the same `space_xxs/xs/sm/md/lg/xl/2xl` roles resolve to 3/5/7/10/16/20/32px.

The exact 400×1280 Home default uses 10 columns × 28 rows (`small@10x28`). `k3/home-layout.json` places the composite `k3_dashboard` widget across the full `[0, 0, 10, 28]` grid and disables the 21 standalone automatic widgets so the portrait Home renders the reference vertical stack without overlapping auto-added tiles:

| Component inside `k3_dashboard` | Height | Purpose |
| --- | --- | --- |
| Printer card (`k3_printer_card`) | 536px | `K3` title + `Emergency` button, two 54px status cards (`State`, `Network` with Wi-Fi icon), and 388px printer frame (`20px` radius) with Annex K3 render and 40px temperature chips (`Nozzle`, `Bed`, `Chamber`) |
| Statistics card (`k3_statistics`) | 128px | `STATISTICS` heading and three equal columns: `Total Time` (`k3_total_time`), `Print Count` (`k3_print_count`), and `Filament Usage` (`k3_filament_used` in meters) |
| Primary Print CTA (`k3_print_files`) | 90px | Full-width violet `Print` button (`#8047FF`) opening `PrintSelect` |
| Action rows (`Move`, `Preheat`, `Extrude`) | 3 × 56px | Full-width dark cards (`#161920`) with lavender icon, 18px bold label, and trailing chevron |

This user-layer default preserves edited layouts and other resolution defaults. The 480×800 home retains its upstream composition rather than inheriting the 400×1280 `k3_dashboard` grid.

Portrait Controls (`ui_xml/portrait/controls_panel.xml`) keeps a fixed 48px header (`Control` title + 48px `Emergency` shell button) outside the vertical scroll container (`pad_bottom="148"` so scrolled content clears the floating dock):
- `POSITION`: three equal 64px cards (`X`, `Y`, `Z`).
- `HOMING` (108px card): three 48px buttons (`All` primary violet, `XY` and `Z` elevated dark).
- `AXIS CONTROLS` (422px card): four 44px step buttons (`5mm`, `10mm`, `25mm`, `50mm` bound to `k3_jog_step`), an inline 224×224 circular XY jog wheel (`k3_jog_wheel`) with crosshairs, directional arrows (`k3_jog_yplus`, `k3_jog_yminus`, `k3_jog_xminus`, `k3_jog_xplus`), and a 74×74 center Home button (`k3_jog_home`) alongside a 72×224 `Z+`/`Z-` column, plus a 48px `Disable Motors` button.
- `Cooling` (272px card): `Part Fan` and `Aux Fan` blocks with live speed subjects (`k3_part_speed`, `k3_aux_speed`) and three 44px step buttons (`-10%`, `Off`, `+10%`).
- `One-Tap Macros` (content-height card): four 48px full-width macro buttons bound to the upstream macro slots.

Portrait navigation (`ui_xml/portrait/navigation_bar.xml` + `ui_xml/portrait/app_layout.xml`) renders as an inset 94%-width floating bottom dock (`24px` radius, `12px` bottom offset, `132px` normal height or `180px` when the 44px safety row for drying/Emergency is active) with four 96px main tabs (`Home`, `Print`, `Control`, `Settings`). To keep every upstream panel reachable without a second permanent navigation row, `ui_xml/portrait/settings_panel.xml` exposes `Move axes`, `Filament & Extrusion`, and `Printer tools` at the top of Settings.

## Elevation & Depth

The K3 preset uses tonal layering and restrained borders, with shadow intensity and opacity both zero. Its stored shadow offset is dormant while shadows are disabled. Borders use theme width 1 and opacity 60 on the native 0–255 opacity scale where applied; do not translate the stored value into a claimed 60 percent. Individual native components may override border treatment.

**The Tonal Depth Rule.** Separate resting surfaces with the existing background ladder and subtle `#353843` borders; the K3 preset has no visible drop shadows.

## Shapes

The theme stores radius size index 5, named Bold, rather than a raw five-pixel radius. In Micro/Tiny/Small/Medium/Large/XLarge/XXLarge order it resolves to 4/5/8/10/16/18/20px. Portrait cards, action rows, and the `Print` CTA locally use `16px`, the inner printer frame and temperature chips use `20px`, selected navigation tabs use `16px`, the floating navigation dock uses `24px`, and the 224px XY jog wheel uses `112px` (`37px` for its 74px center Home button).

## Components

### Buttons

Use native `ui_button` variants: primary, secondary, tertiary, danger, success, warning, ghost, transparent, and outline as applicable. Native pressed, focus, disabled opacity, and contrast handling remain authoritative. Portrait-specific heights are 90px for `Print`, 56px for Home action rows (`Move`, `Preheat`, `Extrude`), 48px for header `Emergency`, `Homing`, `Disable Motors`, and `One-Tap Macros`, and 44px for `Axis Controls` step selectors, fan `-10%`/`Off`/`+10%` buttons, and navigation safety controls.

### Cards / Containers

Use `ui_card` with `#161920` card-background tonal separation and `#353843` borders (`border_opa="90"` on portrait cards); portrait Control cards use the explicit 16px radius and 14px padding. Portrait control cards stretch to available width and grow with content where needed (such as `One-Tap Macros`).

### Inputs / Fields

Retain upstream `ui_text_input` and keyboard behavior, theme-based surfaces, and native focus/error states. No new field treatment was established by this portrait extension.

### Navigation

Retain the native navigation bar, active icon emphasis, and orientation behavior inside the 94%-width floating portrait dock. Keep selected and unselected states tied to upstream state subjects, with `#3B2B6D` selected pill fill and `#8047FF` border on the active tab.

### Position, Homing, and Axis Controls

Axis values align in three 64px cards (`X`, `Y`, `Z`). Homing buttons (`All`, `XY`, `Z`), the inline 224px circular XY jog wheel, `Z+`/`Z-`, and `Disable Motors` route through `MotionPanel` (`jog_axis_distance`) and `ControlsPanel` callbacks while preserving operation-in-progress and connection guards.

### Cooling, Macros, and Emergency

Cooling fan buttons adjust `Part Fan` and `Aux Fan` in 10% increments or turn them off via `k3_fan_adjust` and `MoonrakerAPI::set_fan_speed`. One-Tap Macros use 48px elevated buttons bound to upstream macro slots. Header `Emergency` on Home and Control uses a 48px shell `ui_button` with a `#danger` (`#FF879A`) alert icon, `#text` (`#F4F4F7`) label, and translucent danger fill/border, invoking the existing `emergency_stop_clicked` confirmation flow.

### Home Dashboard and Statistics

`K3DashboardWidget` composes `PrinterImageWidget` and `PrintStatsWidget` inside `panel_widget_k3_dashboard.xml`. Machine statistics display three columns from Moonraker history (`Total Time`, `Print Count`, and `Filament Usage` formatted in meters as `%.1fm` because Moonraker reports filament length in millimeters rather than mass).

## Do's and Don'ts

### Do:

- **Do** keep the Emergency action visible in the fixed header on both Home and portrait Controls.
- **Do** route inline jog wheel and fan step controls through the native `MotionPanel` and `MoonrakerAPI` safety paths.
- **Do** report Moonraker filament usage honestly in meters (`m`) rather than inventing filament density to show kilograms.
- **Do** preserve user-edited home layouts, other resolution defaults, and all upstream panel reachability (via Settings rows when using the 4-tab dock).
- **Do** review both first-view and scrolled content at 400×1280 and 480×800.

### Don't:

- **Don’t** apply the 400×1280 `k3_dashboard` home grid to every display resolution.
- **Don’t** treat mock simulator screenshots or ARM64 cross-builds as physical touch, printer, or display validation.
- **Don’t** replace semantic state colors (`danger`, `warning`, `success`, `info`) with violet for decoration.
- **Don’t** rely on `ui_button` default ghost label/icon recoloring when a button needs a `#danger` icon paired with a `#text` label; use a shell `<ui_button text="">` with explicit children.
