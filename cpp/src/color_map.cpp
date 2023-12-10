#include "../include/color_map.h"

#include <cmath>

#include "../include/rgb.h"

LinearColorMap::LinearColorMap(const int bucket_size) {
  bucket_size_ = bucket_size;
  colors_ = new RGB[bucket_size_];
};

void LinearColorMap::add_color(const float percent, const int idx, const int total_idx,
                               const RGB rgb) {
  // ignoring idx and total_idx for linear color maps
  const int bucket_idx = round(float(percent) * bucket_size_);
  colors_[bucket_idx] = rgb;
}

RGB LinearColorMap::lookup(const float percent, const int idx, const int total_idx) const {
  // ignoring idx and total_idx for linear color maps
  const int bucket_idx = round(float(percent) * bucket_size_);
  return colors_[bucket_idx];
}