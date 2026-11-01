# HelixScreen K3

<!-- impeccable:product-schema 1 -->

## Platform

Native embedded Linux / LVGL. This is neither a web interface nor an iOS or Android redesign.

## Users and purpose

A Klipper printer owner operating a Waveshare touchscreen wants broad printer
features with easy customization. The user supplied dark violet portrait home
and controls references and delegated implementation choices to autonomous work
with Laya advice.

## Stack

Existing HelixScreen C++/LVGL application, runtime XML, JSON themes and Moonraker.
K3 configuration tools use Python's standard library.

## Constraints and evidence

Preserve upstream printer command handling, feature discovery and machine guards.
Keep Linux display mode detection as the default. Exact Waveshare SKU, host,
printer and physical touch alignment are unknown. Screenshots use mock data;
physical compatibility must not be claimed from simulator success.

## Customization

Use upstream Theme Editor, home widget editing, macro settings and printer image
selection. The additional CLI changes appearance/display settings with backups;
its exports exclude printer connections and credentials.
