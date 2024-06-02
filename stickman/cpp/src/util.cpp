#include "../include/util.h"

#include <math.h>

#include <cmath>

// gradual s curve
// https://www.wolframalpha.com/input?i=1+%2F+%281+%2B+%28x+%2F+%281+-+x%29%29%5E-2%29+from+%5B0%2C+1%5D
float s_curve(float x) { return 1.0 / (1 + pow(x / (1 - x), -2)); }

// sharp curve starting at 0 and ending at 1
// https://www.wolframalpha.com/input?i=1+%2F+%281+%2B+%284x+%2F+%281+-+x%29%29%5E-2%29+from+%5B0%2C+1%5D
float sharp_s_ramp(float x) { return 1.0 / (1 + pow(4 * x / (1 - x), -2)); }

// Input [0,1] and get back the Y value of the normalized bell curve
// Return value is between 0 and 1
// https://www.wolframalpha.com/input?i=%28%281+%2F+%280.17+*+sqrt%282+*+pi%29%29%29+*+%28e+%5E+%28+%28-1+%2F2+%29+*+%28%28%28x+-+0.5%29+%2F+0.17%29+%5E+2%29%29%29+%29+%2F+2.34+from+%5B0%2C+1%5D
float gaussian_value(float x) {
  const float scale_factor = 2.34;
  const float std_dev = 0.17;
  const float center = 0.5;

  return ((1.0 / (std_dev * sqrt(2 * M_PI))) * pow(M_E, -0.5 * pow((x - center) / std_dev, 2))) /
         scale_factor;
}