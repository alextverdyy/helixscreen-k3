// SPDX-License-Identifier: GPL-3.0-or-later
// Native reference composition: existing image and history widgets retain their lifecycle.
#include "printer_image_widget.h"
#include "print_stats_widget.h"
#include "panel_widget_registry.h"
#include "widget_subjects.h"
#include "app_globals.h"
#include "asset_manager.h"
#include "printer_state.h"
#include "ui_panel_motion.h"
#include "ui_nav.h"
#include "ui_error_reporting.h"
#include "ui_event_safety.h"
#include "i_moonraker_api.h"
#include <algorithm>
#include <cstring>

namespace {
helix::WidgetSubjects subjects{"K3ReferenceSubjects"};
lv_subject_t step{}, part_available{}, aux_available{}, part_text{}, aux_text{};
char part_buf[24]{}, aux_buf[24]{};
constexpr int distances[] = {5, 10, 25, 50};

const helix::FanInfo* role_fan(bool aux) {
    auto& state = get_printer_state().fan_state();
    const auto primary = state.classify_primary_fans();
    const auto& name = aux ? primary.aux : primary.part;
    for (const auto& fan : state.get_fans())
        if (fan.object_name == name && fan.is_controllable) return &fan;
    return nullptr;
}
void init_subjects() {
    subjects.ensure_init([] {
        UI_MANAGED_SUBJECT_INT(step, 1, "k3_jog_step", subjects);
        UI_MANAGED_SUBJECT_INT(part_available, 0, "k3_part_available", subjects);
        UI_MANAGED_SUBJECT_INT(aux_available, 0, "k3_aux_available", subjects);
        UI_MANAGED_SUBJECT_STRING(part_text, part_buf, "Unavailable", "k3_part_speed", subjects);
        UI_MANAGED_SUBJECT_STRING(aux_text, aux_buf, "Unavailable", "k3_aux_speed", subjects);
    });
}
void fan_adjust(lv_event_t* e) {
    LVGL_SAFE_EVENT_CB_BEGIN("K3 fan adjustment");
    const char* command = static_cast<const char*>(lv_event_get_user_data(e));
    if (!command) return;
    const auto* fan = role_fan(command[0] == 'a');
    auto* api = get_moonraker_api();
    if (!fan || !api) return;
    const int value = command[1] == '0' ? 0 : std::clamp(fan->speed_percent + (command[1] == '+' ? 10 : -10), 0, 100);
    api->set_fan_speed(fan->object_name, value, [] {}, [](const MoonrakerError& err) {
        helix::ui::notify_error_tr(TR_NOOP("Fan control failed: {}"), err);
    });
    LVGL_SAFE_EVENT_CB_END();
}
void jog(lv_event_t* e) {
    LVGL_SAFE_EVENT_CB_BEGIN("K3 jog");
    const char* command = static_cast<const char*>(lv_event_get_user_data(e));
    if (!command) return;
    const int index = std::clamp(lv_subject_get_int(&step), 0, 3);
    get_global_motion_panel().jog_axis_distance(command[0], distances[index] * (command[1] == '-' ? -1 : 1));
    LVGL_SAFE_EVENT_CB_END();
}
}

void k3_refresh_fans() {
    if (!subjects.initialized()) return;
    for (bool aux : {false, true}) {
        const auto* fan = role_fan(aux);
        lv_subject_set_int(aux ? &aux_available : &part_available, fan ? 1 : 0);
        char text[24];
        if (fan) snprintf(text, sizeof(text), "%d%%", fan->speed_percent);
        else snprintf(text, sizeof(text), "%s", "Unavailable");
        lv_subject_copy_string(aux ? &aux_text : &part_text, text);
    }
}

namespace helix {
class K3DashboardWidget final : public PanelWidget {
    PrinterImageWidget image_;
    PrintStatsWidget stats_;
public:
    K3DashboardWidget() { AssetManager::register_fonts_for_tier(3); }
    ~K3DashboardWidget() override { detach(); }
    const char* id() const override { return "k3_dashboard"; }
    void attach(lv_obj_t* obj, lv_obj_t* screen) override {
        if (auto* image = lv_obj_find_by_name(obj, "k3_printer_card")) image_.attach_tile(image, screen);
        if (auto* stats = lv_obj_find_by_name(obj, "k3_statistics")) stats_.attach_tile(stats, screen);
        on_size_changed(10, 28, lv_obj_get_width(obj), lv_obj_get_height(obj));
    }
    void detach() override { image_.detach_tile(); stats_.detach_tile(); }
    void on_size_changed(int, int, int width, int) override {
        image_.on_size_changed(10, 14, width, 534);
        stats_.on_size_changed(10, 3, width, 126);
    }
    void on_activate() override { image_.on_activate(); stats_.on_activate(); }
    void on_deactivate() override { stats_.on_deactivate(); }
};
void register_k3_dashboard_widget() {
    register_widget_factory("k3_dashboard", [](const std::string&) { return std::make_unique<K3DashboardWidget>(); });
    register_widget_subjects("k3_dashboard", init_subjects);
    lv_xml_register_event_cb(nullptr, "k3_jog", jog);
    lv_xml_register_event_cb(nullptr, "k3_fan_adjust", fan_adjust);
    lv_xml_register_event_cb(nullptr, "k3_step", [](lv_event_t* e) {
        const char* value = static_cast<const char*>(lv_event_get_user_data(e));
        if (value && value[0] >= '0' && value[0] <= '3') lv_subject_set_int(&step, value[0] - '0');
    });
    lv_xml_register_event_cb(nullptr, "k3_print", [](lv_event_t*) { helix::nav::set_active(PanelId::PrintSelect); });
    lv_xml_register_event_cb(nullptr, "k3_extrude", [](lv_event_t*) { helix::nav::set_active(PanelId::Filament); });
    lv_xml_register_event_cb(nullptr, "k3_tools", [](lv_event_t*) { helix::nav::set_active(PanelId::Advanced); });
    lv_xml_register_event_cb(nullptr, "k3_move", [](lv_event_t* e) { get_global_motion_panel().show(lv_obj_get_screen(lv_event_get_target_obj(e))); });
}
}
