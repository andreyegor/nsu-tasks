#include "tuple"
#include "gtest/gtest.h"
#include "iostream"

template<typename type>
class ScopedPointerFirst {
    type *pointer = nullptr;
public:
    explicit ScopedPointerFirst(type *inp) : pointer(inp) {}

    ScopedPointerFirst(const ScopedPointerFirst &other) : pointer(new type(*other.pointer)) {}

    ScopedPointerFirst &operator=(const ScopedPointerFirst &other) {
        pointer = new type(*other.pointer);
        return *this;
    }

    ScopedPointerFirst(ScopedPointerFirst &&other) noexcept {
        std::swap(pointer, other.pointer);
    }

    ScopedPointerFirst &operator=(ScopedPointerFirst &&other) {
        std::swap(pointer, other.pointer);
        return *this;
    }

    ~ScopedPointerFirst() {
        delete pointer;
    }

    type &operator*() {
        return *pointer;
    }

    const type &operator*() const {
        return *pointer;
    }

    type *operator->() {
        return pointer;
    }

    const type *operator->() const {
        return pointer;
    }

    bool operator==(ScopedPointerFirst other) const {
        return pointer == other.pointer;
    }

    type *get() {
        return pointer;
    }

};

template<typename type>
class ScopedPointerSecond : public ScopedPointerFirst<type> {
public:
    explicit ScopedPointerSecond(type *inp) : ScopedPointerFirst<type>(inp) {}

    ScopedPointerSecond(const ScopedPointerSecond &other) = delete;

    ScopedPointerSecond &operator=(const ScopedPointerSecond &other) = delete;

    ScopedPointerSecond(ScopedPointerSecond &&other) noexcept: ScopedPointerFirst<type>(std::move(other)) {}
};


struct Triple {
    int x;
    int y;
    int z;

    bool operator==(Triple &other) const {
        return x == other.x && y == other.y && z == other.z;
    }
};


TEST(ScopePointerFirst, deep_copyng) {
    ScopedPointerFirst sp1{new Triple{13, 42, 1}};
    ScopedPointerFirst sp2 = sp1;
    sp2->x = 42;
    EXPECT_FALSE(sp1 == sp2);
}

TEST(ScopePointerFirst, transferring_an_ownership) {
    ScopedPointerFirst sp1{new Triple{13, 42, 1}};
    ScopedPointerFirst sp2 = std::move(sp1);
    EXPECT_TRUE(sp1.get() == nullptr);
}

TEST(ScopePointerSecond, transferring_an_ownership) {
    ScopedPointerSecond sp1{new Triple{13, 42, 1}};
    ScopedPointerSecond sp2 = std::move(sp1);
    std::cout<<sp1.get()<<std::endl;
    EXPECT_TRUE(sp1.get() == nullptr);
}