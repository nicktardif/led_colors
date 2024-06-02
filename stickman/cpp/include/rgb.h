#pragma once

class RGB {
 public:
  int red;
  int green;
  int blue;

  RGB();

  RGB(int r, int g, int b);

  RGB(float r, float g, float b);

  int as_int() const;
};
