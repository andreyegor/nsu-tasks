#include <string>

class Expression {
protected:
    static std::string to_string(Expression *exp, int priority = 21) {
        if (exp->priority > priority) {
            return (std::string) *exp;
        }
        return "(" + (std::string) *exp + ")";
    }

    char priority = 0;

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
};

class Add : public Binary {
public:
    using Binary::Binary;//https://en.cppreference.com/w/cpp/language/using_declaration

    Add(Expression *left_in, Expression *right_in) : Binary(left_in, right_in) {
        priority = 1;
    }

    explicit operator std::string() override {
        return to_str_sign(" + ", priority);
    }

    Add *diff(std::string var) override {
        return new Add(left->diff(var), right->diff(var));
    }

    Add *copy() override {
        return new Add(left->copy(), right->copy());
    }

};

class Sub : public Binary {
public:
    using Binary::Binary;

    Sub(Expression *left_in, Expression *right_in) : Binary(left_in, right_in) {
        priority = 1;
    }

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

    Mult(Expression *left_in, Expression *right_in) : Binary(left_in, right_in) {
        priority = 2;
    }

    explicit operator std::string() override {
        return to_str_sign("*", priority);
    }

    Add *diff(std::string var) override {
        return new Add(new Mult(left->diff(var), right->copy()), new Mult(left->copy(), right->diff(var)));
    }

    Mult *copy() override {
        return new Mult(left->copy(), right->copy());
    }
};

class Div : public Binary {
public:
    using Binary::Binary;

    Div(Expression *left_in, Expression *right_in) : Binary(left_in, right_in) {
        priority = 2;
    }

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
};

class Exponent : public Unary {
public:
    using Unary::Unary;

    explicit Exponent(Expression *exp_in) : Unary(exp_in) {
        priority = 3;
    }

    explicit operator std::string() override {
        return "e^" + to_string(exp, priority);//highest priority, no brackets needed
    }

    Mult *diff(std::string var) override {
        return new Mult(exp->diff(var), new Exponent(exp->copy()));
    }

    Exponent *copy() override {
        return new Exponent(exp->copy());
    }
};

class Val : public Expression {
    int val;

public:
    explicit Val(int val_in) {
        priority = 21;
        val = val_in;
    }

    Val(const Val &other) = delete;

    Val(Val &&other) = delete;

    explicit operator std::string() override {
        return std::to_string(val);
    }

    Val *diff(std::string var_in) override {
        return new Val(0);
    }

    Val *copy() override {
        return new Val(val);
    }

};

class Var : public Expression {
    std::string var;

public:
    explicit Var(const std::string &var_in) {
        priority = 21;
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
};