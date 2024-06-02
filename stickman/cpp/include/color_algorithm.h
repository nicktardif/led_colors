#pragma once

#include <memory>
#include <vector>

#include "color_gradient.h"
#include "color_map.h"
#include "rgb.h"

class ColorAlgorithm {
 public:
  virtual ColorMap* get_color_map() = 0;
  virtual bool is_linear() const = 0;
  void reset_color_map();

 protected:
  int bucket_size_;
  std::unique_ptr<ColorMap> color_map_ = NULL;
  virtual RGB compute(float percent, int idx, int total_idx) const = 0;

  ColorMap* initialize_linear_color_map();
  ColorMap* initialize_full_color_map(const int leds_per_strip);
};

class Rainbow : public ColorAlgorithm {
 public:
  Rainbow(const int bucket_size);
  ColorMap* get_color_map();
  bool is_linear() const;

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
};

class Pastel : public ColorAlgorithm {
 public:
  Pastel(const int bucket_size, int red_scalar, int red_offset, int green_scalar, int green_offset,
         int blue_scalar, int blue_offset);
  bool is_linear() const;
  ColorMap* get_color_map();

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
  bool is_linear() const;
  ColorMap* get_color_map();

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
};

class Yoyo : public ColorAlgorithm {
 public:
  Yoyo(const int bucket_size, const int leds_per_strip, const int r_scalar, const int g_scalar,
       const int b_scalar);
  bool is_linear() const;
  ColorMap* get_color_map();

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
  int r_scalar_;
  int g_scalar_;
  int b_scalar_;
  int leds_per_strip_;

 private:
  float time_scale_;
};

class Wubwub : public ColorAlgorithm {
 public:
  Wubwub(const int bucket_size, const int leds_per_strip, const std::vector<ColorPoint> colors);
  bool is_linear() const;
  ColorMap* get_color_map();

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
  ColorGradient color_gradient_;
  int leds_per_strip_;
};

struct Shot {
  const float start_idx_pct_;  // where the shot starts (as a ratio)
  const float end_idx_pct_;    // where the shot ends (as a ratio)
  const float
      dropoff_factor_;  // how quickly the shot drops off in intensity from the center [0, 1]
  const RGB color_;     // color of the shot

  Shot(float start_idx_pct, float end_idx_pct, float dropoff_factor, RGB color)
      : start_idx_pct_(start_idx_pct),
        end_idx_pct_(end_idx_pct),
        dropoff_factor_(dropoff_factor),
        color_(color) {}
};

class Sparkshot : public ColorAlgorithm {
 public:
  Sparkshot(const int bucket_size, const int leds_per_strip, const bool vary_intensity,
            std::vector<Shot> shots);
  bool is_linear() const;
  ColorMap* get_color_map();

 protected:
  RGB compute(float percent, int idx, int total_idx) const override;
  int leds_per_strip_;

 private:
  const std::vector<Shot> shots_;
  const bool vary_intensity_;
};
