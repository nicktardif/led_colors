#include <algorithm>
#include <vector>

#include "rgb.h"

struct ColorPoint  // Internal class used to store colors at different points in the gradient.
{
  float r, g, b;  // Red, green and blue values of our color.
  float val;      // Position of our color along the gradient (between 0 and 1).
  ColorPoint(float red, float green, float blue, float value)
      : r(red), g(green), b(blue), val(value) {}

  ColorPoint(int red, int green, int blue, float value)
      : r(float(red) / 255), g(float(green) / 255), b(float(blue) / 255), val(value) {}
};

class ColorGradient {
 private:
  std::vector<ColorPoint> color_;  // An array of color points in ascending value.

 public:
  ColorGradient(std::vector<ColorPoint> colors) {
    color_.clear();
    for (auto &color : colors) {
      color_.push_back(color);
    }
  }

  //-- Inputs a (value) between 0 and 1 and outputs the (red), (green) and (blue)
  //-- values representing that position in the gradient.
  RGB getColorAtValue(const float value) const {
    if (color_.size() == 0) return RGB(0, 0, 0);

    for (int i = 0; i < int(color_.size()); i++) {
      ColorPoint currC = color_[i];
      if (value < currC.val) {
        ColorPoint prevC = color_[std::max(0, i - 1)];
        float valueDiff = (prevC.val - currC.val);
        float fractBetween = (valueDiff == 0) ? 0 : (value - currC.val) / valueDiff;
        float red = (prevC.r - currC.r) * fractBetween + currC.r;
        float green = (prevC.g - currC.g) * fractBetween + currC.g;
        float blue = (prevC.b - currC.b) * fractBetween + currC.b;
        return RGB(red * 255, green * 255, blue * 255);
      }
    }
    float r = color_.back().r;
    float g = color_.back().g;
    float b = color_.back().b;
    return RGB(r * 255, g * 255, b * 255);
  }
};