#include "gtest/gtest.h"
#include "nstt_10.cpp"

class Foo : LimitInstances<Foo, 3> {
    int a;
public:
    explicit Foo(int in_a) {
        a = in_a;
    }

};

class Bar : LimitInstances<Bar, 2> {
};

TEST(lonly_test_suite, lonly_test_case) {
    Foo a{1};
    Foo b{2};
    Foo c{3};
    EXPECT_THROW(Foo d{4}, std::runtime_error);
    a.~Foo();
    Foo e{5};
    EXPECT_THROW(Foo f{6}, std::runtime_error);
    Bar g;
    Bar h;
    EXPECT_THROW(Bar i, std::runtime_error);

}
