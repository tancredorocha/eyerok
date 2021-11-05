#include "Arduino.h"
#include "src/AX12A.h"

#define DirectionPin   10
#define BaudRate      (57600u)
#define ID        (1u)

int initial_pos = 512;
int max = initial_pos + 100;
int min = initial_pos - 100;

int pos = initial_pos;
int delta = 5;

void setup()
{
  ax12a.begin(BaudRate, DirectionPin, &Serial);
  ax12a.reset(ID);
}

void loop()
{
  pos = pos + delta;

  if (pos > max)
  {
    pos = max;
    delta *= -1;
  }

  if (pos < min)
  {
    pos = min;
    delta *= -1;
  }

  ax12a.move(ID, pos);
  delay(2000);
}
