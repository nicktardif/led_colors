#define __IMXRT1062__  // Teensy 4.0
#include <OctoWS2811.h>
#include <math.h>

#include "include/color_algorithm.h"

const int LEDS_PER_STRIP = 60;

DMAMEM int displayMemory[LEDS_PER_STRIP * 6];
int drawingMemory[LEDS_PER_STRIP * 6];

const int config = WS2811_GRB | WS2813_800kHz;
const int BUCKET_SIZE = 100;  // too high and we'll run out of RAM
const uint8_t LED_STRIP_COUNT = 1;

const int SEQUENCE_DURATION_MS = 4000;  // DON'T CHANGE THIS
const float REFRESH_HZ = 30;

OctoWS2811 leds(LEDS_PER_STRIP, displayMemory, drawingMemory, config, LED_STRIP_COUNT);
int rainbowColors[BUCKET_SIZE];

std::vector<ColorAlgorithm*> color_algorithms = {};
ColorMap* color_map = NULL;
int color_algorithm_idx = 0;

std::vector<Shot> four_color_shot_list(RGB r1, RGB r2, RGB r3, RGB r4) {
  const float spacing = 0.75;
  const std::vector<Shot> shots = {
      Shot(-1.0, 0.0, spacing, r1),    Shot(0.0, 1.0, spacing, r1),
      Shot(1.0, 2.0, spacing, r1),

      Shot(-1.75, -0.75, spacing, r2), Shot(-0.75, 0.25, spacing, r2),
      Shot(0.25, 1.25, spacing, r2),

      Shot(-0.5, 0.5, spacing, r3),    Shot(0.5, 1.5, spacing, r3),

      Shot(-1.25, -0.25, spacing, r4), Shot(-0.25, 0.75, spacing, r4),
      Shot(0.75, 1.75, spacing, r4),
  };
  return shots;
}

std::vector<Shot> five_color_shot_list(RGB r1, RGB r2, RGB r3, RGB r4, RGB r5) {
  const float spacing = 0.7;
  const std::vector<Shot> shots = {
      Shot(-1.0, 0.0, spacing, r1),    Shot(0.0, 1.0, spacing, r1),
      Shot(1.0, 2.0, spacing, r1),

      Shot(-1.80, -0.80, spacing, r2), Shot(-0.80, 0.20, spacing, r2),
      Shot(0.20, 1.20, spacing, r2),

      Shot(-1.60, -0.60, spacing, r3), Shot(-0.60, 0.40, spacing, r3),
      Shot(0.40, 1.40, spacing, r3),

      Shot(-1.40, -0.40, spacing, r4), Shot(-0.40, 0.60, spacing, r4),
      Shot(0.60, 1.60, spacing, r4),

      Shot(-1.20, -0.20, spacing, r5), Shot(-0.20, 0.80, spacing, r5),
      Shot(0.80, 1.80, spacing, r5),

  };
  return shots;
}

void setup() {
  const std::vector<ColorPoint> spooky_breathing = {
      ColorPoint(0.5f, 0.2f, 0.1f, 0.0f), ColorPoint(0.2, 1, 0.5, 0.5f), ColorPoint(0, 1, 1, 0.25f),
      ColorPoint(1, 1, 0, 0.75f), ColorPoint(1, 0.5, 1, 1.0f)};

  const std::vector<ColorPoint> garden_rave = {ColorPoint(242, 163, 41, 0.0f),   // red
                                               ColorPoint(236, 91, 91, 0.25f),   // yellow
                                               ColorPoint(165, 201, 86, 0.50f),  // purple
                                               ColorPoint(43, 120, 83, 0.75f),   // purple
                                               ColorPoint(175, 60, 182, 1.0f)};  // blue

  const std::vector<Shot> lime_shots = {
      Shot(0.0, 8.0, 0.5, RGB(225, 254, 1)),     // fast bright yellow
      Shot(-0.5, 7.5, 0.8, RGB(118, 89, 255)),   // dark blurple
      Shot(-1.0, 7.0, 0.5, RGB(1, 255, 126)),    // fast bright green
      Shot(-1.5, 6.5, 0.8, RGB(243, 144, 166)),  // pink
      Shot(-2.0, 6.0, 0.9, RGB(225, 254, 1)),    // fast bright yellow
      Shot(-3.0, 5.0, 0.9, RGB(1, 255, 126)),    // fast bright green
      Shot(-4.0, 4.0, 0.5, RGB(225, 254, 1)),    // fast bright yellow
      Shot(-5.0, 3.0, 0.5, RGB(1, 255, 126)),    // fast bright green
      Shot(-6.0, 2.0, 0.9, RGB(225, 254, 1)),    // fast bright yellow
      Shot(-7.0, 1.0, 0.9, RGB(1, 255, 126)),    // fast bright green
  };

  // Sourced a lot of colors from https://www.color-hex.com/color-palettes/
  const RGB bright_green(11, 227, 8);
  const RGB royal_purple(92, 27, 222);
  const RGB turquoise(0, 195, 224);
  const RGB lime(175, 222, 3);

  const std::vector<Shot> acid = {
      Shot(0.0, 8.0, 0.5, bright_green),  Shot(-0.5, 7.5, 0.8, royal_purple),
      Shot(-1.0, 7.0, 0.5, turquoise),    Shot(-1.5, 6.5, 0.8, lime),
      Shot(-2.0, 6.0, 0.9, bright_green), Shot(-3.0, 5.0, 0.9, turquoise),
      Shot(-4.0, 4.0, 0.5, bright_green), Shot(-5.0, 3.0, 0.5, turquoise),
      Shot(-6.0, 2.0, 0.9, bright_green), Shot(-7.0, 1.0, 0.9, turquoise),
  };

  const RGB fire_pink(247, 24, 67);
  const RGB fire_orange(248, 69, 38);
  const RGB fire_light_orange(247, 156, 98);
  const RGB fire_light_pink(239, 199, 219);

  const std::vector<Shot> fire_shots = {
      Shot(0.0, 8.0, 0.5, fire_pink),          Shot(-0.5, 7.5, 0.8, fire_light_orange),
      Shot(-1.0, 7.0, 0.5, fire_orange),       Shot(-1.5, 6.5, 0.8, fire_pink),
      Shot(-2.0, 6.0, 0.9, fire_light_orange), Shot(-3.0, 5.0, 0.9, fire_light_pink),
      Shot(-4.0, 4.0, 0.5, fire_pink),         Shot(-5.0, 3.0, 0.5, fire_orange),
      Shot(-6.0, 2.0, 0.9, fire_light_orange), Shot(-7.0, 1.0, 0.9, fire_light_pink),
  };

  const RGB white(255, 255, 255);

  const RGB summer_sorbet1(255, 181, 28);
  const RGB summer_sorbet2(255, 140, 82);
  const RGB summer_sorbet3(255, 107, 107);
  const RGB summer_sorbet4(255, 131, 189);
  const std::vector<Shot> sorbet_shots =
      four_color_shot_list(summer_sorbet1, summer_sorbet2, summer_sorbet3, summer_sorbet4);

  const RGB hello1(255, 127, 157);
  const RGB hello2(212, 163, 246);
  const RGB hello3(0, 178, 255);
  const RGB hello4(22, 255, 231);
  const RGB hello5(255, 243, 36);
  const std::vector<Shot> hello_shots =
      five_color_shot_list(hello1, hello2, hello3, hello4, hello5);

  const RGB powertrip1(41, 34, 200);
  const RGB powertrip2(85, 33, 203);
  const RGB powertrip3(156, 43, 179);
  const RGB powertrip4(219, 50, 158);
  const RGB powertrip5(167, 239, 70);
  const std::vector<Shot> powertrip_shots =
      five_color_shot_list(powertrip1, powertrip2, powertrip3, powertrip4, powertrip5);

  const RGB dark_purple(32, 18, 77);
  const RGB bright_orange(255, 115, 39);

  const std::vector<Shot> space_shots = {
      Shot(0.0, 0.33, 0.4, dark_purple),     Shot(0.33, 0.67, 0.4, dark_purple),
      Shot(0.67, 1.0, 0.4, dark_purple),

      Shot(0.0, 2.0, 0.7, powertrip1),

      Shot(-0.6, 4.0, 0.6, bright_green),

      Shot(-3.6, 0.8, 0.6, bright_green),    Shot(0.8, 5.2, 0.6, bright_green),

      Shot(-1.0, 1.5, 0.7, powertrip4),

      Shot(-6.0, 2.5, 0.6, bright_orange),

      Shot(0.0, 8.0, 0.4, bright_orange),    Shot(-0.33, 7.66, 0.4, bright_orange),
      Shot(-0.67, 7.33, 0.4, bright_orange), Shot(-1.0, 7.0, 0.4, bright_orange),

      Shot(-4.0, 4.0, 0.3, white),           Shot(-4.33, 3.66, 0.3, white),
      Shot(-4.67, 3.33, 0.3, white),         Shot(-5.0, 3.0, 0.3, white),

      Shot(-7.0, 1.0, 0.7, white),
  };

  Serial.begin(9600);  // initialize serial port for input

  // Create all the color algorithms
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, false, space_shots));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, false, hello_shots));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, true, lime_shots));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, true, acid));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, true, fire_shots));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, false, sorbet_shots));
  color_algorithms.push_back(new Sparkshot(BUCKET_SIZE, LEDS_PER_STRIP, false, powertrip_shots));

  color_algorithms.push_back(new Yoyo(BUCKET_SIZE, LEDS_PER_STRIP, 242, 124, 5));  // fire yoyoyo
  color_algorithms.push_back(new Yoyo(BUCKET_SIZE, LEDS_PER_STRIP, 12, 232, 70));  // green yoyoyo

  color_algorithms.push_back(new Rainbow(BUCKET_SIZE));
  color_algorithms.push_back(new Pastel(BUCKET_SIZE, 50, 105, 110, 145, 80, 145));  // purple/green
  color_algorithms.push_back(new Comet(BUCKET_SIZE));

  color_algorithms.push_back(new Wubwub(BUCKET_SIZE, LEDS_PER_STRIP, spooky_breathing));
  color_algorithms.push_back(new Wubwub(BUCKET_SIZE, LEDS_PER_STRIP, garden_rave));

  // Populate the color map
  color_map = color_algorithms[color_algorithm_idx]->get_color_map();

  leds.begin();
}

// Check the serial input for an input change. Return true if there is a change
bool check_input_and_change_algorithm() {
  if (Serial.available() > 0) {
    const byte incomingByte = Serial.read();

    if (incomingByte != 10) {
      Serial.print("did not detect enter key");
    } else {
      const int original_color_algorithm_idx = color_algorithm_idx;
      color_algorithm_idx = (color_algorithm_idx + 1) % color_algorithms.size();

      // Reload the color map
      Serial.print("Creating new color map \n");
      ColorMap* new_color_map = color_algorithms[color_algorithm_idx]->get_color_map();
      Serial.print("Deleted color map \n");
      color_algorithms[original_color_algorithm_idx]->reset_color_map();
      color_map = new_color_map;
      Serial.print("Loaded new color map \n");
      return true;
    }
  }

  return false;
}

void loop() {
  const int SEQUENCE_SIZE = (int)round(REFRESH_HZ * SEQUENCE_DURATION_MS / 1000);
  const int SEQUENCE_WAIT_US = (int)round(SEQUENCE_DURATION_MS * 1000 / float(SEQUENCE_SIZE));

  assign_colors(SEQUENCE_SIZE, SEQUENCE_WAIT_US);
}

void assign_colors(const int sequence_size, const int sequence_wait_us) {
  const int check_input_per_cycle_frequency = 16;
  for (int loop_idx = 0; loop_idx < sequence_size; loop_idx++) {
    const float percent = float(loop_idx) / sequence_size;

    if (loop_idx % (sequence_size / check_input_per_cycle_frequency) == 0) {
      bool algorithm_changed = check_input_and_change_algorithm();
      // fall out early and change it up
      if (algorithm_changed) {
        return;
      }
    }

    for (int x = 0; x < LEDS_PER_STRIP; x++) {
      for (int y = 0; y < LED_STRIP_COUNT; y++) {
        float adjusted_percent = 0;
        if (color_algorithms[color_algorithm_idx]->is_linear()) {
          adjusted_percent = fmod(percent + (float(x) / LEDS_PER_STRIP), 1.0);
        } else {
          adjusted_percent = percent;
        }

        const int rgb = color_map->lookup(adjusted_percent, x, LEDS_PER_STRIP).as_int();
        leds.setPixel(x + y * LEDS_PER_STRIP, rgb);
      }
    }

    leds.show();
    delayMicroseconds(sequence_wait_us);
  }
}

// void print_rgb(const int i, const RGB rgb) {
//   Serial.print(i, DEC);
//   Serial.print(": ");
//   Serial.print(rgb.red, DEC);
//   Serial.print(" ");
//   Serial.print(rgb.green, DEC);
//   Serial.print(" ");
//   Serial.print(rgb.blue, DEC);
//   Serial.print("\n");
// }
