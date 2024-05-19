#include "nstt_13.cpp"
#include "gtest/gtest.h"

template<int exp>
bool is_eq(const int &n) {
    return n == exp;
}

TEST(lonley_test_suite, lonley_test_case) {
    EXPECT_EQ(getIndexOfFirstMatch(is_eq<3>, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9), 3);
    EXPECT_EQ(getIndexOfFirstMatch(is_eq<3>, 0, 3, 2, 3, 3, 5, 3, 3, 8, 3), 1);
    EXPECT_EQ(getIndexOfFirstMatch(is_eq<0>, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0);
    EXPECT_EQ(getIndexOfFirstMatch(is_eq<9>, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9), 9);
    EXPECT_EQ(getIndexOfFirstMatch(is_eq<11>, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9), -1);
}