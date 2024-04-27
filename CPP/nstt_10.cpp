#include "execution"

template<class C, int LIMIT>
class LimitInstances {
    static inline int alive_objects = 0;//https://habr.com/ru/companies/otus/articles/561772/

    void limited() {
        if (alive_objects == LIMIT) {
            throw std::runtime_error("Too many objects are already exists");
        }
        alive_objects++;
    }

public:
    LimitInstances() {
        limited();
    }

    LimitInstances(const LimitInstances &) {
        limited();
    }

    ~LimitInstances() {
        alive_objects--;
    }
};