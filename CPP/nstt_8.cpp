#include <string>

class Expression {
protected:
    static std::string to_string(Expression *exp, int priority = 21) {
        if ((exp->priority) > priority) {
            return (std::string) *exp;
        }
        return "(" + (std::string) *exp + ")";
    }

    const int priority=-1;

public:
    virtual ~Expression() = default;

    virtual explicit operator std::string() = 0;

    virtual Expression *diff(std::string var) = 0;

    virtual Expression *copy() = 0;
};

class Binary : public Expression {
protected:
    Expression *left;
    Expression *right;

    std::string to_str_sign(const std::string &sign, const int &in_priority = 21) {
        return to_string(left, in_priority) + sign + to_string(right, in_priority);
    }

public:
    Binary(Expression *left_in, Expression *right_in) {
        left = left_in;
        right = right_in;
    }

    Binary(const Binary &other) = delete;

    Binary(Binary &&other) = delete;

    ~Binary() override {
        delete left;
        delete right;
    }

    explicit operator std::string() override {
        return to_str_sign("?");
    }

    const int priority = 21;

};

class Unary : public Expression {
protected:
    Expression *exp;
public:
    explicit Unary(Expression *exp_in) {
        exp = exp_in;
    }

    Unary(const Unary &other) = delete;

    Unary(Unary &&other) = delete;

    ~Unary() override {
        delete exp;
    }

    explicit operator std::string() override {
        return to_string(exp);
    }

    const int priority = 21;
};

class Add : public Binary {
public:
    using Binary::Binary;//https://en.cppreference.com/w/cpp/language/using_declaration

    explicit operator std::string() override {
        return to_str_sign(" + ", priority);
    }

    Add *diff(std::string var) override {
        return new Add(left->diff(var), right->diff(var));
    }

    Add *copy() override {
        return new Add(left->copy(), right->copy());
    }

    const int priority = 1;
};

class Sub : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() override {
        return to_str_sign(" - ", priority);
    }

    Sub *diff(std::string var) override {
        return new Sub(left->diff(var), right->diff(var));
    }

    Sub *copy() override {
        return new Sub(left->copy(), right->copy());
    }
};

class Mult : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() override {
        return to_str_sign("*", priority);
    }

    Add *diff(std::string var) override {
        return new Add(new Mult(left->diff(var), right->copy()), new Mult(left->copy(), right->diff(var)));
    }

    Mult *copy() override {
        return new Mult(left->copy(), right->copy());
    }

    const int priority = 2;
};

class Div : public Binary {
public:
    using Binary::Binary;

    explicit operator std::string() override {
        return to_str_sign("/", priority);
    }

    Div *diff(std::string var) override {
        return new Div(new Sub(new Mult(left->diff(var), right->copy()), new Mult(left->copy(), right->diff(var))),
                       new Mult(right->copy(), right->copy()));
    }

    Div *copy() override {
        return new Div(left->copy(), right->copy());
    }

    const int priority = 2;
};

class Exponent : public Unary {
public:
    using Unary::Unary;

    explicit operator std::string() override {
        return "e^" + to_string(exp, priority);//highest priority, no brackets needed
    }

    Mult *diff(std::string var) override {
        return new Mult(exp->diff(var), new Exponent(exp->copy()));
    }

    Exponent *copy() override {
        return new Exponent(exp->copy());
    }


    const int priority = 3;

};

class Val : public Expression {
    int val;
public:

    explicit Val(int val_in) {
        val = val_in;
    }

    Val(const Val &other) = delete;

    Val &operator=(const Val &other) = delete;

    explicit operator std::string() override {
        return std::to_string(val);
    }

    Val *diff(std::string var_in) override {
        return new Val(0);
    }

    Val *copy() override {
        return new Val(val);
    }

    const int priority = 21;

};

class Var : public Expression {
    std::string var;
public:
    explicit Var(const std::string &var_in) {
        var = var_in;
    }


    Var(const Var &other) = delete;

    explicit operator std::string() override {
        return var;
    }

    Expression *diff(std::string var_in) override {
        if (var_in != var) {
            return new Val(0);
        }
        return new Val(1);
    }

    Var *copy() override {
        return new Var(var);
    }

    const int priority = 21;

};