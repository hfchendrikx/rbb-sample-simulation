cmake_minimum_required(VERSION 2.8.3)
project(outputs_a_sine)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(sine_wave src/sine_wave.cpp)
target_link_libraries(sine_wave ${catkin_LIBRARIES})
