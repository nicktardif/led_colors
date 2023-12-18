#pragma once

#include "rgb.h"

class ColorMap {
 public:
  virtual RGB lookup(float percent, int idx, int total_idx) const = 0;
  virtual void add_color(const int bucket_idx, const int idx, const int total_idx,
                         const RGB rgb) = 0;
  virtual ~ColorMap(){};
};

class LinearColorMap : public ColorMap {
 public:
  LinearColorMap(const int bucket_size);
  ~LinearColorMap();

  void add_color(const int bucket_idx, const int idx, const int total_idx, const RGB rgb) override;

  RGB lookup(float percent, int idx, int total_idx) const override;

 private:
  int bucket_size_;
  RGB* colors_;
};

class FullColorMap : public ColorMap {
 public:
  FullColorMap(const int bucket_size);
  ~FullColorMap();

  void add_color(const int bucket_idx, const int idx, const int total_idx, const RGB rgb) override;

  RGB lookup(float percent, int idx, int total_idx) const override;

 private:
  int bucket_size_;
  RGB* colors_;
};