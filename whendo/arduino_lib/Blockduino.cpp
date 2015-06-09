/*
  Blockduino.cpp - Library for Blockduino modules
  Copyright Ankush Gola, Pranav Badami, Neil Chatterjee, Joseph Bolling
  Released into the public domain.

  Author: Ankush Gola
*/

#include "Arduino.h"
#include "Blockduino.h"
#include <Servo.h>

// Accel
B_Accel::B_Accel()
{}

void B_Accel::init(int x_pin, int y_pin)
{
  pinMode(x_pin, INPUT);
  pinMode(y_pin, INPUT);
  _x_pin = x_pin;
  _y_pin = y_pin;
}

bool B_Accel::is_left()
{
  int pulse_x;
  int accel_x;
  pulse_x = pulseIn(_y_pin, HIGH);
  accel_x = ((pulse_x / 10) - 500) * 8;
  return accel_x > 300;
}

bool B_Accel::is_right()
{
  int pulse_x;
  int accel_x;
  pulse_x = pulseIn(_y_pin, HIGH);
  accel_x = ((pulse_x / 10) - 500) * 8;
  return accel_x < -200;
}

bool B_Accel::is_up()
{
  int pulse_y;
  int accel_y;
  pulse_y = pulseIn(_y_pin, HIGH);
  accel_y = ((pulse_y / 10) - 500) * 8;
  return accel_y < 0;
}

bool B_Accel::is_down()
{
  int pulse_y;
  int accel_y;
  pulse_y = pulseIn(_y_pin, HIGH);
  accel_y = ((pulse_y / 10) - 500) * 8;
  return accel_y > 0;
}

int B_Accel::read_x()
{
  int pulse_x;
  int accel_x;
  pulse_x = pulseIn(_y_pin, HIGH);
  accel_x = ((pulse_x / 10) - 500) * 8;
  return accel_x;
}

int B_Accel::read_y()
{
  int pulse_y;
  int accel_y;
  pulse_y = pulseIn(_x_pin, HIGH);
  accel_y = ((pulse_y / 10) - 500) * 8;
  return accel_y;
}

// Servo
B_Servo::B_Servo()
{}

void B_Servo::init(int pin)
{
  _pin = pin;
  servo.attach(pin);
}

void B_Servo::turn_left()
{
  servo.write(180);
}

void B_Servo::turn_right()
{
  servo.write(0);
}

void B_Servo::center()
{
  servo.write(90);
}

// PushButton
B_PushButton::B_PushButton()
{}

void B_PushButton::init(int pin)
{
  pinMode(pin, INPUT_PULLUP);
  _pin = pin;
}

bool B_PushButton::is_on()
{
  bool val = digitalRead(_pin);
  delay(100);
  return val == HIGH;
}

// LED
B_LED::B_LED() {}

void B_LED::init(int pin)
{
  pinMode(pin, OUTPUT);
  _pin = pin;
}

void B_LED::turn_on()
{
  digitalWrite(_pin, HIGH);
}

void B_LED::turn_off()
{
  digitalWrite(_pin, LOW);
}
// LED Group
B_LEDGroup::B_LEDGroup(B_LED led_1, B_LED led_2, B_LED led_3)
: led_1(led_1), led_2(led_2), led_3(led_3)
{
  _led_array[0] = led_1;
  _led_array[1] = led_2;
  _led_array[2] = led_3;
  _led_num = 3;
  _current_index = 0;
}

B_LED B_LEDGroup::get_current()
{
  return _led_array[_current_index];
}

B_LED B_LEDGroup::get_next()
{
  if (_current_index >= 2)
  {
    _current_index = 0;
  }
  else
  {
    _current_index++;
  }
  return _led_array[_current_index];

}
