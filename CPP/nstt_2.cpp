#include <string>
#include <iostream>
#include <assert.h>
#include <random>

bool epsilon_eq(double p1, double p2) {
    return fabs(p1 - p2) < 0.00001;
}

struct Point {
    const double x;
    const double y;

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
            throw std::runtime_error("Lines are parallel");
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

