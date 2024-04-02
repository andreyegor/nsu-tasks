#include <iostream>
#include <string>
#include "gtest/gtest.h"

class Expression {
protected:
    static const std::string to_string(Expression *exp, int priority = 21) {
        if ((exp->priority()) > priority) {
            return (std::string) *exp;
        }
        return "(" + (std::string) *exp + ")";
    }

public:
    virtual ~Expression() {};

    virtual explicit operator std::string() = 0;

    virtual Expression *diff(std::string var) = 0;

    virtual Expression *copy() = 0;

    virtual char priority() = 0;


};

class Binary : public Expression {
protected:
    Expression *left;
    Expression *right;

    const std::string to_str_sign(std::string sign, int priority = 21) {
        return to_string(left, priority) + sign + to_string(right, priority);
    }

public:
    Binary(Expression *left_in, Expression *right_in) {
        left = left_in;
        right = right_in;
    }


    ~Binary() {
        delete left;
        delete right;
    }

    explicit operator std::string() {
        return to_str_sign("?");
    }

    char priority() {
        return 21;
    }

};

class Unary : public Expression {
protected:
    Expression *exp;
public:
    Unary(Expression *exp_in) {
        exp = exp_in;
    }

    Unary(const Unary& other){
        this->exp = other.exp->copy();
    }

    Unary(Unary&& other){
        this->exp = other.exp;
    }

    ~Unary() {
        delete exp;
    }

    explicit operator std::string() {
        return to_string(exp);
    }

    char priority() {
        return 21;
    }


};

class Add : public Binary {
public:
    using Binary::Binary;//https://en.cppreference.com/w/cpp/language/using_declaration

    explicit operator std::string() {
        return to_str_sign(" + ", priority());
    }

    Add *diff(std::string var) {
        return new Add(left->diff(var), right->diff(var));
    }

    Add *copy() {
        return new Add(left->copy(), right->copy());
    }

    char priority() {
        return 1;
    }
};

class Sub : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() {
        return to_str_sign(" - ", priority());
    }

    Sub *diff(std::string var) {
        return new Sub(left->diff(var), right->diff(var));
    }

    Sub *copy() {
        return new Sub(left->copy(), right->copy());
    }

    char priority() {
        return 1;
    }

};

class Mult : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() {
        return to_str_sign("*", priority());
    }

    Add *diff(std::string var) {
        return new Add(new Mult(left->diff(var), right->copy()), new Mult(left->copy(), right->diff(var)));
    }

    Mult *copy() {
        return new Mult(left->copy(), right->copy());
    }

    char priority() {
        return 2;
    }
};

class Div : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() {
        return to_str_sign("/", priority());
    }

    Div *diff(std::string var) {
        return new Div(new Sub(new Mult(left->diff(var), right->copy()), new Mult(left->copy(), right->diff(var))),
                       new Mult(right->copy(), right->copy()));
    }

    Div *copy() {
        return new Div(left->copy(), right->copy());
    }

    char priority() {
        return 2;
    }
};

class Exponent : public Unary {
public:
    using Unary::Unary;

    explicit operator std::string() {
        return "e^" + to_string(exp, priority());//highest priority, no brackets needed
    }

    Mult *diff(std::string var) {
        return new Mult(exp->diff(var), new Exponent(exp->copy()));
    }

    Exponent *copy() {
        return new Exponent(exp->copy());
    }


    char priority() {
        return 3;
    }

};

class Val : public Expression {
    int val;
public:

    Val(int val_in) {
        val = val_in;
    }

    explicit operator std::string() {
        return std::to_string(val);
    }

    Val *diff(std::string var_in) {
        return new Val(0);
    }

    Val *copy() {
        return new Val(val);
    }

    char priority() {
        return 21;
    }

};

class Var : public Expression {
    std::string var;
public:
    Var(const std::string var_in) {
        var = var_in;
    }

    explicit operator std::string() {
        return var;
    }

    Expression *diff(std::string var_in) {
        if (var_in != var) {
            return new Val(0);
        }
        return new Val(1);
    }

    Var *copy() {
        return new Var(var);
    }

    char priority() {
        return 21;
    }

};

TEST(lonley_test_suite, test_from_presentation) {
    Expression *e = new Add(new Var("x"),
                            new Mult(new Val(10), new Var("y")));
    Expression *res1 = e->diff("x");
    Expression *res2 = e->diff("y");

    EXPECT_TRUE((std::string) *e == "x + 10*y");
    EXPECT_TRUE((std::string) *res1 == "1 + (0*y + 10*0)");
    EXPECT_TRUE((std::string) *res2 == "0 + (0*y + 10*1)");

    delete e;
    delete res1;
    delete res2;
}


TEST(lonley_test_suite, exponent_division_test) {
    Expression *e = new Exponent(new Div(new Var("x"), new Sub(new Val(2), new Var("x"))));
    Expression *q = e->diff("x");
    std::cout<<(std::string) *q;
    EXPECT_TRUE((std::string) *q == "((1*(2 - x) - x*(0 - 1))/((2 - x)*(2 - x)))*e^(x/(2 - x))");//i checked, seems correct

    delete e;
    delete q;
}