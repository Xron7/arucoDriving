/*
 * Copyright 1996-2018 Cyberbotics Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Description:  An example of use of a camera device.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <webots/camera.h>
#include <webots/motor.h>
#include <webots/robot.h>
#include <webots/utils/system.h>
#include <webots/distance_sensor.h>

#define ANSI_COLOR_RED "\x1b[31m"
#define ANSI_COLOR_GREEN "\x1b[32m"
#define ANSI_COLOR_YELLOW "\x1b[33m"
#define ANSI_COLOR_BLUE "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN "\x1b[36m"
#define ANSI_COLOR_RESET "\x1b[0m"

#define SPEED 4
#define TIME_STEP 64
enum BLOB_TYPE { RED, GREEN, BLUE, NONE };

int main() {
  WbDeviceTag camera, left_motor, right_motor,ds0,ds1;
  int width, height;
  double left_speed, right_speed;
  int i, j;
  int red, blue, green;
  const char *color_names[3] = {"red", "green", "blue"};
  const char *ansi_colors[3] = {ANSI_COLOR_RED, ANSI_COLOR_GREEN, ANSI_COLOR_BLUE};
  enum BLOB_TYPE current_blob;
  int stop=40;
  int mode=1;
  wb_robot_init();
  
  ds0 = wb_robot_get_device("ds0");
  ds1 = wb_robot_get_device("ds1");
  wb_distance_sensor_enable(ds0, TIME_STEP);
  wb_distance_sensor_enable(ds1, TIME_STEP);
  double ds0_value;
  double ds1_value;

  /* Get the camera device, enable it, and store its width and height */
  camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, TIME_STEP);
  width = wb_camera_get_width(camera);
  height = wb_camera_get_height(camera);

  /* get a handler to the motors and set target position to infinity (speed control). */
  left_motor = wb_robot_get_device("left wheel motor");
  right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);

  /* Main loop */
  while (wb_robot_step(TIME_STEP) != -1) {
    /* Get the new camera values */
    const unsigned char *image = wb_camera_get_image(camera);
    switch (mode){
    
      case 1:
        /* Decrement the pause_counter*/
        if (stop!=0){
          
          /* Reset the sums */
          red = 0;
          green = 0;
          blue = 0;
    
          /*
           * Here we analyse the image from the camera. The goal is to detect a
           * blob (a spot of color) of a defined color in the middle of our
           * screen.
           * In order to achieve that we simply parse the image pixels of the
           * center of the image, and sum the color components individually
           */
          for (i = width / 3; i < 2 * width / 3; i++) {
            for (j = height / 2; j < 3 * height / 4; j++) {
              red += wb_camera_image_get_red(image, width, i, j);
              blue += wb_camera_image_get_blue(image, width, i, j);
              green += wb_camera_image_get_green(image, width, i, j);
            }
          }
    
          /*
           * If a component is much more represented than the other ones,
           * a blob is detected
           */
          if ((red > 3 * green) && (red > 3 * blue))
            current_blob = RED;
          else if ((green > 3 * red) && (green > 3 * blue))
            current_blob = GREEN;
          else if ((blue > 3 * red) && (blue > 3 * green))
            current_blob = BLUE;
          else
            current_blob = NONE;
    
          /*
           * Case 3a
           * No blob is detected
           * the robot continues to turn
           */
          stop--;
          left_speed = -SPEED;
          right_speed = SPEED;
          /*
           * Case 3b
           * A blob is detected
           * the robot stops, stores the image, and changes its state
           */
          if(current_blob!=NONE) {
            printf("Looks like I found a %s%s%s blob.\n", ansi_colors[current_blob], color_names[current_blob], ANSI_COLOR_RESET);      
          }
          }
          else{
            mode=2;
            }
          break;


        case 2:
    
           /* Get distance sensor values */
          
      
          /* Compute the motor speeds */
          ds0_value = wb_distance_sensor_get_value(ds0);
          ds1_value = wb_distance_sensor_get_value(ds1);
          wb_camera_get_image(camera);
          if (ds1_value > 500) {
            /*
             * If both distance sensors are detecting something, this means that
             * we are facing a wall. In this case we need to move backwards.
             */
            if (ds0_value > 500) {
              left_speed = -SPEED;
              right_speed = -SPEED / 2;
            } else {
              /*
               * We turn proportionnaly to the sensors value because the
               * closer we are from the wall, the more we need to turn.
               */
              left_speed = -ds1_value / 100;
              right_speed = (ds0_value / 100) + 0.5;
            }
          } else if (ds0_value > 500) {
            left_speed = (ds1_value / 100) + 0.5;
            right_speed = -ds0_value / 100;
          } else {
            /*
             * If nothing was detected we can move forward at maximal speed.
             */
            left_speed = SPEED;
            right_speed = SPEED;
          }
          break;
          }
      

    /* Set the motor speeds. */
    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);
  }
  

  wb_robot_cleanup();

  return 0;
}
