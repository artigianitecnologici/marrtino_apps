# 44+45 1,48
# 129 2,25147

rostopic pub -1 /sfr05_controller/command std_msgs/Float64 "data: 0.19"
rostopic pub -1  /sfl02_controller/command std_msgs/Float64 "data: 0.0"
rostopic pub -1  /sbr11_controller/command std_msgs/Float64 "data: 0.19"
rostopic pub -1  /sbl08_controller/command std_msgs/Float64 "data: 0.0"

rostopic pub -1  /sbr10_controller/command std_msgs/Float64 "data: 0.994"
rostopic pub -1  /sbr09_controller/command std_msgs/Float64 "data: 0.61"

rostopic pub -1 /sfr04_controller/command std_msgs/Float64 "data: 0.994"
rostopic pub -1 /sfr03_controller/command std_msgs/Float64 "data: 0.61"


rostopic pub -1 /sfl01_controller/command std_msgs/Float64 "data: -0.994"
rostopic pub -1 /sfl00_controller/command std_msgs/Float64 "data: -0.61"

rostopic pub -1  /sbl07_controller/command std_msgs/Float64 "data: -0.994"
rostopic pub -1  /sbr06_controller/command std_msgs/Float64 "data: -0.61"

