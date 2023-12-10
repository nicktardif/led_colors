#include <OctoWS2811.h>
#include <math.h>

const int LEDS_PER_STRIP = 60;

DMAMEM int displayMemory[LEDS_PER_STRIP*6];
int drawingMemory[LEDS_PER_STRIP*6];

const int config = WS2811_GRB | WS2813_800kHz;
const int BUCKET_SIZE = 200;
const int LED_STRIP_COUNT = 1;

const int SEQUENCE_DURATION_MS = 1000;
const float REFRESH_HZ = 30;
const int SEQUENCE_SIZE = round(REFRESH_HZ * SEQUENCE_DURATION_MS / 1000);
const int SEQUENCE_WAIT_MS = round(SEQUENCE_DURATION_MS * 1000 / float(SEQUENCE_SIZE));

const int RGB_SCALAR = 128;
const int RGB_OFFSET = 128;
const float BRIGHTNESS_SCALAR = 0.07;

OctoWS2811 leds(LEDS_PER_STRIP, displayMemory, drawingMemory, config, LED_STRIP_COUNT);
int rainbowColors[BUCKET_SIZE];

int rgb_to_int(int r, int g, int b) {
  return (r << 16) | (g << 8) | b;
}

int clamp(float f) {
  return min(max(round(f), 0), 255);
}

void setup() {
  // Pre-compute the colors
  for (int i=0; i<BUCKET_SIZE; i++) {
    float offset_percent = float(i) / BUCKET_SIZE;
    float a = offset_percent * 2 * PI;
    float r = BRIGHTNESS_SCALAR * (sin(a) * RGB_SCALAR + RGB_OFFSET);
    float g = BRIGHTNESS_SCALAR * (sin(a - (2 * PI / 3)) * RGB_SCALAR + RGB_OFFSET);
    float b = BRIGHTNESS_SCALAR * (sin(a - (4 * PI / 3)) * RGB_SCALAR + RGB_OFFSET);

    /*
    Serial.print(i, DEC);
    Serial.print(": ");
    Serial.print(clamp(r), DEC);
    Serial.print(" ");
    Serial.print(clamp(g), DEC);
    Serial.print(" ");
    Serial.print(clamp(b), DEC);
    Serial.print("\n");
    */

    rainbowColors[i] = rgb_to_int(clamp(r), clamp(g), clamp(b));
  }

  leds.begin();
}


void loop() {
  rainbow();
}


void rainbow()
{
  for (int loop_idx = 0; loop_idx < SEQUENCE_SIZE; loop_idx++) {
    const float percent = float(loop_idx) / SEQUENCE_SIZE;

    for (int x=0; x < LEDS_PER_STRIP; x++) {
      for (int y=0; y < LED_STRIP_COUNT; y++) {
        const float adjusted_percent = percent + (float(x) / LEDS_PER_STRIP);
        int bucket_idx = round(BUCKET_SIZE * fmod(adjusted_percent, 1.0));
        leds.setPixel(x + y*LEDS_PER_STRIP, rainbowColors[bucket_idx]);
      }
    }

    leds.show();
    delayMicroseconds(SEQUENCE_WAIT_MS);
  }
}

