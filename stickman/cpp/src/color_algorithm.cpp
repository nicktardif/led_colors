#define _USE_MATH_DEFINES
#include "../include/color_algorithm.h"

#include <math.h>

#include <algorithm>
#include <cmath>
#include <vector>

#include "../include/color_map.h"
#include "../include/rgb.h"
#include "../include/util.h"

const float POWER_SCALE = 0.07;  // 7% of max power

ColorMap* ColorAlgorithm::initialize_linear_color_map() {
  ColorMap* color_map = new LinearColorMap(bucket_size_);
  for (int i = 0; i < bucket_size_; i++) {
    const float percent = float(i) / bucket_size_;
    const RGB rgb = compute(percent, i, bucket_size_);
    color_map->add_color(i, i, bucket_size_, rgb);
  }
  return color_map;
}

ColorMap* ColorAlgorithm::initialize_full_color_map(const int leds_per_strip) {
  ColorMap* color_map = new FullColorMap(bucket_size_);
  for (int i = 0; i < bucket_size_; i++) {
    const float percent = float(i) / bucket_size_;
    for (int j = 0; j < bucket_size_; j++) {
      const RGB rgb = compute(percent, j, leds_per_strip);
      color_map->add_color(i, j, leds_per_strip, rgb);
    }
  }
  return color_map;
}

void ColorAlgorithm::reset_color_map() { color_map_ = NULL; }

Rainbow::Rainbow(const int bucket_size) { bucket_size_ = bucket_size; }

ColorMap* Rainbow::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_linear_color_map());
  }
  return color_map_.get();
}

RGB Rainbow::compute(float percent, int idx, int total_idx) const {
  const int RGB_SCALAR = 128;
  const int RGB_OFFSET = 128;

  float a = percent * 2 * M_PI;
  const float r_sin = sin(a);
  const float g_sin = sin(a - (2 * M_PI / 3));
  const float b_sin = sin(a - (4 * M_PI / 3));
  float r = POWER_SCALE * (r_sin * RGB_SCALAR + RGB_OFFSET);
  float g = POWER_SCALE * (g_sin * RGB_SCALAR + RGB_OFFSET);
  float b = POWER_SCALE * (b_sin * RGB_SCALAR + RGB_OFFSET);
  return RGB(r, g, b);
}

bool Rainbow::is_linear() const { return true; }

Pastel::Pastel(const int bucket_size, int red_scalar, int red_offset, int green_scalar,
               int green_offset, int blue_scalar, int blue_offset) {
  bucket_size_ = bucket_size;
  red_scalar_ = red_scalar;
  red_offset_ = red_offset;
  green_scalar_ = green_scalar;
  green_offset_ = green_offset;
  blue_scalar_ = blue_scalar;
  blue_offset_ = blue_offset;
}

ColorMap* Pastel::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_linear_color_map());
  }
  return color_map_.get();
}

RGB Pastel::compute(float percent, int idx, int total_idx) const {
  float a = percent * 2 * M_PI;
  float r_sin = sin(a);
  float g_sin = sin(a - (2 * M_PI / 3));
  float b_sin = sin(a - (4 * M_PI / 3));

  float r = POWER_SCALE * (r_sin * red_scalar_ + red_offset_);
  float g = POWER_SCALE * (g_sin * green_scalar_ + green_offset_);
  float b = POWER_SCALE * (b_sin * blue_scalar_ + blue_offset_);
  return RGB(r, g, b);
}
bool Pastel::is_linear() const { return true; }

Comet::Comet(const int bucket_size) { bucket_size_ = bucket_size; }

ColorMap* Comet::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_linear_color_map());
  }
  return color_map_.get();
}

RGB Comet::compute(float percent, int idx, int total_idx) const {
  const int RGB_SCALAR = 128;
  const int RGB_OFFSET = 128;

  // Split into groups and determine the relative intensity
  const int dot_count = 6;
  const int count_per_grouping = float(bucket_size_) / dot_count;
  const float dropoff_factor = 1.0 / (count_per_grouping * 2 / 3);
  const int bucket = int(round(percent * bucket_size_));
  const int mod = bucket % (int)(float(bucket_size_) / dot_count);
  const float intensity = std::max(1 - (mod * dropoff_factor), 0.0f);

  // Figure out the colors
  const float a = percent * M_PI * 2;
  const float r_sin = sin(a);
  const float g_sin = sin(a - (2 * M_PI / 3));
  const float b_sin = sin(a - (4 * M_PI / 3));
  const float r = POWER_SCALE * intensity * (r_sin * RGB_SCALAR + RGB_OFFSET);
  const float g = POWER_SCALE * intensity * (g_sin * RGB_SCALAR + RGB_OFFSET);
  const float b = POWER_SCALE * intensity * (b_sin * RGB_SCALAR + RGB_OFFSET);
  return RGB(r, g, b);
}

bool Comet::is_linear() const { return true; }

Yoyo::Yoyo(const int bucket_size, const int leds_per_strip, const int r_scalar, const int g_scalar,
           const int b_scalar)
    : leds_per_strip_(leds_per_strip), time_scale_(3.0) {
  bucket_size_ = bucket_size;
  r_scalar_ = r_scalar;
  g_scalar_ = g_scalar;
  b_scalar_ = b_scalar;
}

ColorMap* Yoyo::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_full_color_map(leds_per_strip_));
  }
  return color_map_.get();
}

RGB Yoyo::compute(float input_percent, int idx, int total_idx) const {
  float percent = fmod(input_percent * time_scale_, 1.0);
  // 2.0 is for the yoyo effect
  float offset_percent = percent * 2.0;
  bool reverse = false;
  if (offset_percent >= 1.0) {
    offset_percent = 2.0 - offset_percent;
    reverse = true;
  }

  // S curve for the head idx to simulate different speeds
  const float min_head_percent = 0.05;
  const float comet_range_percent = 0.9;
  const float min_head_idx = min_head_percent * total_idx;
  const int head_idx =
      std::round(s_curve(offset_percent) * total_idx * comet_range_percent + min_head_idx);

  // use a normal distribution to determine the tail length
  const float tail_length_percent = pow(gaussian_value(offset_percent), 1.5);
  const float tail_length_count = tail_length_percent * total_idx;

  float intensity = 0.0f;
  int offset_from_head = head_idx - idx;
  if (reverse) {
    offset_from_head = idx - head_idx;
  }
  if (offset_from_head >= 0 && offset_from_head <= tail_length_count) {
    intensity = 1 * pow(0.9, offset_from_head);
  }

  // give the head a bit extra
  const int pre_head_count = 4;
  if (offset_from_head <= 0 && offset_from_head > -1.0 * pre_head_count) {
    intensity = 1;
  }

  // adjust up due to the relative darkness of custom colors
  const float additional_scale_factor = 255.0 * 3 / (r_scalar_ + g_scalar_ + b_scalar_);

  float r = r_scalar_ * intensity * POWER_SCALE * additional_scale_factor;
  float g = g_scalar_ * intensity * POWER_SCALE * additional_scale_factor;
  float b = b_scalar_ * intensity * POWER_SCALE * additional_scale_factor;

  // highlight the head red
  // if (idx == head_idx) {
  //   r = 255 * POWER_SCALE;
  //   g = 0;
  //   b = 0;
  // }

  return RGB(r, g, b);
}
bool Yoyo::is_linear() const { return false; }

Wubwub::Wubwub(const int bucket_size, const int leds_per_strip,
               const std::vector<ColorPoint> colors)
    : color_gradient_(ColorGradient(colors)), leds_per_strip_(leds_per_strip) {
  bucket_size_ = bucket_size;
}

ColorMap* Wubwub::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_full_color_map(leds_per_strip_));
  }
  return color_map_.get();
}

RGB Wubwub::compute(float percent, int idx, int total_idx) const {
  const float wave_count = 3.0;

  const float idx_percent = float(idx) / total_idx;
  const float wave1_shape = (1.0 * cos(wave_count * M_PI * 2 * idx_percent) + 1) / 2.0;

  // Rotate the wave around 0.5
  float wave_value = 0;
  if (wave1_shape >= 0.5 && percent <= 0.5) {
    wave_value = wave1_shape - 4.0 * percent * abs(wave1_shape - 0.5);
  }
  if (wave1_shape >= 0.5 && percent > 0.5) {
    wave_value = wave1_shape - 4.0 * (1.0 - percent) * abs(wave1_shape - 0.5);
  }
  if (wave1_shape < 0.5 && percent <= 0.5) {
    wave_value = wave1_shape + 4.0 * percent * abs(wave1_shape - 0.5);
  }
  if (wave1_shape < 0.5 && percent > 0.5) {
    wave_value = wave1_shape + 4.0 * (1.0 - percent) * abs(wave1_shape - 0.5);
  }

  float wave_amp = wave_value;

  const RGB gradient_rgb = color_gradient_.getColorAtValue(wave_amp);
  const float r = gradient_rgb.red * POWER_SCALE;
  const float g = gradient_rgb.green * POWER_SCALE;
  const float b = gradient_rgb.blue * POWER_SCALE;

  return RGB(r, g, b);
}

bool Wubwub::is_linear() const { return false; }

Sparkshot::Sparkshot(const int bucket_size, const int leds_per_strip, const bool vary_intensity,
                     const std::vector<Shot> shots)
    : shots_(shots), vary_intensity_(vary_intensity) {
  bucket_size_ = bucket_size;
  leds_per_strip_ = leds_per_strip;
}

ColorMap* Sparkshot::get_color_map() {
  if (color_map_ == NULL) {
    color_map_ = std::unique_ptr<ColorMap>(initialize_full_color_map(leds_per_strip_));
  }
  return color_map_.get();
}

RGB Sparkshot::compute(float percent, int idx, int total_idx) const {
  const float min_intensity = 0.2;
  RGB rgb = RGB(0, 0, 0);

  // Iterate over shots backwards (last shot gets precedence)
  for (auto shot = shots_.rbegin(); shot != shots_.rend(); ++shot) {
    const float start_idx_pct = shot->start_idx_pct_;
    const float end_idx_pct = shot->end_idx_pct_;
    const float dropoff_factor = shot->dropoff_factor_;
    const RGB color = shot->color_;

    // derived
    const int start_idx = std::round(start_idx_pct * total_idx);
    const int end_idx = std::round(end_idx_pct * total_idx);
    const int total_distance = abs(end_idx - start_idx);
    const bool forward = end_idx > start_idx;
    const float distance = percent * total_distance;
    const int head_idx =
        forward ? std::round(start_idx + distance) : std::round(start_idx - distance);
    const int distance_from_head = abs(head_idx - idx);
    float intensity = pow(dropoff_factor, distance_from_head);

    // Move to the next shot if this one isn't bright enough
    if (intensity < min_intensity) {
      continue;
    }

    if (!vary_intensity_) {
      intensity = 1;
    }

    // Figure out the colors
    const float additional_scale_factor = 255.0 * 3 / (color.red + color.green + color.blue);
    rgb = RGB(POWER_SCALE * intensity * color.red * additional_scale_factor,
              POWER_SCALE * intensity * color.green * additional_scale_factor,
              POWER_SCALE * intensity * color.blue * additional_scale_factor);

    // If we found a color, drop out
    break;
  }
  return rgb;
}

bool Sparkshot::is_linear() const { return false; }
