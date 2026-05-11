use re_log_types::{
    AbsoluteTimeRange, EntityPath, TimeCell, TimeInt, TimeReal, TimeType, TimelineName,
    TimestampFormat,
};
use re_time_ruler::TimeRangesUi;
use re_ui::{Help, UiExt as _, icons};
use re_viewer_context::{
    DataResultInteractionAddress, IdentifiedViewSystem as _, Item, TimeControlCommand, TimeView,
    ViewClass, ViewClassLayoutPriority, ViewClassRegistryError, ViewId, ViewQuery,
    ViewSpawnHeuristics, ViewState, ViewStateExt as _, ViewSystemExecutionError, ViewerContext,
};

use crate::data::{StatusLane, StatusLanesData};

// Layout constants (in screen pixels).
const LANE_BAND_HEIGHT: f32 = 22.0;
const LANE_LABEL_HEIGHT: f32 = 14.0;
const LANE_GAP: f32 = 4.0;
const LANE_TOTAL_HEIGHT: f32 = LANE_BAND_HEIGHT + LANE_LABEL_HEIGHT + LANE_GAP;

const TIME_AXIS_HEIGHT: f32 = 20.0;
const TOP_MARGIN: f32 = 4.0;

/// View state for pan/zoom.
#[derive(Default)]
struct StatusViewState {
    /// Visible time range, in the same representation as the timeline panel.
    /// `None` means "fit all data" — populated on the next frame from the data range.
    time_view: Option<TimeView>,

    /// The timeline we last rendered. When the active timeline changes,
    /// we reset `time_view` so the view auto-fits to the new data.
    active_timeline: Option<TimelineName>,

    /// `true` if the current primary-button press landed on a phase rectangle.
    /// A phase press selects the phase's entity and does NOT move the time cursor;
    /// a press on empty space drags the time cursor.
    press_on_phase: bool,
}

impl re_byte_size::SizeBytes for StatusViewState {
    fn heap_size_bytes(&self) -> u64 {
        let Self {
            time_view: _,
            active_timeline,
            press_on_phase: _,
        } = self;

        active_timeline.heap_size_bytes()
    }
}

impl ViewState for StatusViewState {
    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn as_any_mut(&mut self) -> &mut dyn std::any::Any {
        self
    }
}

#[derive(Default)]
pub struct StatusView;

impl ViewClass for StatusView {
    fn identifier() -> re_sdk_types::ViewClassIdentifier {
        "Status".into()
    }

    fn display_name(&self) -> &'static str {
        "Status"
    }

    fn icon(&self) -> &'static re_ui::Icon {
        // TODO(RR-4264): Add a proper icon.
        &icons::VIEW_GENERIC
    }

    fn new_state(&self) -> Box<dyn ViewState> {
        Box::<StatusViewState>::default()
    }

    fn help(&self, _os: egui::os::OperatingSystem) -> Help {
        Help::new("Status view")
            .markdown("Shows status transitions as horizontal colored lanes over time.")
    }

    fn on_register(
        &self,
        system_registry: &mut re_viewer_context::ViewSystemRegistrator<'_>,
    ) -> Result<(), ViewClassRegistryError> {
        system_registry.register_visualizer::<crate::StatusVisualizer>()
    }

    fn preferred_tile_aspect_ratio(&self, _state: &dyn ViewState) -> Option<f32> {
        Some(2.5)
    }

    fn layout_priority(&self) -> ViewClassLayoutPriority {
        ViewClassLayoutPriority::Low
    }

    fn spawn_heuristics(
        &self,
        ctx: &ViewerContext<'_>,
        include_entity: &dyn Fn(&EntityPath) -> bool,
    ) -> re_viewer_context::ViewSpawnHeuristics {
        re_tracing::profile_function!();

        // Show every status in a single view by default.
        if ctx
            .indicated_entities_per_visualizer
            .get(&crate::StatusVisualizer::identifier())
            .is_some_and(|entities| entities.iter().any(include_entity))
        {
            ViewSpawnHeuristics::root()
        } else {
            ViewSpawnHeuristics::empty()
        }
    }

    fn selection_ui(
        &self,
        _ctx: &ViewerContext<'_>,
        _ui: &mut egui::Ui,
        _state: &mut dyn ViewState,
        _space_origin: &EntityPath,
        _view_id: ViewId,
    ) -> Result<(), ViewSystemExecutionError> {
        Ok(())
    }

    fn ui(
        &self,
        ctx: &ViewerContext<'_>,
        _missing_chunk_reporter: &re_viewer_context::MissingChunkReporter,
        ui: &mut egui::Ui,
        state: &mut dyn ViewState,
        query: &ViewQuery<'_>,
        system_output: re_viewer_context::SystemExecutionOutput,
    ) -> Result<(), ViewSystemExecutionError> {
        re_tracing::profile_function!();

        let state = state.downcast_mut::<StatusViewState>()?;

        // Reset the view when the active timeline changes.
        if state.active_timeline.as_ref() != Some(&query.timeline) {
            state.active_timeline = Some(query.timeline);
            state.time_view = None;
        }

        // Collect all lanes from all visualizers.
        let all_lanes: Vec<&StatusLane> = system_output
            .iter_visualizer_data::<StatusLanesData>()
            .flat_map(|d| d.lanes.iter())
            .collect();

        if all_lanes.is_empty() {
            ui.centered_and_justified(|ui| {
                ui.label("No status data. Add a visualizer that produces StatusLanesData.");
            });
            return Ok(());
        }

        // Compute data time range.
        let (data_min, data_max) = data_time_range(&all_lanes);

        // Auto-fit on first frame.
        // TODO(aedm): The calculation of the end time is incorrect since status transitions don't have an end time.
        //      We should use an estimation so that the latest state is still somewhat visible. Maybe also consider
        //      the density of states? An idea is to keep as much space for the last state as the average state
        //      duration on the screen.
        if state.time_view.is_none() {
            let padding = (data_max - data_min).max(1.0) * 0.05;
            let min = data_min - padding;
            let max = data_max + padding;
            state.time_view = Some(TimeView {
                min: TimeReal::from(min),
                time_spanned: max - min,
            });
        }

        let Some(mut time_view) = state.time_view else {
            return Ok(());
        };

        // Allocate the full available rect.
        let (rect, response) =
            ui.allocate_exact_size(ui.available_size(), egui::Sense::click_and_drag());

        if !ui.is_rect_visible(rect) {
            return Ok(());
        }

        // Layout: ruler at the top, lanes below.
        let time_axis_rect = egui::Rect::from_min_max(
            rect.left_top(),
            egui::pos2(rect.right(), rect.top() + TIME_AXIS_HEIGHT),
        );
        let lanes_rect = egui::Rect::from_min_max(
            egui::pos2(rect.left(), rect.top() + TIME_AXIS_HEIGHT),
            rect.right_bottom(),
        );

        // Build the time↔screen map. A single contiguous segment matches today's
        // Status view behavior (no gap collapsing).
        let data_segment = AbsoluteTimeRange::new(
            TimeInt::saturated_temporal_i64(data_min as i64),
            TimeInt::saturated_temporal_i64(data_max.ceil() as i64),
        );
        let time_ranges_ui = TimeRangesUi::new(
            rect.x_range(),
            time_view,
            std::slice::from_ref(&data_segment),
        );

        let current_time = TimeReal::from(query.latest_at.as_i64() as f64);
        let cursor_x = time_ranges_ui.x_from_time_f32(current_time);

        // On primary press, remember whether it landed on a phase. A phase press
        // selects the entity; a press on empty space drags the time cursor.
        if ui.input(|i| i.pointer.primary_pressed()) {
            state.press_on_phase = response
                .interact_pointer_pos()
                .is_some_and(|pos| hit_test_phase(pos, lanes_rect, &all_lanes, &time_ranges_ui));
        }

        // While the primary button is active on the view and the press started on
        // empty space, move the time cursor to the pointer. Using primary_pressed /
        // primary_down / primary_released mirrors `re_time_panel` so that the cursor
        // jumps on press and then follows during a drag.
        let primary_active = response.hovered()
            && ui.input(|i| {
                i.pointer.primary_pressed()
                    || i.pointer.primary_down()
                    || i.pointer.primary_released()
            });
        let dragging_cursor = primary_active && !state.press_on_phase;
        if dragging_cursor
            && let Some(pos) = response.interact_pointer_pos()
            && let Some(time) = time_ranges_ui.time_from_x_f32(pos.x)
        {
            ctx.send_time_commands([TimeControlCommand::Pause, TimeControlCommand::SetTime(time)]);
        }

        // Pan: right- or middle-click drag, plus two-finger touchpad horizontal scroll.
        // Cmd+scroll is routed to `zoom_delta` by egui, so it won't double-fire here.
        let mut pan_dx = 0.0;
        if response.dragged_by(egui::PointerButton::Secondary)
            || response.dragged_by(egui::PointerButton::Middle)
        {
            pan_dx += response.drag_delta().x;
            ui.ctx().set_cursor_icon(egui::CursorIcon::AllScroll);
        }
        if response.hovered() {
            pan_dx += ui.input(|i| i.smooth_scroll_delta.x);
        }
        if pan_dx != 0.0
            && let Some(new_view) = time_ranges_ui.pan(-pan_dx)
        {
            time_view = new_view;
        }

        // Ctrl/Cmd + scroll to zoom.
        let zoom_delta = ui.input(|i| i.zoom_delta());
        if zoom_delta != 1.0
            && response.hovered()
            && let Some(pointer_pos) = ui.input(|i| i.pointer.hover_pos())
            && let Some(new_view) = time_ranges_ui.zoom_at(pointer_pos.x, zoom_delta)
        {
            time_view = new_view;
        }
        state.time_view = Some(time_view);

        // Background.
        let painter = ui.painter_at(rect);
        painter.rect_filled(rect, 0.0, ui.style().visuals.extreme_bg_color);

        // Draw the time ruler at the top.
        let time_type = ctx
            .time_ctrl
            .timeline()
            .map_or(TimeType::Sequence, |tl| tl.typ());
        let timestamp_format = ctx.app_options().timestamp_format;
        re_time_ruler::paint_time_ranges_and_ticks(
            &time_ranges_ui,
            ui,
            &painter.with_clip_rect(time_axis_rect),
            time_axis_rect.y_range(),
            time_type,
            timestamp_format,
        );
        // Separator between ruler and lanes.
        painter.line_segment(
            [time_axis_rect.left_bottom(), time_axis_rect.right_bottom()],
            egui::Stroke::new(1.0, ui.style().visuals.weak_text_color()),
        );

        // Draw lanes.
        let label_color = ui.style().visuals.text_color();
        for (lane_idx, lane) in all_lanes.iter().enumerate() {
            paint_lane(
                ui,
                &painter,
                lanes_rect,
                lane_idx,
                lane,
                &time_ranges_ui,
                time_type,
                timestamp_format,
                label_color,
            );
        }

        // Handle selection: determine what's under the pointer (lane entity or view).
        let hover_pos = ui.input(|i| i.pointer.hover_pos());
        let hovered_lane = hover_pos.and_then(|pos| hovered_lane(pos, lanes_rect, &all_lanes));

        // Time cursor — uses the same triangle-headed style as the time panel.
        if let Some(cursor_x) = cursor_x
            && rect.x_range().contains(cursor_x)
        {
            let cursor_response = if dragging_cursor || hovered_lane.is_none() {
                Some(&response)
            } else {
                None
            };
            ui.paint_time_cursor(&painter, cursor_response, cursor_x, rect.y_range());
        }

        let interacted_item = if let Some(entity_path) = hovered_lane {
            Item::DataResult(DataResultInteractionAddress::from_entity_path(
                query.view_id,
                entity_path.clone(),
            ))
        } else {
            Item::View(query.view_id)
        };
        ctx.handle_select_hover_drag_interactions(&response, interacted_item, false);

        Ok(())
    }
}

/// Compute the (min, max) time range across all lanes.
fn data_time_range(lanes: &[&StatusLane]) -> (f64, f64) {
    let mut min = f64::MAX;
    let mut max = f64::MIN;
    for lane in lanes {
        for phase in &lane.phases {
            let t = phase.start_time as f64;
            min = min.min(t);
            max = max.max(t);
        }
    }
    if min > max {
        (0.0, 1.0)
    } else if (max - min).abs() < f64::EPSILON {
        (min - 0.5, max + 0.5)
    } else {
        (min, max)
    }
}

/// Returns the entity path of the lane under `pos`, if any.
fn hovered_lane<'a>(
    pos: egui::Pos2,
    lanes_rect: egui::Rect,
    lanes: &'a [&'a StatusLane],
) -> Option<&'a EntityPath> {
    lanes.iter().enumerate().find_map(|(lane_idx, lane)| {
        let y_top =
            lanes_rect.top() + TOP_MARGIN + lane_idx as f32 * LANE_TOTAL_HEIGHT + LANE_LABEL_HEIGHT;
        let y_bottom = y_top + LANE_BAND_HEIGHT;
        (pos.y >= y_top && pos.y <= y_bottom).then_some(&lane.entity_path)
    })
}

/// Returns `true` if `pos` lies inside any visible phase rectangle.
fn hit_test_phase(
    pos: egui::Pos2,
    lanes_rect: egui::Rect,
    lanes: &[&StatusLane],
    time_ranges_ui: &TimeRangesUi,
) -> bool {
    for (lane_idx, lane) in lanes.iter().enumerate() {
        let y_top = lanes_rect.top() + TOP_MARGIN + lane_idx as f32 * LANE_TOTAL_HEIGHT;
        let band_y_top = y_top + LANE_LABEL_HEIGHT;
        let band_y_bottom = band_y_top + LANE_BAND_HEIGHT;
        if pos.y < band_y_top || pos.y > band_y_bottom {
            continue;
        }
        for (i, phase) in lane.phases.iter().enumerate() {
            if !phase.visible {
                continue;
            }
            let Some(x_start) =
                time_ranges_ui.x_from_time_f32(TimeReal::from(phase.start_time as f64))
            else {
                continue;
            };
            let x_start = x_start.max(lanes_rect.left());
            let x_end = if let Some(next) = lane.phases.get(i + 1) {
                time_ranges_ui
                    .x_from_time_f32(TimeReal::from(next.start_time as f64))
                    .unwrap_or_else(|| lanes_rect.right())
            } else {
                lanes_rect.right()
            }
            .min(lanes_rect.right());
            if x_end <= x_start {
                continue;
            }
            if pos.x >= x_start && pos.x <= x_end {
                return true;
            }
        }
    }
    false
}

/// Paint a single lane (label + colored band of phases) and show tooltips on hover.
#[expect(clippy::too_many_arguments)]
fn paint_lane(
    ui: &egui::Ui,
    painter: &egui::Painter,
    lanes_rect: egui::Rect,
    lane_idx: usize,
    lane: &StatusLane,
    time_ranges_ui: &TimeRangesUi,
    time_type: TimeType,
    timestamp_format: TimestampFormat,
    label_color: egui::Color32,
) {
    let y_top = lanes_rect.top() + TOP_MARGIN + lane_idx as f32 * LANE_TOTAL_HEIGHT;
    let label_rect = egui::Rect::from_min_size(
        egui::pos2(lanes_rect.left() + 4.0, y_top),
        egui::vec2(lanes_rect.width() - 8.0, LANE_LABEL_HEIGHT),
    );
    let band_y_top = y_top + LANE_LABEL_HEIGHT;
    let band_y_bottom = band_y_top + LANE_BAND_HEIGHT;

    // Lane label.
    painter.text(
        label_rect.left_top(),
        egui::Align2::LEFT_TOP,
        &lane.label,
        egui::FontId::proportional(11.0),
        label_color,
    );

    let hover_pos = ui.input(|i| i.pointer.hover_pos());

    // Phases.
    for (i, phase) in lane.phases.iter().enumerate() {
        if !phase.visible {
            continue;
        }
        let Some(x_start) = time_ranges_ui.x_from_time_f32(TimeReal::from(phase.start_time as f64))
        else {
            continue;
        };
        let next_phase = lane.phases.get(i + 1);
        let x_end = if let Some(next) = next_phase {
            time_ranges_ui
                .x_from_time_f32(TimeReal::from(next.start_time as f64))
                .unwrap_or_else(|| lanes_rect.right())
        } else {
            lanes_rect.right()
        };

        // Clip to visible area.
        let x_start = x_start.max(lanes_rect.left());
        let x_end = x_end.min(lanes_rect.right());

        if x_end <= x_start {
            continue;
        }

        let phase_rect = egui::Rect::from_min_max(
            egui::pos2(x_start, band_y_top),
            egui::pos2(x_end, band_y_bottom),
        );

        // Filled band. Dim when not hovered.
        let hovered = hover_pos.is_some_and(|pos| phase_rect.contains(pos));
        #[expect(clippy::disallowed_methods)]
        // Data-driven visualization color, not a UI theme color.
        let fill = if hovered {
            phase.color
        } else {
            let [r, g, b, _] = phase.color.to_array();
            egui::Color32::from_rgba_unmultiplied(r, g, b, 200)
        };
        painter.add(egui::epaint::RectShape::new(
            phase_rect,
            0.0,
            fill,
            egui::Stroke::NONE,
            egui::StrokeKind::Outside,
        ));

        // Phase label (clipped to band width).
        let text_width = x_end - x_start - 6.0;
        if text_width > 10.0 {
            painter.with_clip_rect(phase_rect).text(
                egui::pos2(x_start + 4.0, band_y_top + 3.0),
                egui::Align2::LEFT_TOP,
                &phase.label,
                egui::FontId::proportional(12.0),
                readable_text_color(phase.color),
            );
        }

        // Tooltip on hover.
        if let Some(pos) = hover_pos
            && phase_rect.contains(pos)
        {
            let start = TimeCell::new(time_type, phase.start_time).format(timestamp_format);
            egui::Tooltip::always_open(
                ui.ctx().clone(),
                ui.layer_id(),
                egui::Id::new("state_tooltip"),
                egui::PopupAnchor::Pointer,
            )
            .show(|ui| {
                ui.label(&phase.label);
                ui.add_space(4.0);
                let weak = ui.visuals().weak_text_color();
                let small = egui::FontId::proportional(11.0);
                ui.label(
                    egui::RichText::new(format!("Start: {start}"))
                        .font(small.clone())
                        .color(weak),
                );
                if let Some(next) = next_phase {
                    let end = TimeCell::new(time_type, next.start_time).format(timestamp_format);
                    ui.label(
                        egui::RichText::new(format!("End: {end}"))
                            .font(small)
                            .color(weak),
                    );
                }
            });
        }
    }
}

/// Choose white or black text depending on background luminance.
fn readable_text_color(bg: egui::Color32) -> egui::Color32 {
    if bg.intensity() > 0.6 {
        egui::Color32::BLACK
    } else {
        egui::Color32::WHITE
    }
}

#[test]
fn test_help_view() {
    re_test_context::TestContext::test_help_view(|ctx| StatusView.help(ctx));
}
