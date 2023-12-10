#define _USE_MATH_DEFINES
#include "../include/color_algorithm.h"

#include <math.h>

#include <algorithm>

#include "../include/color_map.h"
#include "../include/rgb.h"

const float POWER_SCALE = 0.07;  // 7% of max power

ColorMap* ColorAlgorithm::get_color_map() const { return color_map_; }

ColorMap* ColorAlgorithm::initialize_linear_color_map() {
  ColorMap* color_map = new LinearColorMap(bucket_size_);
  for (int i = 0; i < bucket_size_; i++) {
    const float percent = float(i) / bucket_size_;

    // Ignoring idx and total_idx for linear color map
    const RGB rgb = compute(percent, 0, 0);
    color_map->add_color(percent, i, bucket_size_, rgb);
  }
  return color_map;
}

Rainbow::Rainbow(const int bucket_size) {
  bucket_size_ = bucket_size;
  color_map_ = initialize_linear_color_map();
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

Pastel::Pastel(const int bucket_size, int red_scalar, int red_offset, int green_scalar,
               int green_offset, int blue_scalar, int blue_offset) {
  bucket_size_ = bucket_size;
  red_scalar_ = red_scalar;
  red_offset_ = red_offset;
  green_scalar_ = green_scalar;
  green_offset_ = green_offset;
  blue_scalar_ = blue_scalar;
  blue_offset_ = blue_offset;
  color_map_ = initialize_linear_color_map();
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

Comet::Comet(const int bucket_size) {
  bucket_size_ = bucket_size;
  color_map_ = initialize_linear_color_map();
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
