# FRA502 Service Robot Project: Final Presentation
> หุ่นยนต์สำหรับขนส่งกล่องพัสดุภายในคอนโด หุ่นจะรับพัสดุจากตำแหน่งรับพัสดุและนำไปส่งได้พร้อมกันไม่เกิน 2 ห้อง หุ่นยนต์จะรอเพื่อรับโค้ดเพื่อยืนยันตัวตนและเดินออกไปเมื่อพัสดุถูกหยิบไปและได้รับคำยืนยันจากผู้หยิบ

## Description
### 1. Environment
- OS: Ubuntu 20.04 LTS
- ROS: Noetic

### 2. Dependencies
- actionlib
- amcl
- gazebo_ros
- geometry_msgs
- map_server
- move_base_msgs
- std_ms
- rospy
- turtlebot3
- sensor_msgs
- sound_play

### 2. Python library
- pyaudio
- pttsx3
- SpeechRecognition

## Getting ready

เนื่องจากในตอนนี้หุ่นยนต์ที่ได้ทำขึ้นยังมีปัญหา[^1] จึงต้องใช้ turtle bot ในการรันใน gazebo
```
cd ~/[your_desire_catkin_workspace]/src
git clone https://github.com/notchap30/Delirobot
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
```
source file
```
cd ..
source devel/setup.bash
```
## Run gazebo and Rviz

การเปิด gazebo ด้วย Apartment world โดยภายในคำสั่งจะทำการเปิด Rviz ที่มีการตั้งค่าไว้ให้ และจะมีการ spawn หุ่นยนต์ให้โดยหุ่นยนต์ดังกล่าวคือ turtlebot burger model 

```
roslaunch delirobot world.launch
```

## Mapping
หลังจากที่ได้เปิด gazebo world แล้ว ให้รันคำสั่งเพื่อบังคับการเดินเพื่อเริ่มเก็บ map 
```
roslaunch delirobot teleop.launch
```
หลังจากทีเดินจะมีการจำแมพแสดงให้เห็นผ่านโปรแกรม rviz เมื่อเดินจนครบให้รันคำสั่งด้านล่างเพื่อบันทึก 
map ที่ถูกบันทึกจะถูกนำไปเก็บภายในโฟลเดอร์ชื่อว่า maps
```
rosrun map_server map_saver -f ~/[your_desire_catkin_workspace]/src/delirobot/maps/map
```
## All set! Try out the robot
การรันหุ่นยนต์จะต้องใช้ terminal ทั้งหมดสามช่องเพื่อรันไฟล์ .launch และไฟล์ .py แยกกันได้แก่

- world.launch
```
source devel/setup.bash
roslaunch delirobot world.launch
```
- navigation.launch
```
source devel/setup.bash
roslaunch delirobot_navigation delirobot_navigation.launch
```
- delispeech.py
```
source devel/setup.bash
rosrun delirobot delispeech.py
```
หน้าจอจะถูกแสดงขึ้นมาพร้อมกับหุ่นยนต์ในตำแหน่งรับพัสดุ

## Voice command
การใช้งานหุ่นยนต์จะแบ่งเป็นฝั่งของ user และ client userจะใช้งานเมื่อหุ่นยนต์อยู่ ณ ตำแหน่งรับพัสดุ และ client จะอยู่ที่ห้อง
 
### user command
ในฝั่งผู้ใช้จะเน้นการพิมพ์เนื่องจากมีคำสั่งที่ต้องใช้เยอะ ในช่วงที่ไม่ได้ทำอะไรหุ่นยนต์จะอยู่นิ่งๆจนกว่าจะถูกเรียก ในช่วงที่หุ่นยนต์อยู่นิ่ง โค้ดจะอยู่ในลูปสามารถสั่งคำสั่งให้จบการทำงานของไฟล์โดยใช้คำสั่ง
 - **delistop** (พิมพ์)

 คำสั่งในการเรียก[^2]หุ่นยนต์คือ
- **hey** (พิมพ์)
 หรือใช้การเรียกด้วยเสียงโดยพิมพ์คำสั่ง
- **delilisten** (พิมพ์)
ตามด้วย
- **hey** (พูด)

หลังจากนั้นหุ่นยนต์จะถามว่าต้องการให้ไปส่งกี่ห้อง 
- **1** หรือ **2** (พิมพ์)

หุ่นยนต์จะถามต่อว่าต้องการให้ทำอะไรต่อโดยจะเป็นการจัดการตัวหุ่นยนต์[^3] สามารถสั่งการได้ต่อไปนี้
- **upper open** เป็นการเปิดฝาด้านบนของหุ่น
- **upper close** เป็นการปิดฝาด้านบนของหุ่น
- **lower open** เป็นการเปิดฝาด้านล่างของหุ่น
- **lower close** เป็นการปิดฝาด้านล่างของหุ่น
- **bigbox** เป็นการเปิดแผ่นที่กันทั้งสองช่อง
- **smallbox** เป็นการปิดแผ่นที่กันทั้งสองช่อง
- **ready** เพื่อไปคำสั่งต่อไป

หลังจากนั้นหุ่นยนต์จะถามว่าห้องที่ต้องการจะส่งอยู่ห้องไหนและจะถามตามจำนวนห้องที่ได้เลือกไว้ในตอนแรก
- **[พิมพ์เลขห้อง]** เพื่อบอกห้องที่ต้องการส่ง
หุ่นยนต์จะถามว่ายืนยันไหมให้พิมพ์ว่า
clip
[^1]: ปัญหาที่พบ
