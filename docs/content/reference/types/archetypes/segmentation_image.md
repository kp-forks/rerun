---
title: "SegmentationImage"
---
<!-- DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/docs/website.rs -->

An image made up of integer [`components.ClassId`](https://rerun.io/docs/reference/types/components/class_id)s.

Each pixel corresponds to a [`components.ClassId`](https://rerun.io/docs/reference/types/components/class_id) that will be mapped to a color based on [`archetypes.AnnotationContext`](https://rerun.io/docs/reference/types/archetypes/annotation_context).

In the case of floating point images, the label will be looked up based on rounding to the nearest
integer value.

Use [`archetypes.AnnotationContext`](https://rerun.io/docs/reference/types/archetypes/annotation_context) to associate each class with a color and a label.

## Fields
### Required
* `buffer`: [`ImageBuffer`](../components/image_buffer.md)
* `format`: [`ImageFormat`](../components/image_format.md)

### Optional
* `opacity`: [`Opacity`](../components/opacity.md)
* `draw_order`: [`DrawOrder`](../components/draw_order.md)


## Can be shown in
* [Spatial2DView](../views/spatial2d_view.md)
* [Spatial3DView](../views/spatial3d_view.md) (if logged under a projection)
* [DataframeView](../views/dataframe_view.md)

## API reference links
 * 🌊 [C++ API docs for `SegmentationImage`](https://ref.rerun.io/docs/cpp/stable/structrerun_1_1archetypes_1_1SegmentationImage.html)
 * 🐍 [Python API docs for `SegmentationImage`](https://ref.rerun.io/docs/python/stable/common/archetypes#rerun.archetypes.SegmentationImage)
 * 🦀 [Rust API docs for `SegmentationImage`](https://docs.rs/rerun/latest/rerun/archetypes/struct.SegmentationImage.html)

## Example

### Simple segmentation image

snippet: archetypes/segmentation_image_simple

<picture data-inline-viewer="snippets/segmentation_image_simple">
  <source media="(max-width: 480px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/480w.png">
  <source media="(max-width: 768px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/768w.png">
  <source media="(max-width: 1024px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/1024w.png">
  <source media="(max-width: 1200px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/1200w.png">
  <img src="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/full.png">
</picture>

