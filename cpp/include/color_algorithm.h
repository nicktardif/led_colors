#pragma once

#include "color_map.h"
#include "rgb.h"

class ColorAlgorithm {
 public:
  ColorMap* get_color_map() const;

 protected:
  int bucket_size_;
  ColorMap* color_map_;
  virtual RGB compute(float percent, int idx, int total_idx) const = 0;

  ColorMap* initialize_linear_color_map();
};

class Rainbow : public ColorAlgorithm {
 public:
  Rainbow(const int bucket_size);
  ColorMap* get_color_map() const;

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
};

class Pastel : public ColorAlgorithm {
 public:
  Pastel(const int bucket_size, int red_scalar, int red_offset, int green_scalar, int green_offset,
         int blue_scalar, int blue_offset);

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;

 private:
  int red_scalar_;
  int green_scalar_;
  int blue_scalar_;
  int red_offset_;
  int green_offset_;
  int blue_offset_;
};

class Comet : public ColorAlgorithm {
 public:
  Comet(const int bucket_size);

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
};