#include "../include/rgb.h"

#include <algorithm>
#include <cmath>


int clamp(int val) { return std::min(std::max(val, 0), 255); }

RGB::RGB() {
  red = 0;
  green = 0;
  blue = 0;
}

RGB::RGB(int r, int g, int b) {
  red = clamp(r);
  green = clamp(g);
  blue = clamp(b);
}

RGB::RGB(float r, float g, float b) {
  red = clamp(int(std::round(r)));
  green = clamp(int(std::round(g)));
  blue = clamp(int(std::round(b)));
}

int RGB::as_int() const { return (red << 16) | (green << 8) | blue; }