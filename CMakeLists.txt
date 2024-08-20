project(imesa_experiments CXX C)
cmake_minimum_required(VERSION 2.8.3)
set(CMAKE_CXX_STANDARD 20)

message(STATUS "================  CMake iMESA Experiments  ======================")

# Dependency - GTSAM
find_package(GTSAM REQUIRED)
include_directories(${GTSAM_INCLUDE_DIR})

find_package(imesa REQUIRED)

# Build the methods we evaluate
add_subdirectory(prior_work)

# Build the experiment infrastructure
add_subdirectory(experiments)
