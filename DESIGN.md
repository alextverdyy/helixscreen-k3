---
name: HelixScreen K3
description: Native LVGL printer controls with charcoal surfaces and violet actions.
colors:
  screen-bg: "#101116"
  overlay-bg: "#171921"
  card-bg: "#1B1D27"
  elevated-bg: "#292C3B"
  border: "#454354"
  text: "#F5F3FF"
  text-muted: "#B9B5CC"
  text-subtle: "#A29CB7"
  primary: "#7946E8"
  secondary: "#C4B5FD"
  tertiary: "#71D4C1"
  info: "#98C8FF"
  success: "#78D6A3"
  warning: "#F5C879"
  danger: "#FF879A"
  focus: "#C4B5FD"
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
  portrait-title:
    fontFamily: "Noto Sans"
    fontSize: "28px"
    fontWeight: 700
  portrait-section:
    fontFamily: "Noto Sans"
    fontSize: "18px"
    fontWeight: 700
  portrait-hero:
    fontFamily: "Noto Sans"
    fontSize: "24px"
    fontWeight: 700
  portrait-action:
    fontFamily: "Noto Sans"
    fontSize: "16px"
    fontWeight: 400
  portrait-nav-label:
    fontFamily: "Noto Sans"
    fontSize: "12px"
    fontWeight: 700
rounded:
  bold-small: "8px"
  bold-medium: "10px"
  portrait-card: "16px"
  portrait-chip: "20px"
  portrait-selection: "12px"
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
  portrait-action-inset: "16px"
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
    backgroundColor: "{colors.elevated-bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.portrait-card}"
    typography: "{typography.portrait-section}"
  portrait-print-button:
    backgroundColor: "{colors.primary}"
    typography: "{typography.portrait-hero}"
    height: "72px"
  portrait-navigation:
    backgroundColor: "{colors.card-bg}"
    rounded: "{rounded.portrait-card}"
    height: "128px"
  portrait-macro:
    typography: "{typography.portrait-action}"
    height: "52px"
---
# Design System: HelixScreen K3

## Overview

HelixScreen K3 extends the existing native embedded Linux/LVGL interface. Charcoal surfaces, violet actions and pale lavender icons follow the user’s portrait reference while retaining the upstream component vocabulary, typography and broad printer functionality.

The visual character is compact, calm and operational. Group related readings and actions in clear tonal containers; reserve semantic colors for the state or command they communicate. This documents the implemented K3 theme and portrait extension, not a replacement identity for upstream HelixScreen.

**Key Characteristics:**
- Charcoal tonal surfaces with violet action emphasis.
- Native Noto Sans text and Material Design Icons.
- Full-width portrait groups with reachable scrolling content.
- Existing command handlers, feature discovery and machine guards.

Provenance: `PRODUCT.md`; `assets/config/themes/defaults/k3-violet.json`; `ui_xml/globals.xml`; `include/border_radius_sizes.h`; `include/ui_breakpoint.h`; `k3/home-layout.json`; native XML overrides in `ui_xml/portrait/`; native `ui_button`, `ui_card` and `ui_text_input` implementations. The `annex-k3.png` printer image has provenance in `docs/images/k3/README.md`. Current simulator capture directories are `.impeccable/review/native-reference-400/` and `.impeccable/review/native-reference-480/`. Source extraction and mock captures establish implementation evidence, not pixel parity or physical hardware validation.

## Colors

The frontmatter records the actual K3 palette. Unprefixed colors are the dark preset; `light-` colors are the supplied light alternative, not colors to mix into the dark preset. Theme JSON remains the runtime authority; explicit user theme overrides remain valid.

### Primary

Violet `primary` marks primary actions, selection and chart emphasis. Pale lavender `secondary` supports secondary actions and iconography; `focus` supplies the existing focus treatment.

### Secondary

Lavender provides a softer action fill and supporting emphasis.

### Tertiary

Mint `tertiary` supports existing tertiary controls. Semantic `info`, `success`, `warning` and `danger` retain upstream meanings. The Emergency action uses danger.

### Neutral

`screen-bg` anchors the screen; `overlay-bg`, `card-bg` and `elevated-bg` distinguish native surface levels. `border` separates edges. `text`, `text-muted` and `text-subtle` establish reading hierarchy. Button foregrounds are contrast-adjusted by the native component; a universal white foreground is not a token.

**The Semantic State Rule.** Use danger, warning, success and info for their existing state meanings; violet identifies ordinary primary actions.

## Typography

Use upstream Noto Sans regular, light and bold bitmap faces with Material Design Icons. No fallback stack or CSS scaling is defined by this native application. Frontmatter typography records the upstream Small tier used at 400×1280 and explicit portrait overrides; it does not replace upstream responsive typography.

| Runtime role | Small | Medium | Purpose |
| --- | --- | --- | --- |
| font_heading | 20px regular | 26px regular | Screen and section headings |
| font_body | 14px regular | 18px regular | Values, action labels and primary reading |
| font_small | 12px light | 16px light | Supporting labels and hints |
| font_xs | 10px light | 12px light | Compact metadata |

Portrait overrides use 28px bold for the Control title, 18px bold for sections, positions and action rows, 24px bold for Print and the statistics hero, 16px regular for Control buttons, and 12px bold for navigation labels. Statistics use a 16px bold title and 14px regular support. Use the existing bold roles elsewhere where their native components require them. Preserve uppercase group labels where already implemented; do not uppercase all body copy. Line heights follow the native font metrics; no invented line-height or letter-spacing scale is specified.

**The Native Hierarchy Rule.** Reuse upstream responsive font tokens and MDI assets; do not introduce web fonts, a new display face or an unrelated icon family.

## Layout

Responsive tiers use `min(width,height)`: Micro ≤272, Tiny ≤390, Small ≤460, Medium ≤550, Large ≤700, XLarge ≤1000 and XXLarge above 1000. These are inclusive narrow-axis limits, not browser media queries. Thus 400×1280 is Small and 480×800 is Medium. Runtime spacing/font/radius resolution is authoritative.

The Small spacing ladder is encoded in frontmatter. At Medium the same `space_xxs/xs/sm/md/lg/xl/2xl` roles resolve to 3/5/7/10/16/20/32px. Keep token references in runtime XML instead of copying Small pixel values into new screens.

Portrait Controls uses full-width stacked cards. The Control header and 48px Emergency action remain outside the vertical scroller. Position uses three equal columns, followed by Z-offset and Motion/motor actions. Quick Actions places segmented homing above content-height macro rows; Temperature, Cooling, and Calibration & Tools follow. Outer padding and major gaps are 12px; cards use 14px padding, 12px internal gaps and 16px radii. Macro/homing actions are 52px high; the tools grid has a local 196px height. Motion opens the separate native panel with its existing controls.

The exact 400×1280 home default uses 10 columns ×28 rows (`small@10x28`). `k3/home-layout.json` defines these zero-based placements:

| Content | Start row | Rows | Columns |
| --- | --- | --- | --- |
| Printer image and live temperature chips | 0 | 13 | 10 |
| Machine statistics | 13 | 3 | 10 |
| Print status and file action | 16 | 4 | 10 |
| Motion | 20 | 2 | 10 |
| Preheat | 22 | 2 | 10 |
| Macros / Console | 24 | 2 | 5 each |
| Reserved empty space | 26 | 2 | 10 |

This user-layer default preserves edited layouts and other resolution defaults. Optional automatic widgets, including AMS, are disabled for this composition. The 480×800 home retains its upstream composition rather than inheriting the exact 400×1280 grid. Small-tier printer imagery uses 44px-high live temperature chips with 20px radii; chamber visibility follows hardware capability.

Portrait navigation has four main destinations (Home, Print, Control, Settings) in an 80px row, then a 44px secondary row for Filament, More and optional printer switching, separated by 4px: 128px total. Two fixed 44px root slots hold drying and Emergency state controls independently of navigation editor visibility. The editor uses 64px Add/Done buttons. Landscape retains the upstream leading navigation layout. Do not transfer portrait composition requirements to every upstream panel.

## Elevation & Depth

The K3 preset uses tonal layering and restrained borders, with shadow intensity and opacity both zero. Its stored shadow offset is dormant while shadows are disabled. Borders use theme width 1 and opacity 60 on the native 0–255 opacity scale where applied; do not translate the stored value into a claimed 60 percent. Individual native components may override border treatment.

**The Tonal Depth Rule.** Separate resting surfaces with the existing background ladder and borders; the K3 preset has no visible drop shadows.

## Shapes

The theme stores radius size index 5, named Bold, rather than a raw five-pixel radius. In Micro/Tiny/Small/Medium/Large/XLarge/XXLarge order it resolves to 4/5/8/10/16/18/20px. The frontmatter exposes the two reviewed portrait tier values. Portrait cards, action rows and navigation locally use 16px, temperature chips 20px, and selected navigation backgrounds 12px. Other cards and buttons share the native radius vocabulary; segmented homing buttons use square internal joins inside a clipped rounded group. Circular indicators are local component geometry, not an instruction to make every control a pill.

## Components

### Buttons

Use native `ui_button` variants: primary, secondary, tertiary, danger, success, warning, ghost, transparent and outline as applicable. The common Small button height is 48px; compact `button_height_sm` is 40px at Small and Medium, while the normal Medium height is 52px. These are distinct incumbent roles; do not claim every compact button has a 48px visible height. Native pressed, focus, disabled opacity and contrast handling remain authoritative. Portrait-specific heights are 72px for Print, 56px for Preheat, 52px for quick macros/homing, 44–48px for header Emergency, and 44px for idle secondary actions and navigation safety controls. There is no new browser hover language.

### Cards / Containers

Use `ui_card` with card-background tonal separation; portrait Control cards use the explicit 16px radius and 14px padding. Portrait control cards stretch to available width and grow with content. Preserve group titles, concise values and trailing native disclosure affordances. Avoid reserving a tall empty card for a single quick macro.

### Inputs / Fields

Retain upstream `ui_text_input` and keyboard behavior, theme-based surfaces and native focus/error states. No new field treatment was established by this portrait extension.

### Navigation

Retain the native navigation bar, active icon emphasis and orientation behavior. Keep selected and unselected states tied to upstream state subjects, not a visually hardcoded active tab. Preserve native icon transitions; this work introduces no new animation timing scale.

### Position and homing

Axis values align in three columns; the separate Quick Actions homing row uses upstream homed/unhomed colors and keeps operation-in-progress guards. Motion and motor actions retain their existing command routes and machine-state treatment.

### Quick Actions and Emergency

Quick macros use the native outline variant at 52px in content-height rows; configured Light cells retain secondary treatment. Control header Emergency uses a 48px ghost button (Home uses 44px) with danger text, border and translucent fill, invoking the existing handler and confirmation flow. Navigation Emergency remains a circular danger variant. Documentation does not broaden command authority or bypass safety state.

### Home actions and statistics

Motion, Macros and Console use horizontal native `k3_action_row` controls with elevated backgrounds, 16px radii, 16px horizontal padding and 18px bold labels. Preheat retains its native split-button and material selection at 56px height. Idle Print is 72px high, with native Reprint Last and conditional Job Queue below. Machine statistics bind the upstream weekly hero and lifetime support text; do not invent the reference image’s three metrics or turn mock values into labels. Active-print state, feature visibility and existing command handlers remain authoritative.

## Do's and Don'ts

### Do:

- **Do** keep the Emergency action above the portrait Controls scroll container.
- **Do** let quick macro content determine its card height.
- **Do** use runtime responsive tokens and existing native components.
- **Do** preserve user-edited home layouts, other resolution defaults and command guards.
- **Do** review both first-view and scrolled content at the target resolution.

### Don't:

- **Don’t** apply the 400×1280 home grid to every display.
- **Don’t** treat mock screenshots as physical touch, printer or display validation.
- **Don’t** replace semantic state colors with violet for decoration.
- **Don’t** turn incidental truncation, clipping or a transient mock value into a design rule.
