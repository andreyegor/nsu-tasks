cmake_minimum_required(VERSION 3.6)
project(CPP)

ADD_SUBDIRECTORY(googletest)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=leak")

link_libraries(GTest::gtest_main)

add_executable(test_8 nstt_8_test.cpp)

