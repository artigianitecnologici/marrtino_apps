rosservice call /sfr03_controller/set_torque_limit "torque_limit: 1"
rosservice call /sfl00_controller/set_torque_limit "torque_limit: 1"
rosservice call /sbr09_controller/set_torque_limit "torque_limit: 1"
rosservice call /sbl06_controller/set_torque_limit "torque_limit: 1"

rosservice call /sfr03_controller/set_speed "speed: 0.6"
rosservice call /sfl00_controller/set_speed "speed: 0.6"
rosservice call /sbr09_controller/set_speed "speed: 0.6"
rosservice call /sbl06_controller/set_speed "speed: 0.6"
 
rosservice call /sfr04_controller/set_torque_limit "torque_limit: 1"
rosservice call /sfl01_controller/set_torque_limit "torque_limit: 1"
rosservice call /sbr10_controller/set_torque_limit "torque_limit: 1"
rosservice call /sbl07_controller/set_torque_limit "torque_limit: 1"

rosservice call /sfr04_controller/set_speed "speed: 0.6"
rosservice call /sfl01_controller/set_speed "speed: 0.6"
rosservice call /sbr10_controller/set_speed "speed: 0.6"
rosservice call /sbl07_controller/set_speed "speed: 0.6"