#include "gtest/gtest.h"
#include "nstt_2.cpp"

TEST(lonley_test_suite, few_manual_tests) {
    EXPECT_TRUE(Line(1, 2, 3) == Line(2, 4, 6));
    EXPECT_TRUE(Line(0, 2, 0) == Line(0, 5, 0));
    EXPECT_TRUE(Line(1, 2, 3) == Line(1, 2, Point{-3, 0}));
    EXPECT_TRUE(Line(1, 2, 3) == Line(Point{0, -1.5}, Point{-3, 0}));
    EXPECT_TRUE(Line(1, 2, 3) || Line(1, 2, 4));
    EXPECT_TRUE(Line(0, 2, 0) == Line(0, 5, 0));
    EXPECT_TRUE(Line(0, 2, 0) || Line(0, 5, 10));

    EXPECT_TRUE(Line(1, 2, 3).get_perpendicular(Point{-3, 0}) == Line(2, -1, 6));
    EXPECT_TRUE(Line(0, 2, 0).get_perpendicular(Point{0, 0}) == Line(-2, 0, 0));

    EXPECT_TRUE(Line(1, 2, 3).get_perpendicular(Point{0, -1.5}) == Line(-4, 2, 3));
    EXPECT_TRUE((Line(1, 2, 3) & Line(-4, 2, 3)) == (Point{0, -1.5}));
}

TEST(lonley_test_suite, eq_parrallel_test) {
    for (int i = 0; i < 100; i++) {
        double a = rand() % 100, b = rand() % 99 + 1, c = rand() % 100;
        double k = rand() % 10 + 1;
        Line main_line = Line(a, b, c);
        Line same_line = Line(a * k, b * k, c * k);
        Line parallel_line = Line(a, b, c + k);
        EXPECT_TRUE(main_line == same_line);
        EXPECT_TRUE(main_line || parallel_line);
        EXPECT_FALSE(main_line == parallel_line);
        EXPECT_FALSE(main_line || same_line);
    }
}

TEST(lonley_test_suite, intersection_perpendicular_test) {
    //strange test, but idk how do it better
    for (int i = 0; i < 100; i++) {
        double a = rand() % 10, b = rand() % 9 + 1, c = rand() % 10;
        double k = rand() % 1 + 1;
        Line main_line = Line(a, b, c);
        Line perpendicular_line = Line(-1 * b * k, a * k, c * k);
        if (!((main_line || perpendicular_line)|main_line==perpendicular_line)) {
            Point intersection = main_line & perpendicular_line;
            EXPECT_TRUE(main_line.get_perpendicular(intersection) == perpendicular_line);
        } else {
            EXPECT_THROW(main_line & perpendicular_line, std::runtime_error);
        }
    }
}
