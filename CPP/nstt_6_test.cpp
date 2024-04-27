#include "gtest/gtest.h"
#include "nstt_6.cpp"

TEST(FirstCase, from_vector) {
    Matrix first{std::vector<double>{1, 2}};
    Matrix second{{{1., 0.}, {0., 2.}}, 2};
    EXPECT_TRUE(first == second);
};

TEST(SecondCase, conversion_to_double) {
    Matrix first{{{1., 0.}, {0., 2.}}, 2};
    EXPECT_TRUE((double) first == 3.);
}

TEST(operators, overloaded_operators_add) {
    Matrix first{{{1., 1.}, {2., 0.}}, 2};
    Matrix second{{{0., 1.}, {1., 4.}}, 2};
    Matrix expected{{{1., 2.}, {3., 4.}}, 2};

    EXPECT_TRUE(first + second == expected);
    second += first;
    EXPECT_TRUE(second == expected);

    Matrix expected_scalar{{{2., 2.}, {3., 1.}}, 2};
    EXPECT_TRUE(first + 1. == expected_scalar);
    first += 1.;
    EXPECT_TRUE(first == expected_scalar);
}

TEST(operators, overloaded_operators_mul) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    Matrix second{{{5, 6}, {7, 8}}, 2};
    Matrix expected{{{19, 22}, {43, 50}}, 2};

    EXPECT_TRUE(first * second == expected);
    first *= second;
    EXPECT_TRUE(first == expected);

    Matrix expected_scalar{{{10, 12}, {14, 16}}, 2};
    EXPECT_TRUE(2 * second == expected_scalar);
    second *= 2;
    EXPECT_TRUE(second == expected_scalar);
}

TEST(double_indexing, double_indexing) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    EXPECT_TRUE(first[0][0] == 1);
    EXPECT_TRUE(first[0][1] == 2);
    EXPECT_TRUE(first[1][0] == 3);
    EXPECT_TRUE(first[1][1] == 4);

    EXPECT_THROW(first[5][0], std::out_of_range);
    EXPECT_THROW(first[0][5], std::out_of_range);
}

TEST(move, move_test) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    Matrix second = first;
    Matrix third = std::move(first);
    EXPECT_TRUE(second == third);
    EXPECT_TRUE(first == (Matrix{{}, 0}));
}

TEST(mul_add_exeption, multiple_add_diff_size_test) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    Matrix second{{{1}, {2}}, 1};

    EXPECT_THROW(first * second, std::range_error);
    EXPECT_THROW(first + second, std::range_error);
}