#include "gtest/gtest.h"
#include "nstt_7.cpp"

TEST(nstt_7, test_from_presentation) {
    Expression *e = new Add(new Var("x"),
                            new Mult(new Val(10), new Var("y")));
    Expression *res1 = e->diff("x");
    Expression *res2 = e->diff("y");

    EXPECT_EQ((std::string) *e, "x + 10*y");
    EXPECT_EQ((std::string) *res1, "1 + (0*y + 10*0)");
    EXPECT_EQ((std::string) *res2, "0 + (0*y + 10*1)");

    delete e;
    delete res1;
    delete res2;
}


TEST(nstt_7, exponent_division_test) {
    Expression *e = new Exponent(new Div(new Var("x"), new Sub(new Val(2), new Var("x"))));
    Expression *q = e->diff("x");
    EXPECT_EQ(
            (std::string) *q, "((1*(2 - x) - x*(0 - 1))/((2 - x)*(2 - x)))*e^(x/(2 - x))");//i checked, seems correct

    delete e;
    delete q;
}