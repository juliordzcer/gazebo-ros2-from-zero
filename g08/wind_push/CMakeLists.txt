cmake_minimum_required(VERSION 3.16)
project(wind_push)

find_package(gz-plugin2 REQUIRED COMPONENTS register)
find_package(gz-sim8 REQUIRED)

add_library(WindPush SHARED WindPush.cc)
target_link_libraries(WindPush
  gz-plugin2::register
  gz-sim8::gz-sim8)
