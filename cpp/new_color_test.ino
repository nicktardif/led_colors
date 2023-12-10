#define __IMXRT1062__  // Teensy 4.0
#include <OctoWS2811.h>
#include <math.h>

#include "include/color_algorithm.h"

const int LEDS_PER_STRIP = 60;

DMAMEM int displayMemory[LEDS_PER_STRIP * 6];
int drawingMemory[LEDS_PER_STRIP * 6];

const int config = WS2811_GRB | WS2813_800kHz;
const int BUCKET_SIZE = 200;
const uint8_t LED_STRIP_COUNT = 1;

const int SEQUENCE_DURATION_MS = 4000;
const float REFRESH_HZ = 30;

OctoWS2811 leds(LEDS_PER_STRIP, displayMemory, drawingMemory, config, LED_STRIP_COUNT);
int rainbowColors[BUCKET_SIZE];

ColorAlgorithm* color_alg = NULL;
ColorMap* color_map = NULL;

void setup() {
  // color_alg = new Rainbow(BUCKET_SIZE);
  // color_alg = new Pastel(BUCKET_SIZE, 110, 145, 110, 145, 110, 145);  // default pastel
  // color_alg = new Pastel(BUCKET_SIZE, 50, 105, 110, 145, 80, 145);  // less red
  // color_alg = new Pastel(BUCKET_SIZE, 10, 105, 110, 145, 40, 145);  // green/purple/blue
  color_alg = new Comet(BUCKET_SIZE);  // comets!
  color_map = color_alg->get_color_map();

  leds.begin();
}

void loop() {
  const int SEQUENCE_SIZE = (int)round(REFRESH_HZ * SEQUENCE_DURATION_MS / 1000);
  const int SEQUENCE_WAIT_US = (int)round(SEQUENCE_DURATION_MS * 1000 / float(SEQUENCE_SIZE));

  assign_colors(SEQUENCE_SIZE, SEQUENCE_WAIT_US);
}

void assign_colors(const int sequence_size, const int sequence_wait_us) {
  for (int loop_idx = 0; loop_idx < sequence_size; loop_idx++) {
    const float percent = float(loop_idx) / sequence_size;

    for (int x = 0; x < LEDS_PER_STRIP; x++) {
      for (int y = 0; y < LED_STRIP_COUNT; y++) {
        const float adjusted_percent = fmod(percent + (float(x) / LEDS_PER_STRIP), 1.0);
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
