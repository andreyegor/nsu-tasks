cmake_minimum_required(VERSION 3.6)
project(CPP)

ADD_SUBDIRECTORY(googletest)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=leak")

link_libraries(GTest::gtest_main)

add_executable(test_1349 nstt_1349_test.cpp)
add_executable(test_2 nstt_2_test.cpp)
add_executable(test_5 nstt_5_test.cpp)
add_executable(test_6 nstt_6_test.cpp)
add_executable(test_7 nstt_7_test.cpp)
add_executable(test_8 nstt_8_test.cpp)
add_executable(test_10 nstt_10_test.cpp)
add_executable(test_11 nstt_11_test.cpp)