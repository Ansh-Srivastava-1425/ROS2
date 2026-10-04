cmake_minimum_required(VERSION 3.8)
project(my_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# install launch folder
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# install Python scripts
install(PROGRAMS
  scripts/pub.py
  scripts/sub.py
  scripts/draw_circle.py
  scripts/pose_subscriber.py
  scripts/add_two_ints_server.py
  scripts/add_two_ints_clients.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package() 