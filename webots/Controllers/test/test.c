/*εισαγωγή βιβλιοθηκών*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <webots/camera.h>
#include <webots/motor.h>
#include <webots/robot.h>
#include <webots/utils/system.h>
#include <webots/distance_sensor.h>

/*_______________________________________
Ορισμοί χρωμάτων*/

#define ANSI_COLOR_RED "\x1b[31m"
#define ANSI_COLOR_GREEN "\x1b[32m"
#define ANSI_COLOR_YELLOW "\x1b[33m"
#define ANSI_COLOR_BLUE "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN "\x1b[36m"
#define ANSI_COLOR_RESET "\x1b[0m"

/*ταχύτητα*/
#define SPEED 4
#define TIME_STEP 64

/*πιθανά χρώματα*/
enum BLOB_TYPE { RED, GREEN, BLUE, NONE };

/*_______________________________________
Η συνάρτηση απόφασης χρώματος*/

int color(const unsigned char *image, int width,int height){
/* Reset the sums */
          int i;
          int j;
          int red = 0;
          int green = 0;
          int blue = 0;
          enum BLOB_TYPE current_blob;
    
          /*Μετράει τα pixel*/
          for (i = width / 3; i < 2 * width / 3; i++) {
            for (j = height / 2; j < 3 * height / 4; j++) {
              red += wb_camera_image_get_red(image, width, i, j);
              blue += wb_camera_image_get_blue(image, width, i, j);
              green += wb_camera_image_get_green(image, width, i, j);
            }
          }
    
          /*
           Επικρατέστερο χρώμα
           */
           
          if ((red > 3 * green) && (red > 3 * blue))
            current_blob = RED;
          else if ((green > 3 * red) && (green > 3 * blue))
            current_blob = GREEN;
          else if ((blue > 3 * red) && (blue > 3 * green))
            current_blob = BLUE;
          else
            current_blob = NONE;
              
  return current_blob;
}

/*_______________________________________
Η main*/

int main() {

  /*αρχικοποίηση μεταβλητών/παραμέτρων*/
  WbDeviceTag camera, left_motor, right_motor,ds0,ds1;
  int width, height;
  double left_speed, right_speed;
  const char *color_names[3] = {"red", "green", "blue"};
  const char *ansi_colors[3] = {ANSI_COLOR_RED, ANSI_COLOR_GREEN, ANSI_COLOR_BLUE};
  enum BLOB_TYPE current_blob;
  enum BLOB_TYPE target_blob= BLUE;
  int stop=40;
  int time=500;
  int mode=1;
  wb_robot_init();/*αρχικοποίηση του ρομπότ*/
  
  /*αισθητήρες*/
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
  
  
/*_______________________________________
Το Main Loop*/


  while (wb_robot_step(TIME_STEP) != -1) {
    /* Get the new camera values */
    const unsigned char *image = wb_camera_get_image(camera);
    switch (mode){
    
      /*_______________________________________
      Ξεκινάει με κύκλο γύρω από τον εαυτό του*/
    
      case 1:
        /* Decrement the pause_counter*/
        if (stop!=0){
          
          /*Αναγνώριση Χρωμάτων*/
          current_blob=color(image,width,height);
          if (current_blob == target_blob){
            mode=3;
            }
          
          stop--;/* Για να σταματήσει*/
          left_speed = -SPEED;
          right_speed = SPEED;
          /*
           Δεν βρήκε κάποιο χρώμα*/
          if(current_blob!=NONE) {
            printf("Looks like I found a %s%s%s blob.\n", ansi_colors[current_blob], color_names[current_blob], ANSI_COLOR_RESET);      
          }
          }
          
          /*_______________________________________
          Τελείωσε ο κ΄υκλος και τώρα πάει ευθεία αποφεύγοντας εμπόδια*/
          
          else{
          time=500;
            mode=2;
            }
          break;


        case 2:
    
           /*_______________________________________
          Αποφυγή εμποδίων*/
    
            
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
          
          /*Αναγνώριση Χρωμάτων*/          
          current_blob=color(image,width,height);
          
          if (current_blob == target_blob){
            mode=3;
            }
          
          if(current_blob!=NONE) {
            printf("Looks like I found a %s%s%s blob.\n", ansi_colors[current_blob], color_names[current_blob], ANSI_COLOR_RESET);      
          }
          
          time--;
          if (time==0){
            stop=20;
            mode=1;
            }
          break;
          
        case 3:
        
          left_speed = 0;
          right_speed = 0;
          printf("Target %s%s%s found.\n", ansi_colors[current_blob], color_names[current_blob], ANSI_COLOR_RESET);
          mode=4;
          
          break;
         
        case 4:
          
          break;
          }
      

    /* Set the motor speeds. */
    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);
  }
  

  wb_robot_cleanup();

  return 0;
}
