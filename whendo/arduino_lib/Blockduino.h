/*
  Blockduino.h - Library for flashing Blockduino modules.
  Created by Neil Chatterjee, Ankush Gola, Pranav Badami, Joseph Bolling
  Released into the public domain.

  Author: Ankush Gola
*/
#ifndef Blockduino_h
#define Blockduino_h

#include "Arduino.h"
#include <Servo.h>

class B_Accel
{
  public:
    B_Accel();
    void init(int x_pin, int y_pin);
    bool is_left();
    bool is_right();
    bool is_up();
    bool is_down();
    int read_x();
    int read_y();
  private:
    int _x_pin;
    int _y_pin;
};

class B_Servo
{
  public:
    B_Servo();
    void turn_left();
    void turn_right();
    void center();
    void init(int pin);
  private:
    int _pin;
    Servo servo;
};

class B_PushButton
{
  public:
    B_PushButton();
    void init(int pin);
    bool is_on();
  private:
    int _pin;
};

class B_LED
{
  public:
    B_LED();
    void init(int pin);
    void turn_on();
    void turn_off();
  private:
    int _pin;
};

class B_LEDGroup : public B_LED
{
  public:
    B_LEDGroup(B_LED led_1, B_LED led_2, B_LED led_3);
    B_LED get_current();
    B_LED get_next();
  private:
    int _led_num;
    int _current_index;
    B_LED _led_array[3];
    B_LED led_1;
    B_LED led_2;
    B_LED led_3;
};

#endif