#include "../include/color_map.h"

#include <cmath>

#include "../include/rgb.h"

LinearColorMap::LinearColorMap(const int bucket_size) {
  bucket_size_ = bucket_size;
  colors_ = new RGB[bucket_size_];
};

void LinearColorMap::add_color(const int bucket_idx, const int idx, const int total_idx,
                               const RGB rgb) {
  colors_[bucket_idx] = rgb;
}

LinearColorMap::~LinearColorMap() { delete[] colors_; }

RGB LinearColorMap::lookup(const float percent, const int idx, const int total_idx) const {
  // ignoring idx and total_idx for linear color maps
  const int bucket_idx = std::floor(float(percent) * bucket_size_);
  return colors_[bucket_idx];
}

FullColorMap::FullColorMap(const int bucket_size) {
  bucket_size_ = bucket_size;
  colors_ = new RGB[bucket_size_ * bucket_size_];
};

FullColorMap::~FullColorMap() { delete[] colors_; }

void FullColorMap::add_color(const int bucket_idx, const int idx, const int total_idx,
                             const RGB rgb) {
  colors_[bucket_idx * total_idx + idx] = rgb;
}

RGB FullColorMap::lookup(const float percent, const int idx, const int total_idx) const {
  const int bucket_idx = std::floor(float(percent) * bucket_size_);
  return colors_[bucket_idx * total_idx + idx];
}