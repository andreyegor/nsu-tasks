#include <string>
#include <iostream>
#include <assert.h>
#include <random>
#include "gtest/gtest.h"

bool epsilon_eq(double p1, double p2) {
    return fabs(p1 - p2) < 0.00001;
}

struct Point {
    double x;
    double y;
    bool exists = true;

    std::string get_string() const {
        return "(" + std::to_string(this->x) + ";" + std::to_string(this->y) + ")";
    }

    bool operator==(const Point &other) const { // equal
        return epsilon_eq(this->x, other.x) && epsilon_eq(this->y, other.y);
    }
};

class Line {
    // ax+by+c==0
    double a;
    double b;
    double c;

public:
    Line(const Point &point_1, const Point &point_2) {
        this->a = point_2.y - point_1.y;
        this->b = point_1.x - point_2.x;
        this->c = -1 * (a * (point_1.x) + b * (point_1.y));
    }

    Line(double a, double b, double c) {
        assert(a != 0 || b != 0);
        this->a = a;
        this->b = b;
        this->c = c;
    }

    Line(double a, double b, const Point &point) {// proverirt'
        assert(a != 0 || b != 0);
        this->a = a;
        this->b = b;
        this->c = -1 * (a * (point.x) + b * (point.y));
    }

    Point operator&(const Line &other) const {
        if ((*this || other) || (*this == other)) {
            return Point{0, 0, false};
        } else {
            return Point{(this->b * other.c - other.b * this->c) / (this->a * other.b - other.a * this->b),
                         (other.a * this->c - this->a * other.c) / (this->a * other.b - other.a * this->b)};
        }
    }

    bool operator||(const Line &other) const {
        double k1 = this->a * other.b * other.c, k2 = other.a * this->b * other.c, k3 = other.a * other.b * this->c;
        return (epsilon_eq(k1, k2)) &&
               (k2 != 0 ? !epsilon_eq(k2, k3) : !epsilon_eq(this->c, other.c));
    }

    bool operator==(const Line &other) const { // equal
        double k1 = this->a * other.b * other.c, k2 = other.a * this->b * other.c, k3 = other.a * other.b * this->c;
        return epsilon_eq(k1, k2) && epsilon_eq(k2, k3);
    }


    Line get_perpendicular(const Point &point) const {
        return Line(this->b, -1 * this->a, point);
    }

    std::string get_string() const {
        return std::to_string(this->a) + (this->b > 0 ? "+" : "") + std::to_string(this->b)
               + (this->c > 0 ? "+" : "") + std::to_string(this->c) + "==0";
    }
};

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
        Point intersection = main_line & perpendicular_line;
        EXPECT_TRUE(main_line.get_perpendicular(intersection) == perpendicular_line);
    }
}


int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}